import ucryptolib
import ubinascii
import os  # Changed from urandom
import _thread
import time
import uhashlib
# Removed unused RTC import

class ParallelAESCrypto:
    def __init__(self, password):
        self.key = self._derive_key(password)
        self.results = {}
        self.lock = _thread.allocate_lock()
        
    def _derive_key(self, password, iterations=1000):
        """Optimized key derivation function"""
        key = password.encode('utf-8')
        for _ in range(iterations):
            key = uhashlib.sha256(key).digest()
        return key[:16]  # AES-128

    def _process_chunk(self, data, iv, chunk_id, mode):
        """Parallel processing of each data chunk"""
        aes = ucryptolib.aes(self.key, 2, iv)  # CBC mode
        result = aes.encrypt(data) if mode == 'encrypt' else aes.decrypt(data)
        
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
                _thread.start_new_thread(
                    self._process_chunk,
                    (chunk, iv, i, mode)
                )
                threads.append(i)
        
        # Wait for all threads to complete
        start_time = time.ticks_ms()
        while len(self.results) < len(threads):
            if time.ticks_diff(time.ticks_ms(), start_time) > 5000:  # Timeout 5s
                raise TimeoutError("Parallel processing timed out")
            time.sleep(0.01)
        
        # Combine results
        return b''.join([self.results[i] for i in sorted(self.results.keys())])

    def encrypt(self, plaintext):
        """Parallel encryption"""
        iv = self._generate_iv()
        padded = self.pad(plaintext.encode('utf-8'))
        encrypted = self.parallel_process(padded, iv, 'encrypt', 2)
        return ubinascii.b2a_base64(iv + encrypted).decode('utf-8')

    def decrypt(self, ciphertext):
        """Parallel decryption"""
        data = ubinascii.a2b_base64(ciphertext)
        iv, encrypted = data[:16], data[16:]
        decrypted = self.parallel_process(encrypted, iv, 'decrypt', 2)
        return self.unpad(decrypted).decode('utf-8')

    def pad(self, s):
        """PKCS7 padding"""
        pad_size = 16 - (len(s) % 16)
        return s + bytes([pad_size] * pad_size)
    
    def unpad(self, s):
        """PKCS7 unpadding"""
        pad_size = s[-1]
        return s[:-pad_size]
    
    def _generate_iv(self):
        """Generate random IV using secure OS RNG"""
        return os.urandom(16)  # Fixed IV generation

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