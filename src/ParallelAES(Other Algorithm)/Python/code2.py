import os
import time
import hashlib
import threading
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from dataclasses import dataclass
from typing import List, Tuple, Optional
import struct

try:
    from Crypto.Cipher import AES, ChaCha20
    from Crypto.Random import get_random_bytes
    CRYPTO_AVAILABLE = True
except ImportError:
    print("Warning: pycryptodome not available, using basic implementation")
    CRYPTO_AVAILABLE = False

# Global worker function for multiprocessing
def process_chunk_worker_global(args):
    """Global worker function for multiprocessing"""
    chunk_id, chunk_data, nonce, operation, algorithm, key = args[:6]
    tag = args[6] if len(args) > 6 else None
    
    if operation == 'encrypt':
        if algorithm == 'chacha20':
            if CRYPTO_AVAILABLE:
                cipher = ChaCha20.new(key=key, nonce=nonce)
                result = cipher.encrypt(chunk_data)
            else:
                # Fallback XOR
                key_repeated = (key * ((len(chunk_data) // len(key)) + 1))[:len(chunk_data)]
                result = bytes(a ^ b for a, b in zip(chunk_data, key_repeated))
            return chunk_id, result, None
        else:  # AES-GCM
            if CRYPTO_AVAILABLE:
                cipher = AES.new(key[:16], AES.MODE_GCM, nonce=nonce)
                ciphertext, tag = cipher.encrypt_and_digest(chunk_data)
                return chunk_id, ciphertext, tag
            else:
                key_repeated = (key * ((len(chunk_data) // len(key)) + 1))[:len(chunk_data)]
                result = bytes(a ^ b for a, b in zip(chunk_data, key_repeated))
                return chunk_id, result, b""
    else:  # decrypt
        if algorithm == 'chacha20':
            if CRYPTO_AVAILABLE:
                cipher = ChaCha20.new(key=key, nonce=nonce)
                result = cipher.decrypt(chunk_data)
            else:
                key_repeated = (key * ((len(chunk_data) // len(key)) + 1))[:len(chunk_data)]
                result = bytes(a ^ b for a, b in zip(chunk_data, key_repeated))
            return chunk_id, result, None
        else:  # AES-GCM
            if CRYPTO_AVAILABLE:
                cipher = AES.new(key[:16], AES.MODE_GCM, nonce=nonce)
                result = cipher.decrypt_and_verify(chunk_data, tag)
                return chunk_id, result, None
            else:
                key_repeated = (key * ((len(chunk_data) // len(key)) + 1))[:len(chunk_data)]
                result = bytes(a ^ b for a, b in zip(chunk_data, key_repeated))
                return chunk_id, result, None

@dataclass
class EncryptionResult:
    data: bytes
    iv_or_nonce: bytes
    tag: Optional[bytes] = None
    timing: float = 0.0

class IoTOptimizedCrypto:
    """
    IoT-optimized encryption system with multiple algorithms and processing modes
    """
    
    def __init__(self, password: str, algorithm='chacha20', mode='auto'):
        self.password = password
        self.algorithm = algorithm.lower()
        self.mode = mode  # 'sequential', 'threaded', 'multiprocess', 'auto'
        
        # IoT device detection and optimization (must be set before _derive_key)
        self.cpu_count = mp.cpu_count()
        self.is_low_power = self._detect_low_power_device()
        self.optimal_chunk_size = self._calculate_optimal_chunk_size()
        
        # Now derive key after device characteristics are set
        self.key = self._derive_key(password)
        
        print(f"Initialized for {self.cpu_count} cores, low-power: {self.is_low_power}")
    
    def _detect_low_power_device(self) -> bool:
        """Detect if running on low-power IoT device"""
        # Simple heuristics for IoT device detection
        if self.cpu_count <= 2:
            return True
        
        # Check available memory (basic approximation)
        try:
            import psutil
            memory_gb = psutil.virtual_memory().total / (1024**3)
            return memory_gb < 1.0  # Less than 1GB RAM
        except ImportError:
            # Fallback: assume low power if fewer cores
            return self.cpu_count <= 2
    
    def _calculate_optimal_chunk_size(self) -> int:
        """Calculate optimal chunk size based on device capabilities"""
        if self.is_low_power:
            return 1024  # 1KB chunks for low-power devices
        else:
            return 8192  # 8KB chunks for more powerful devices
    
    def _derive_key(self, password: str, salt: bytes = None) -> bytes:
        """Optimized key derivation using PBKDF2"""
        if salt is None:
            salt = b"IoTOptimizedSalt2024"  # In production, use random salt
        
        # Adaptive iterations based on device capability
        iterations = 1000 if self.is_low_power else 10000
        
        if self.algorithm == 'chacha20':
            return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, iterations, 32)
        else:  # AES
            return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, iterations, 32)
    
    def _chacha20_encrypt_chunk(self, data: bytes, nonce: bytes) -> bytes:
        """ChaCha20 encryption (faster than AES on many IoT devices)"""
        if CRYPTO_AVAILABLE:
            cipher = ChaCha20.new(key=self.key, nonce=nonce)
            return cipher.encrypt(data)
        else:
            # Fallback: simple XOR (NOT secure, for demo only)
            return self._simple_xor(data, self.key)
    
    def _chacha20_decrypt_chunk(self, data: bytes, nonce: bytes) -> bytes:
        """ChaCha20 decryption"""
        if CRYPTO_AVAILABLE:
            cipher = ChaCha20.new(key=self.key, nonce=nonce)
            return cipher.decrypt(data)
        else:
            return self._simple_xor(data, self.key)
    
    def _aes_gcm_encrypt_chunk(self, data: bytes, nonce: bytes) -> Tuple[bytes, bytes]:
        """AES-GCM encryption with authentication"""
        if CRYPTO_AVAILABLE:
            cipher = AES.new(self.key[:16], AES.MODE_GCM, nonce=nonce)
            ciphertext, tag = cipher.encrypt_and_digest(data)
            return ciphertext, tag
        else:
            return self._simple_xor(data, self.key), b""
    
    def _aes_gcm_decrypt_chunk(self, data: bytes, nonce: bytes, tag: bytes) -> bytes:
        """AES-GCM decryption with verification"""
        if CRYPTO_AVAILABLE:
            cipher = AES.new(self.key[:16], AES.MODE_GCM, nonce=nonce)
            return cipher.decrypt_and_verify(data, tag)
        else:
            return self._simple_xor(data, self.key)
    
    def _simple_xor(self, data: bytes, key: bytes) -> bytes:
        """Simple XOR for fallback (NOT cryptographically secure)"""
        key_repeated = (key * ((len(data) // len(key)) + 1))[:len(data)]
        return bytes(a ^ b for a, b in zip(data, key_repeated))
    
    def _process_chunk_worker(self, args) -> Tuple[int, bytes, Optional[bytes]]:
        """Worker function for parallel processing"""
        if len(args) == 4:
            chunk_id, chunk_data, nonce, operation = args
            tag = None
        else:
            chunk_id, chunk_data, nonce, operation, tag = args
        
        if operation == 'encrypt':
            if self.algorithm == 'chacha20':
                result = self._chacha20_encrypt_chunk(chunk_data, nonce)
                return chunk_id, result, None
            else:  # AES-GCM
                result, tag = self._aes_gcm_encrypt_chunk(chunk_data, nonce)
                return chunk_id, result, tag
        else:  # decrypt
            if self.algorithm == 'chacha20':
                result = self._chacha20_decrypt_chunk(chunk_data, nonce)
                return chunk_id, result, None
            else:  # AES-GCM
                result = self._aes_gcm_decrypt_chunk(chunk_data, nonce, tag)
                return chunk_id, result, None
    
    def encrypt(self, plaintext: str) -> EncryptionResult:
        """Main encryption function with adaptive processing"""
        start_time = time.time()
        data = plaintext.encode('utf-8')
        
        # Generate random nonce/IV
        if self.algorithm == 'chacha20':
            nonce = get_random_bytes(12) if CRYPTO_AVAILABLE else os.urandom(12)
        else:
            nonce = get_random_bytes(16) if CRYPTO_AVAILABLE else os.urandom(16)
        
        # Choose processing mode
        processing_mode = self._choose_processing_mode(len(data))
        
        if processing_mode == 'sequential' or len(data) < self.optimal_chunk_size:
            # Sequential processing for small data or low-power devices
            if self.algorithm == 'chacha20':
                encrypted_data = self._chacha20_encrypt_chunk(data, nonce)
                tag = None
            else:
                encrypted_data, tag = self._aes_gcm_encrypt_chunk(data, nonce)
        else:
            # Parallel processing for larger data
            encrypted_data, tag = self._parallel_process(data, nonce, 'encrypt', processing_mode)
        
        timing = time.time() - start_time
        return EncryptionResult(encrypted_data, nonce, tag, timing)
    
    def decrypt(self, result: EncryptionResult) -> str:
        """Main decryption function"""
        start_time = time.time()
        
        processing_mode = self._choose_processing_mode(len(result.data))
        
        if processing_mode == 'sequential' or len(result.data) < self.optimal_chunk_size:
            if self.algorithm == 'chacha20':
                decrypted_data = self._chacha20_decrypt_chunk(result.data, result.iv_or_nonce)
            else:
                decrypted_data = self._aes_gcm_decrypt_chunk(result.data, result.iv_or_nonce, result.tag)
        else:
            decrypted_data, _ = self._parallel_process(result.data, result.iv_or_nonce, 'decrypt', processing_mode, result.tag)
        
        timing = time.time() - start_time
        print(f"Decryption took: {timing:.4f}s")
        
        return decrypted_data.decode('utf-8')
    
    def _choose_processing_mode(self, data_size: int) -> str:
        """Intelligently choose processing mode based on data size and device capability"""
        if self.mode != 'auto':
            return self.mode
        
        # For very small data, always use sequential
        if data_size < 1024:
            return 'sequential'
        
        # For low-power devices, prefer sequential or light threading
        if self.is_low_power:
            return 'sequential' if data_size < 4096 else 'threaded'
        
        # For powerful devices with large data, use multiprocessing
        if data_size > 50000 and self.cpu_count > 2:
            return 'multiprocess'
        elif data_size > 8192:
            return 'threaded'
        else:
            return 'sequential'
    
    def _parallel_process(self, data: bytes, nonce: bytes, operation: str, 
                         mode: str, tag: bytes = None) -> Tuple[bytes, Optional[bytes]]:
        """Parallel processing with different execution modes"""
        
        # Split data into chunks
        chunk_size = self.optimal_chunk_size
        chunks = []
        for i in range(0, len(data), chunk_size):
            chunk = data[i:i + chunk_size]
            if chunk:
                # Create unique nonce for each chunk
                chunk_nonce = self._create_chunk_nonce(nonce, i // chunk_size)
                chunks.append((i // chunk_size, chunk, chunk_nonce, operation))
        
        if mode == 'multiprocess':
            return self._multiprocess_execution(chunks, tag)
        else:  # threaded
            return self._threaded_execution(chunks, tag)
    
    def _create_chunk_nonce(self, base_nonce: bytes, chunk_id: int) -> bytes:
        """Create unique nonce for each chunk"""
        # Combine base nonce with chunk ID
        chunk_bytes = struct.pack('<I', chunk_id)
        if len(base_nonce) == 12:  # ChaCha20
            return base_nonce[:8] + chunk_bytes
        else:  # AES (16 bytes)
            return base_nonce[:12] + chunk_bytes
    
    def _threaded_execution(self, chunks: List, tag: bytes = None) -> Tuple[bytes, Optional[bytes]]:
        """Execute using thread pool"""
        max_workers = min(len(chunks), self.cpu_count)
        results = {}
        combined_tag = b""
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(self._process_chunk_worker, chunk) for chunk in chunks]
            
            for future in futures:
                chunk_id, result, chunk_tag = future.result()
                results[chunk_id] = result
                if chunk_tag:
                    combined_tag += chunk_tag
        
        # Combine results in order
        combined_data = b''.join([results[i] for i in sorted(results.keys())])
        return combined_data, combined_tag if combined_tag else None
    
    def _multiprocess_execution(self, chunks: List, tag: bytes = None) -> Tuple[bytes, Optional[bytes]]:
        """Execute using process pool"""
        max_workers = min(len(chunks), self.cpu_count)
        results = {}
        combined_tag = b""
        
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(self._process_chunk_worker, chunk) for chunk in chunks]
            
            for future in futures:
                chunk_id, result, chunk_tag = future.result()
                results[chunk_id] = result
                if chunk_tag:
                    combined_tag += chunk_tag
        
        combined_data = b''.join([results[i] for i in sorted(results.keys())])
        return combined_data, combined_tag if combined_tag else None

# Benchmark and comparison functions
class CryptoBenchmark:
    """Benchmark different encryption methods"""
    
    @staticmethod
    def benchmark_algorithm(crypto_instance, test_data: str, iterations: int = 100):
        """Benchmark encryption/decryption performance"""
        total_encrypt_time = 0
        total_decrypt_time = 0
        
        for _ in range(iterations):
            # Encryption
            start = time.time()
            encrypted = crypto_instance.encrypt(test_data)
            total_encrypt_time += time.time() - start
            
            # Decryption  
            start = time.time()
            decrypted = crypto_instance.decrypt(encrypted)
            total_decrypt_time += time.time() - start
            
            # Verify correctness
            assert decrypted == test_data, "Decryption failed!"
        
        return {
            'avg_encrypt_time': total_encrypt_time / iterations,
            'avg_decrypt_time': total_decrypt_time / iterations,
            'total_time': (total_encrypt_time + total_decrypt_time) / iterations
        }
    
    @staticmethod
    def compare_algorithms(test_data: str, password: str):
        """Compare different algorithms and modes"""
        algorithms = ['chacha20', 'aes']
        modes = ['sequential', 'threaded', 'auto']
        
        results = {}
        
        for alg in algorithms:
            for mode in modes:
                print(f"\nTesting {alg.upper()} with {mode} mode...")
                crypto = IoTOptimizedCrypto(password, algorithm=alg, mode=mode)
                
                try:
                    benchmark = CryptoBenchmark.benchmark_algorithm(crypto, test_data, 10)
                    results[f"{alg}_{mode}"] = benchmark
                    print(f"  Average total time: {benchmark['total_time']:.4f}s")
                except Exception as e:
                    print(f"  Error: {e}")
                    continue
        
        return results

# Usage example and demonstration
def main():
    print("=== IoT Optimized Encryption System ===\n")
    
    # Test data of different sizes
    small_data = "Hello IoT World! This is a test message."
    medium_data = "A" * 10000  # 10KB
    large_data = "B" * 100000  # 100KB
    
    password = "IoTSecurePassword2024!"
    
    # Test with different data sizes
    test_cases = [
        ("Small data", small_data),
        ("Medium data (10KB)", medium_data),
        ("Large data (100KB)", large_data)
    ]
    
    for test_name, data in test_cases:
        print(f"\n{'='*50}")
        print(f"Testing with {test_name}")
        print(f"{'='*50}")
        
        # Test ChaCha20 (recommended for IoT)
        crypto_chacha = IoTOptimizedCrypto(password, algorithm='chacha20', mode='auto')
        
        print("\n--- ChaCha20 Encryption ---")
        result = crypto_chacha.encrypt(data)
        print(f"Encryption time: {result.timing:.4f}s")
        print(f"Data size: {len(data)} bytes -> {len(result.data)} bytes")
        
        decrypted = crypto_chacha.decrypt(result)
        print(f"Decryption successful: {decrypted[:50]}...")
        print(f"Data integrity: {'✓' if decrypted == data else '✗'}")
        
        # Performance comparison for medium data
        if test_name == "Medium data (10KB)":
            print(f"\n--- Performance Comparison ---")
            benchmark_results = CryptoBenchmark.compare_algorithms(data, password)
            
            print(f"\nResults summary:")
            for method, perf in benchmark_results.items():
                print(f"  {method:20}: {perf['total_time']:.4f}s")

if __name__ == "__main__":
    main()