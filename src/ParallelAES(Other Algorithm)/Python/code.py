import base64
import os
import threading
import time
import hashlib
from Crypto.Cipher import AES

class ParallelAESCrypto:
    def __init__(self, password):
        self.key = self._derive_key(password)
        self.results = {}
        self.lock = threading.Lock()
        
    def _derive_key(self, password, iterations=1000):
        """Optimized key derivation function"""
        key = password.encode('utf-8')
        for _ in range(iterations):
            key = hashlib.sha256(key).digest()
        return key[:16]  # AES-128

    def _process_chunk(self, data, iv, chunk_id, mode):
        """Parallel processing of each data chunk"""
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        result = cipher.encrypt(data) if mode == 'encrypt' else cipher.decrypt(data)
        
        with self.lock:
            self.results[chunk_id] = result

    def parallel_process(self, data, iv, mode='encrypt', chunks=2):
        """Manage parallel processing"""
        self.results = {}
        chunk_size = (len(data) + chunks - 1) // chunks
        threads = []
        
        # Create threads for each chunk
        for i in range(chunks):
            start = i * chunk_size
            end = start + chunk_size
            chunk = data[start:end]
            if chunk:
                # Ensure chunk size is multiple of 16 (AES block size)
                if len(chunk) % 16 != 0:
                    # Only pad for encryption (decryption should already be padded)
                    if mode == 'encrypt':
                        chunk = self.pad(chunk)
                t = threading.Thread(
                    target=self._process_chunk,
                    args=(chunk, iv, i, mode)
                )
                t.start()
                threads.append(t)
        
        # Wait for all threads to complete
        start_time = time.time()
        for t in threads:
            t.join(timeout=5)  # Timeout 5 seconds per thread
            if time.time() - start_time > 5:
                raise TimeoutError("Parallel processing timed out")
        
        # Combine results in order
        return b''.join([self.results[i] for i in sorted(self.results.keys())])

    def encrypt(self, plaintext):
        """Parallel encryption"""
        iv = self._generate_iv()
        padded = self.pad(plaintext.encode('utf-8'))
        encrypted = self.parallel_process(padded, iv, 'encrypt', 2)
        return base64.b64encode(iv + encrypted).decode('utf-8')

    def decrypt(self, ciphertext):
        """Parallel decryption"""
        data = base64.b64decode(ciphertext)
        iv, encrypted = data[:16], data[16:]
        decrypted = self.parallel_process(encrypted, iv, 'decrypt', 2)
        return self.unpad(decrypted).decode('utf-8')

    @staticmethod
    def pad(s):
        """PKCS7 padding"""
        pad_size = 16 - (len(s) % 16)
        return s + bytes([pad_size] * pad_size)
    
    @staticmethod
    def unpad(s):
        """PKCS7 unpadding"""
        pad_size = s[-1]
        if pad_size > 16 or pad_size < 1:  # Validate padding size
            raise ValueError("Invalid padding")
        return s[:-pad_size]
    
    @staticmethod
    def _generate_iv():
        """Generate random IV using secure OS RNG"""
        return os.urandom(16)  # 16 bytes for AES IV

# Usage Example
if __name__ == "__main__":
    crypto = ParallelAESCrypto("SecurePassword123")
    
    text = "This is a secret message"
    print("Original:", text)
    
    encrypted = crypto.encrypt(text)
    print("\nEncrypted:", encrypted)
    
    decrypted = crypto.decrypt(encrypted)
    print("\nDecrypted:", decrypted)
    
    print("\nVerification:", text == decrypted)