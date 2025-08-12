import time
import base64
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding, serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from cryptography.hazmat.backends import default_backend
import matplotlib.pyplot as plt
import numpy as np
import threading
import requests
import json

class ProposedAlgorithm:
    """Your custom PPE (Proposed Parallel Encryption) algorithm"""
    
    def __init__(self):
        self.results = {'Left_Cipher': None, 'Right_Cipher': None, 'Left_Text': None, 'Right_Text': None}
        self.lock = threading.Lock()
    
    def calculate_time(self, func):
        """Decorator to calculate execution time"""
        def wrapper(*args, **kwargs):
            start_time = time.time() * 1000
            result = func(*args, **kwargs)
            end_time = time.time() * 1000
            execution_time = end_time - start_time
            return result, execution_time
        return wrapper
    
    def get_unix_time(self):
        """Get current unix timestamp"""
        try:
            # Fallback to local time since the original URL might not be accessible
            return str(int(time.time()))
        except Exception as e:
            return str(int(time.time()))
    
    def get_current_time_key(self, salt):
        """Generate time-based key"""
        keybase = ""
        key = ""
        unix_time = self.get_unix_time()
        timestep = int(unix_time)
        timestep8 = str(timestep)[:8]
        timestep8char = list(timestep8)
        
        keybase = timestep8
        # Build keybase with alternating patterns
        for _ in range(12):  # Simplified the repetitive loops
            for i in range(len(timestep8char) - 1, -1, -1):
                keybase += timestep8char[i]
            for i in range(len(timestep8char)):
                keybase += timestep8char[i]
        
        keybasechar = list(keybase)
        for i in range(0, len(keybasechar) // 2, 2):
            if i + 1 < len(keybasechar):
                num_a = keybasechar[i]
                num_b = keybasechar[i + 1]
                add_num = int(num_a + num_b)
                key_char = chr(add_num)
                key += key_char
        
        key = salt + key
        key = key[:16]
        result = base64.b64encode(key.encode()).decode()
        return result
    
    def pad(self, s):
        """Add PKCS7 padding"""
        pad_len = 16 - len(s) % 16
        return s + (chr(pad_len) * pad_len)
    
    def unpad(self, s):
        """Remove PKCS7 padding"""
        return s[:-ord(s[-1])]
    
    def remove_control_chars(self, input_str):
        """Remove control characters"""
        control_chars = [b'\x01', b'\x02', b'\x03', b'\x04', b'\x05', b'\x06', 
                        b'\x07', b'\x08', b'\x09', b'\x10', b'\x0a', b'\x0b', 
                        b'\x0c', b'\x0d', b'\x0e', b'\x0f']
        
        byte_data = input_str.encode('utf-8')
        for char in control_chars:
            byte_data = byte_data.replace(char, b'')
        
        return byte_data.decode('utf-8')
    
    def single_core_encrypt(self, data, key_str):
        """Single core AES encryption"""
        key_bytes = base64.b64decode(key_str)[:16]
        
        cipher = Cipher(algorithms.AES(key_bytes), modes.ECB(), backend=default_backend())
        encryptor = cipher.encryptor()
        
        padded_data = self.pad(data).encode('utf-8')
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        
        return base64.b64encode(ciphertext).decode('utf-8')
    
    def single_core_decrypt(self, enc_data, key_str):
        """Single core AES decryption"""
        key_bytes = base64.b64decode(key_str)[:16]
        
        cipher = Cipher(algorithms.AES(key_bytes), modes.ECB(), backend=default_backend())
        decryptor = cipher.decryptor()
        
        ciphertext = base64.b64decode(enc_data.encode('utf-8'))
        decrypted = decryptor.update(ciphertext) + decryptor.finalize()
        
        return decrypted.decode('utf-8').strip()
    
    def encrypt_left(self, data, key):
        """Encrypt left half"""
        result = self.single_core_encrypt(data, key)
        with self.lock:
            self.results['Left_Cipher'] = result
    
    def encrypt_right(self, data, key):
        """Encrypt right half"""
        result = self.single_core_encrypt(data, key)
        with self.lock:
            self.results['Right_Cipher'] = result
    
    def multi_core_encrypt(self, data, key_str):
        """Multi-threaded encryption"""
        # Reset results
        with self.lock:
            self.results['Left_Cipher'] = None
            self.results['Right_Cipher'] = None
        
        midpoint = len(data) // 2
        left_data = data[:midpoint]
        right_data = data[midpoint:]
        
        # Start threads
        left_thread = threading.Thread(target=self.encrypt_left, args=(left_data, key_str))
        right_thread = threading.Thread(target=self.encrypt_right, args=(right_data, key_str))
        
        left_thread.start()
        right_thread.start()
        
        left_thread.join()
        right_thread.join()
        
        # Combine results
        cipher = f"{self.results['Left_Cipher']}~|~{self.results['Right_Cipher']}"
        cipher = cipher.replace("\n", "").replace("\r", "")
        encoded_bytes = base64.b64encode(cipher.encode('utf-8'))
        return encoded_bytes.decode('utf-8')
    
    def decrypt_left(self, data, key):
        """Decrypt left half"""
        result = self.single_core_decrypt(data, key)
        with self.lock:
            self.results['Left_Text'] = result
    
    def decrypt_right(self, data, key):
        """Decrypt right half"""
        result = self.single_core_decrypt(data, key)
        with self.lock:
            self.results['Right_Text'] = result
    
    def multi_core_decrypt(self, data, key_str):
        """Multi-threaded decryption"""
        # Reset results
        with self.lock:
            self.results['Left_Text'] = None
            self.results['Right_Text'] = None
        
        ciphers = base64.b64decode(data).decode('utf-8')
        main_cipher = ciphers.split('~|~')
        
        # Start threads
        left_thread = threading.Thread(target=self.decrypt_left, args=(main_cipher[0], key_str))
        right_thread = threading.Thread(target=self.decrypt_right, args=(main_cipher[1], key_str))
        
        left_thread.start()
        right_thread.start()
        
        left_thread.join()
        right_thread.join()
        
        # Combine results
        left = self.remove_control_chars(self.results['Left_Text'])
        right = self.remove_control_chars(self.results['Right_Text'])
        return left + right
    
    def PPE(self, inp, salt):
        """Main encryption function"""
        key = base64.b64encode(self.get_current_time_key(salt).encode()).decode()
        return self.multi_core_encrypt(inp, key)
    
    def PPD(self, inp, salt):
        """Main decryption function"""
        key = base64.b64encode(self.get_current_time_key(salt).encode()).decode()
        return self.multi_core_decrypt(inp, key)

class StandardAES:
    """Standard AES encryption with fixed key"""
    
    def __init__(self, key="MyFixedAESKey123"):
        # Ensure key is 32 bytes for AES-256
        self.key = hashlib.sha256(key.encode()).digest()
    
    def calculate_time(self, func):
        """Decorator to calculate execution time"""
        def wrapper(*args, **kwargs):
            start_time = time.time() * 1000
            result = func(*args, **kwargs)
            end_time = time.time() * 1000
            execution_time = end_time - start_time
            return result, execution_time
        return wrapper
    
    def encrypt(self, data):
        """AES encryption"""
        # Add padding
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(data.encode()) + padder.finalize()
        
        # Encrypt
        cipher = Cipher(algorithms.AES(self.key), modes.ECB(), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        
        return base64.b64encode(ciphertext).decode()
    
    def decrypt(self, encrypted_data):
        """AES decryption"""
        # Decrypt
        ciphertext = base64.b64decode(encrypted_data)
        cipher = Cipher(algorithms.AES(self.key), modes.ECB(), backend=default_backend())
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(ciphertext) + decryptor.finalize()
        
        # Remove padding
        unpadder = padding.PKCS7(128).unpadder()
        data = unpadder.update(padded_data) + unpadder.finalize()
        
        return data.decode()

class StandardRSA:
    """Standard RSA encryption"""
    
    def __init__(self, key_size=2048):
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()
    
    def calculate_time(self, func):
        """Decorator to calculate execution time"""
        def wrapper(*args, **kwargs):
            start_time = time.time() * 1000
            result = func(*args, **kwargs)
            end_time = time.time() * 1000
            execution_time = end_time - start_time
            return result, execution_time
        return wrapper
    
    def encrypt(self, data):
        """RSA encryption (for small data chunks)"""
        # RSA can only encrypt small amounts of data, so we'll encrypt in chunks
        max_chunk_size = 190  # Safe size for 2048-bit key
        encrypted_chunks = []
        
        for i in range(0, len(data), max_chunk_size):
            chunk = data[i:i+max_chunk_size].encode()
            encrypted_chunk = self.public_key.encrypt(
                chunk,
                asym_padding.OAEP(
                    mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            encrypted_chunks.append(base64.b64encode(encrypted_chunk).decode())
        
        return "|".join(encrypted_chunks)
    
    def decrypt(self, encrypted_data):
        """RSA decryption"""
        encrypted_chunks = encrypted_data.split("|")
        decrypted_chunks = []
        
        for chunk in encrypted_chunks:
            encrypted_chunk = base64.b64decode(chunk)
            decrypted_chunk = self.private_key.decrypt(
                encrypted_chunk,
                asym_padding.OAEP(
                    mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            decrypted_chunks.append(decrypted_chunk.decode())
        
        return "".join(decrypted_chunks)

def benchmark_algorithms():
    """Benchmark all three algorithms with multiple iterations for accuracy"""
    
    # Test data - make it much longer for meaningful measurements
    test_data = "Hello world my name is reza, this is a longer test string for encryption benchmarking. " * 1000  # Much longer
    print(f"Test data length: {len(test_data)} characters")
    
    # Initialize algorithms
    proposed = ProposedAlgorithm()
    aes = StandardAES()
    rsa = StandardRSA()
    
    # Benchmark results
    results = {
        'Proposed': {'encrypt_time': 0, 'decrypt_time': 0, 'total_time': 0},
        'AES': {'encrypt_time': 0, 'decrypt_time': 0, 'total_time': 0},
        'RSA': {'encrypt_time': 0, 'decrypt_time': 0, 'total_time': 0}
    }
    
    print("Benchmarking encryption algorithms...")
    print("=" * 50)
    
    # Number of iterations for more accurate timing
    iterations = 100  # More iterations for better averaging
    
    # Test Proposed Algorithm
    print("Testing Proposed Algorithm...")
    encrypt_times = []
    decrypt_times = []
    
    for i in range(iterations):
        # Warm up run
        if i == 0:
            _ = proposed.PPE(test_data[:100], "reza")
        
        start_time = time.perf_counter_ns()  # Use nanoseconds for better precision
        enc_proposed = proposed.PPE(test_data, "reza")
        encrypt_time = (time.perf_counter_ns() - start_time) / 1_000_000  # Convert to milliseconds
        encrypt_times.append(encrypt_time)
        
        start_time = time.perf_counter_ns()
        dec_proposed = proposed.PPD(enc_proposed, "reza")
        decrypt_time = (time.perf_counter_ns() - start_time) / 1_000_000
        decrypt_times.append(decrypt_time)
        
        if i == 0:  # Verify correctness on first iteration
            print(f"Original length: {len(test_data)}, Decrypted length: {len(dec_proposed)}")
            success = test_data.strip() == dec_proposed.strip()
            print(f"Proposed decryption successful: {success}")
    
    results['Proposed']['encrypt_time'] = sum(encrypt_times) / len(encrypt_times)
    results['Proposed']['decrypt_time'] = sum(decrypt_times) / len(decrypt_times)
    results['Proposed']['total_time'] = results['Proposed']['encrypt_time'] + results['Proposed']['decrypt_time']
    
    print(f"Proposed - Avg Encrypt: {results['Proposed']['encrypt_time']:.4f}ms, Avg Decrypt: {results['Proposed']['decrypt_time']:.4f}ms")
    
    # Test Standard AES
    print("Testing Standard AES...")
    encrypt_times = []
    decrypt_times = []
    
    for i in range(iterations):
        # Warm up run
        if i == 0:
            _ = aes.encrypt(test_data[:100])
        
        start_time = time.perf_counter_ns()
        enc_aes = aes.encrypt(test_data)
        encrypt_time = (time.perf_counter_ns() - start_time) / 1_000_000
        encrypt_times.append(encrypt_time)
        
        start_time = time.perf_counter_ns()
        dec_aes = aes.decrypt(enc_aes)
        decrypt_time = (time.perf_counter_ns() - start_time) / 1_000_000
        decrypt_times.append(decrypt_time)
        
        if i == 0:  # Verify correctness on first iteration
            success = test_data == dec_aes
            print(f"AES decryption successful: {success}")
    
    results['AES']['encrypt_time'] = sum(encrypt_times) / len(encrypt_times)
    results['AES']['decrypt_time'] = sum(decrypt_times) / len(decrypt_times)
    results['AES']['total_time'] = results['AES']['encrypt_time'] + results['AES']['decrypt_time']
    
    print(f"AES - Avg Encrypt: {results['AES']['encrypt_time']:.4f}ms, Avg Decrypt: {results['AES']['decrypt_time']:.4f}ms")
    
    # Test Standard RSA
    print("Testing Standard RSA...")
    encrypt_times = []
    decrypt_times = []
    
    # Use shorter data for RSA due to size limitations
    rsa_test_data = test_data[:1000]  # RSA is slow with large data
    rsa_iterations = 10  # Fewer iterations for RSA as it's much slower
    
    for i in range(rsa_iterations):
        start_time = time.perf_counter_ns()
        enc_rsa = rsa.encrypt(rsa_test_data)
        encrypt_time = (time.perf_counter_ns() - start_time) / 1_000_000
        encrypt_times.append(encrypt_time)
        
        start_time = time.perf_counter_ns()
        dec_rsa = rsa.decrypt(enc_rsa)
        decrypt_time = (time.perf_counter_ns() - start_time) / 1_000_000
        decrypt_times.append(decrypt_time)
        
        if i == 0:  # Verify correctness on first iteration
            success = rsa_test_data == dec_rsa
            print(f"RSA decryption successful: {success}")
    
    results['RSA']['encrypt_time'] = sum(encrypt_times) / len(encrypt_times)
    results['RSA']['decrypt_time'] = sum(decrypt_times) / len(decrypt_times)
    results['RSA']['total_time'] = results['RSA']['encrypt_time'] + results['RSA']['decrypt_time']
    
    print(f"RSA - Avg Encrypt: {results['RSA']['encrypt_time']:.4f}ms, Avg Decrypt: {results['RSA']['decrypt_time']:.4f}ms")
    
    return results

def create_comparison_chart(results):
    """Create bar chart comparing the algorithms"""
    
    algorithms = list(results.keys())
    encrypt_times = [results[alg]['encrypt_time'] for alg in algorithms]
    decrypt_times = [results[alg]['decrypt_time'] for alg in algorithms]
    total_times = [results[alg]['total_time'] for alg in algorithms]
    
    # Set up the figure and axes
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
    
    # Colors for each algorithm
    colors = ['#4CAF50', '#2196F3', '#FF5722']  # Green, Blue, Red
    
    # Chart 1: Encryption Time
    bars1 = ax1.bar(algorithms, encrypt_times, color=colors, alpha=0.7)
    ax1.set_title('Encryption Time Comparison', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Time (milliseconds)')
    ax1.grid(True, alpha=0.3)
    
    # Add value labels on bars
    for bar, time in zip(bars1, encrypt_times):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + max(encrypt_times)*0.02,
                f'{time:.4f}ms', ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    # Chart 2: Decryption Time
    bars2 = ax2.bar(algorithms, decrypt_times, color=colors, alpha=0.7)
    ax2.set_title('Decryption Time Comparison', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Time (milliseconds)')
    ax2.grid(True, alpha=0.3)
    
    # Add value labels on bars
    for bar, time in zip(bars2, decrypt_times):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + max(decrypt_times)*0.02,
                f'{time:.4f}ms', ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    # Chart 3: Total Time
    bars3 = ax3.bar(algorithms, total_times, color=colors, alpha=0.7)
    ax3.set_title('Total Time Comparison', fontsize=14, fontweight='bold')
    ax3.set_ylabel('Time (milliseconds)')
    ax3.grid(True, alpha=0.3)
    
    # Add value labels on bars
    for bar, time in zip(bars3, total_times):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + max(total_times)*0.02,
                f'{time:.4f}ms', ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    plt.tight_layout()
    plt.show()
    
    # Create a single comprehensive chart
    fig2, ax = plt.subplots(figsize=(12, 8))
    
    x = np.arange(len(algorithms))
    width = 0.25
    
    bars1 = ax.bar(x - width, encrypt_times, width, label='Encryption', color='#4CAF50', alpha=0.8)
    bars2 = ax.bar(x, decrypt_times, width, label='Decryption', color='#2196F3', alpha=0.8)
    bars3 = ax.bar(x + width, total_times, width, label='Total', color='#FF5722', alpha=0.8)
    
    ax.set_xlabel('Algorithms', fontsize=12, fontweight='bold')
    ax.set_ylabel('Time (milliseconds)', fontsize=12, fontweight='bold')
    ax.set_title('Encryption Algorithms Performance Comparison', fontsize=16, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(algorithms)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Add value labels on bars
    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + height*0.02,
                    f'{height:.2f}', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Run benchmark
    benchmark_results = benchmark_algorithms()
    
    # Display results
    print("\n" + "=" * 50)
    print("BENCHMARK RESULTS")
    print("=" * 50)
    
    for alg_name, times in benchmark_results.items():
        print(f"\n{alg_name}:")
        print(f"  Encryption Time: {times['encrypt_time']:.4f} ms")
        print(f"  Decryption Time: {times['decrypt_time']:.4f} ms")
        print(f"  Total Time: {times['total_time']:.4f} ms")
    
    # Create visualization
    create_comparison_chart(benchmark_results)
    
    # Performance analysis
    print("\n" + "=" * 50)
    print("PERFORMANCE ANALYSIS")
    print("=" * 50)
    
    fastest_encrypt = min(benchmark_results.items(), key=lambda x: x[1]['encrypt_time'])
    fastest_decrypt = min(benchmark_results.items(), key=lambda x: x[1]['decrypt_time'])
    fastest_total = min(benchmark_results.items(), key=lambda x: x[1]['total_time'])
    
    print(f"Fastest Encryption: {fastest_encrypt[0]} ({fastest_encrypt[1]['encrypt_time']:.3f} ms)")
    print(f"Fastest Decryption: {fastest_decrypt[0]} ({fastest_decrypt[1]['decrypt_time']:.3f} ms)")
    print(f"Fastest Overall: {fastest_total[0]} ({fastest_total[1]['total_time']:.3f} ms)")