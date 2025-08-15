import time
import hashlib
import threading
import psutil
import gc
from memory_profiler import profile
import sys
import os
import matplotlib.pyplot as plt
import numpy as np
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
import base64

class ESP32Simulator:
    """
    Accurate ESP32 simulator on powerful system
    Applies real ESP32 limitations
    """
    
    def __init__(self):
        # Real ESP32 specifications
        self.ESP32_CPU_FREQ = 240_000_000  # 240 MHz
        self.YOUR_CPU_FREQ = 3_600_000_000  # Estimated i7-13650HX base clock
        self.SLOWDOWN_FACTOR = self.YOUR_CPU_FREQ / self.ESP32_CPU_FREQ  # ~15x
        
        # ESP32 memory limitations
        self.MAX_HEAP_SIZE = 300 * 1024  # 300KB usable from 520KB
        self.MAX_CHUNK_SIZE = 4 * 1024   # 4KB maximum chunk
        self.MAX_STACK_SIZE = 8 * 1024   # 8KB stack
        
        # Processing limitations
        self.SINGLE_CORE_ONLY = True
        self.LIMITED_OPERATIONS = True
        
        print(f"ESP32 Simulator initialized:")
        print(f"  CPU Slowdown Factor: {self.SLOWDOWN_FACTOR:.1f}x")
        print(f"  Max Heap: {self.MAX_HEAP_SIZE:,} bytes")
        print(f"  Max Chunk: {self.MAX_CHUNK_SIZE:,} bytes")
        print()
    
    def simulate_cpu_slowdown(self, operation_time):
        """Simulate CPU slowdown with busy-wait"""
        if operation_time > 0:
            # محاسبه زمان انتظار برای شبیه‌سازی کندی
            delay = operation_time * (self.SLOWDOWN_FACTOR - 1) / self.SLOWDOWN_FACTOR
            time.sleep(delay)
    
    def check_memory_limit(self, data_size):
        """Check memory limitations"""
        if data_size > self.MAX_HEAP_SIZE:
            raise MemoryError(f"Data size {data_size} exceeds ESP32 heap limit {self.MAX_HEAP_SIZE}")
        
        # شبیه‌سازی فشار حافظه
        if data_size > self.MAX_HEAP_SIZE * 0.8:
            print(f"⚠️  Memory pressure: {data_size:,}/{self.MAX_HEAP_SIZE:,} bytes")
    
    def simulate_memory_fragmentation(self):
        """Simulate ESP32 memory fragmentation"""
        # ESP32 اغلب با fragmentation مشکل دارد
        time.sleep(0.001)  # تأخیر کوچک برای allocation
        gc.collect()  # garbage collection مانند ESP32

class ESP32CryptoSimulator:
    """ESP32 encryption algorithms simulator"""
    
    def __init__(self):
        self.simulator = ESP32Simulator()
        
    def get_current_time_key(self, salt):
        """Generate key based on time - ESP32 version"""
        start_time = time.perf_counter()
        
        # شبیه‌سازی عملیات کند ESP32
        unix_time = str(int(time.time()))
        timestep = int(unix_time)
        timestep8 = str(timestep)[:8]
        timestep8char = list(timestep8)
        
        # تکرار کمتر برای محدودیت حافظه ESP32
        keybase = timestep8
        for i in range(4):  # کمتر از 8 در کد اصلی
            keybase += ''.join(reversed(timestep8char))
            keybase += ''.join(timestep8char)
            
            # شبیه‌سازی کندی ESP32
            self.simulator.simulate_cpu_slowdown(0.0001)
        
        # تولید کلید نهایی
        key = ""
        keybasechar = list(keybase)
        for i in range(0, len(keybasechar) - 1, 2):
            if i + 1 < len(keybasechar):
                try:
                    add_num = int(keybasechar[i] + keybasechar[i + 1])
                    key_char = chr(add_num % 94 + 33)
                    key += key_char
                except:
                    key += 'X'
            
            # شبیه‌سازی کندی محاسبات
            self.simulator.simulate_cpu_slowdown(0.00001)
        
        key = (salt + key)[:16].ljust(16, '0')
        
        operation_time = time.perf_counter() - start_time
        self.simulator.simulate_cpu_slowdown(operation_time)
        
        return key.encode('utf-8')
    
    def simple_PPE_encrypt(self, data, key):
        """Simple PPE encryption like ESP32"""
        start_time = time.perf_counter()
        
        # بررسی محدودیت حافظه
        data_bytes = data.encode('utf-8')
        self.simulator.check_memory_limit(len(data_bytes) * 3)  # تخمین استفاده حافظه
        
        key_bytes = key[:16]
        result = bytearray()
        
        # شبیه‌سازی پردازش byte-by-byte ESP32
        for i, byte in enumerate(data_bytes):
            result.append(byte ^ key_bytes[i % len(key_bytes)])
            
            # هر 100 byte یک تأخیر کوچک (شبیه‌سازی محدودیت ESP32)
            if i % 100 == 0:
                self.simulator.simulate_cpu_slowdown(0.0001)
        
        operation_time = time.perf_counter() - start_time
        self.simulator.simulate_cpu_slowdown(operation_time)
        
        # شبیه‌سازی memory fragmentation
        self.simulator.simulate_memory_fragmentation()
        
        return result.hex()
    
    def simple_PPE_decrypt(self, hex_data, key):
        """Simple PPE decryption"""
        start_time = time.perf_counter()
        
        try:
            encrypted_bytes = bytes.fromhex(hex_data)
            self.simulator.check_memory_limit(len(encrypted_bytes) * 2)
            
            key_bytes = key[:16]
            result = bytearray()
            
            for i, byte in enumerate(encrypted_bytes):
                result.append(byte ^ key_bytes[i % len(key_bytes)])
                
                # شبیه‌سازی کندی
                if i % 100 == 0:
                    self.simulator.simulate_cpu_slowdown(0.0001)
            
            operation_time = time.perf_counter() - start_time
            self.simulator.simulate_cpu_slowdown(operation_time)
            
            return result.decode('utf-8')
        except Exception as e:
            return f"Decryption failed: {str(e)}"
    
    def aes_encrypt(self, data, key):
        """AES encryption - ESP32 optimized version"""
        start_time = time.perf_counter()
        
        try:
            # بررسی محدودیت حافظه
            data_bytes = data.encode('utf-8')
            self.simulator.check_memory_limit(len(data_bytes) * 4)  # AES needs more memory
            
            # Pad data to 16-byte blocks
            padding_length = 16 - (len(data_bytes) % 16)
            padded_data = data_bytes + bytes([padding_length] * padding_length)
            
            # Create AES cipher
            cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
            encryptor = cipher.encryptor()
            
            # Process in chunks (ESP32 limitation)
            result = bytearray()
            chunk_size = 1024  # 1KB chunks for ESP32
            
            for i in range(0, len(padded_data), chunk_size):
                chunk = padded_data[i:i + chunk_size]
                encrypted_chunk = encryptor.update(chunk)
                result.extend(encrypted_chunk)
                
                # شبیه‌سازی کندی ESP32 برای AES
                self.simulator.simulate_cpu_slowdown(0.001)
            
            final_chunk = encryptor.finalize()
            result.extend(final_chunk)
            
            operation_time = time.perf_counter() - start_time
            self.simulator.simulate_cpu_slowdown(operation_time * 2)  # AES is slower on ESP32
            
            return base64.b64encode(bytes(result)).decode('utf-8')
            
        except Exception as e:
            return f"AES encryption failed: {str(e)}"
    
    def aes_decrypt(self, encrypted_data, key):
        """AES decryption - ESP32 optimized version"""
        start_time = time.perf_counter()
        
        try:
            encrypted_bytes = base64.b64decode(encrypted_data.encode('utf-8'))
            self.simulator.check_memory_limit(len(encrypted_bytes) * 3)
            
            # Create AES cipher
            cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
            decryptor = cipher.decryptor()
            
            # Process in chunks
            result = bytearray()
            chunk_size = 1024
            
            for i in range(0, len(encrypted_bytes), chunk_size):
                chunk = encrypted_bytes[i:i + chunk_size]
                decrypted_chunk = decryptor.update(chunk)
                result.extend(decrypted_chunk)
                
                # شبیه‌سازی کندی
                self.simulator.simulate_cpu_slowdown(0.001)
            
            final_chunk = decryptor.finalize()
            result.extend(final_chunk)
            
            # Remove padding
            padding_length = result[-1]
            result = result[:-padding_length]
            
            operation_time = time.perf_counter() - start_time
            self.simulator.simulate_cpu_slowdown(operation_time * 2)
            
            return result.decode('utf-8')
            
        except Exception as e:
            return f"AES decryption failed: {str(e)}"
    
    def rsa_encrypt(self, data, public_key):
        """RSA encryption - ESP32 optimized version"""
        start_time = time.perf_counter()
        
        try:
            data_bytes = data.encode('utf-8')
            self.simulator.check_memory_limit(len(data_bytes) * 10)  # RSA needs much more memory
            
            # RSA can only encrypt small chunks
            max_chunk_size = 190  # For 2048-bit RSA
            result_parts = []
            
            for i in range(0, len(data_bytes), max_chunk_size):
                chunk = data_bytes[i:i + max_chunk_size]
                
                # Encrypt chunk
                encrypted_chunk = public_key.encrypt(
                    chunk,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
                
                result_parts.append(base64.b64encode(encrypted_chunk).decode('utf-8'))
                
                # شبیه‌سازی کندی شدید ESP32 برای RSA
                self.simulator.simulate_cpu_slowdown(0.01)
            
            operation_time = time.perf_counter() - start_time
            self.simulator.simulate_cpu_slowdown(operation_time * 5)  # RSA is very slow on ESP32
            
            return "|".join(result_parts)
            
        except Exception as e:
            return f"RSA encryption failed: {str(e)}"
    
    def rsa_decrypt(self, encrypted_data, private_key):
        """RSA decryption - ESP32 optimized version"""
        start_time = time.perf_counter()
        
        try:
            encrypted_parts = encrypted_data.split("|")
            result_parts = []
            
            for part in encrypted_parts:
                encrypted_chunk = base64.b64decode(part.encode('utf-8'))
                
                # Decrypt chunk
                decrypted_chunk = private_key.decrypt(
                    encrypted_chunk,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
                
                result_parts.append(decrypted_chunk)
                
                # شبیه‌سازی کندی شدید
                self.simulator.simulate_cpu_slowdown(0.01)
            
            operation_time = time.perf_counter() - start_time
            self.simulator.simulate_cpu_slowdown(operation_time * 5)
            
            return b''.join(result_parts).decode('utf-8')
            
        except Exception as e:
            return f"RSA decryption failed: {str(e)}"
    
    def chunked_process(self, data, salt, algorithm="PPE", encrypt=True):
        """Chunked processing like ESP32"""
        key = self.get_current_time_key(salt)
        
        # تقسیم به چانک‌های کوچک ESP32
        chunk_size = min(self.simulator.MAX_CHUNK_SIZE, len(data.encode('utf-8')))
        
        if len(data.encode('utf-8')) <= chunk_size:
            # داده کوچک - پردازش یکجا
            if algorithm == "PPE":
                if encrypt:
                    return self.simple_PPE_encrypt(data, key)
                else:
                    return self.simple_PPE_decrypt(data, key)
            elif algorithm == "aes":
                if encrypt:
                    return self.aes_encrypt(data, key)
                else:
                    return self.aes_decrypt(data, key)
            elif algorithm == "rsa":
                # Generate RSA keys for this operation
                private_key = rsa.generate_private_key(
                    public_exponent=65537,
                    key_size=2048,
                    backend=default_backend()
                )
                public_key = private_key.public_key()
                
                if encrypt:
                    return self.rsa_encrypt(data, public_key), private_key
                else:
                    return self.rsa_decrypt(data, private_key)
        else:
            # داده بزرگ - پردازش تکه‌ای
            result_parts = []
            
            if algorithm == "PPE":
                if encrypt:
                    for i in range(0, len(data), chunk_size):
                        chunk = data[i:i + chunk_size]
                        encrypted_chunk = self.simple_PPE_encrypt(chunk, key)
                        result_parts.append(encrypted_chunk)
                        
                        # شبیه‌سازی تأخیر بین چانک‌ها
                        self.simulator.simulate_cpu_slowdown(0.001)
                    
                    return "|".join(result_parts)
                else:
                    # رمزگشایی چانک‌ها
                    chunks = data.split("|")
                    for chunk in chunks:
                        if chunk:
                            decrypted_chunk = self.simple_PPE_decrypt(chunk, key)
                            result_parts.append(decrypted_chunk)
                            self.simulator.simulate_cpu_slowdown(0.001)
                    
                    return "".join(result_parts)
            elif algorithm == "aes":
                if encrypt:
                    for i in range(0, len(data), chunk_size):
                        chunk = data[i:i + chunk_size]
                        encrypted_chunk = self.aes_encrypt(chunk, key)
                        result_parts.append(encrypted_chunk)
                        self.simulator.simulate_cpu_slowdown(0.002)
                    
                    return "|".join(result_parts)
                else:
                    chunks = data.split("|")
                    for chunk in chunks:
                        if chunk:
                            decrypted_chunk = self.aes_decrypt(chunk, key)
                            result_parts.append(decrypted_chunk)
                            self.simulator.simulate_cpu_slowdown(0.002)
                    
                    return "".join(result_parts)
            elif algorithm == "rsa":
                # RSA is not suitable for large data on ESP32
                return f"RSA not suitable for data size {len(data)} bytes"
    
    def encrypt(self, data, salt, algorithm="PPE"):
        """Main encryption function"""
        if algorithm == "rsa":
            encrypted, private_key = self.chunked_process(data, salt, algorithm, encrypt=True)
            return encrypted, private_key
        else:
            encrypted = self.chunked_process(data, salt, algorithm, encrypt=True)
            key = self.get_current_time_key(salt)
            return encrypted, key.hex()
    
    def decrypt(self, encrypted_data, salt, algorithm="PPE", key=None):
        """Main decryption function"""
        if algorithm == "rsa":
            return self.chunked_process(encrypted_data, salt, algorithm, encrypt=False)
        else:
            return self.chunked_process(encrypted_data, salt, algorithm, encrypt=False)

def esp32_algorithm_benchmark():
    """Compare PPE, AES, and RSA algorithms on ESP32"""
    
    # داده‌های آزمایشی مناسب ESP32
    test_cases = [
        ("ESP32 Tiny (32B)", "Hello ESP32 World!"),
        ("ESP32 Small (128B)", "This is a realistic ESP32 test with moderate length data for encryption testing purposes."),
        ("ESP32 Medium (512B)", "ESP32 medium size test data. " + "Testing ESP32 encryption with realistic data size. " * 8),
        ("ESP32 Large (2KB)", "ESP32 large test. " + "This simulates larger data processing on ESP32 microcontroller. " * 40),
    ]
    
    algorithms = ["PPE", "aes", "rsa"]
    crypto_sim = ESP32CryptoSimulator()
    results = {}
    salt = "esp32test"
    iterations = 3  # کم برای شبیه‌سازی ESP32
    
    print("🔧 ESP32 Algorithm Comparison Simulation")
    print("="*70)
    print(f"Target Device: ESP32 (240MHz, 520KB RAM)")
    print(f"Host System: i7-13650HX (16GB DDR5)")
    print(f"Algorithms: PPE, AES-128, RSA-2048")
    print(f"Simulation Method: CPU slowdown + Memory limits")
    print()
    
    for size_name, test_data in test_cases:
        print(f"📊 Testing {size_name}")
        print(f"   Data size: {len(test_data.encode('utf-8')):,} bytes")
        
        results[size_name] = {}
        
        for algorithm in algorithms:
            print(f"   🔐 Testing {algorithm.upper()} algorithm...")
            
            # بررسی محدودیت حافظه
            try:
                memory_multiplier = 3 if algorithm == "PPE" else (4 if algorithm == "aes" else 10)
                crypto_sim.simulator.check_memory_limit(len(test_data.encode('utf-8')) * memory_multiplier)
            except MemoryError as e:
                print(f"      ❌ {e}")
                results[size_name][algorithm] = None
                continue
            
            encrypt_times = []
            decrypt_times = []
            key_gen_times = []
            memory_usage = []
            success_count = 0
            
            for iteration in range(iterations):
                try:
                    # تست تولید کلید
                    start_time = time.perf_counter()
                    if algorithm == "rsa":
                        # RSA key generation is very slow on ESP32
                        private_key = rsa.generate_private_key(
                            public_exponent=65537,
                            key_size=2048,
                            backend=default_backend()
                        )
                        public_key = private_key.public_key()
                        key_gen_time = (time.perf_counter() - start_time) * 1000
                        crypto_sim.simulator.simulate_cpu_slowdown(key_gen_time / 1000 * 10)  # Very slow on ESP32
                    else:
                        key = crypto_sim.get_current_time_key(salt)
                        key_gen_time = (time.perf_counter() - start_time) * 1000
                    
                    key_gen_times.append(key_gen_time)
                    
                    # تست رمزنگاری
                    start_time = time.perf_counter()
                    if algorithm == "rsa":
                        encrypted, private_key = crypto_sim.encrypt(test_data, salt, algorithm)
                    else:
                        encrypted, key_hex = crypto_sim.encrypt(test_data, salt, algorithm)
                    encrypt_time = (time.perf_counter() - start_time) * 1000
                    encrypt_times.append(encrypt_time)
                    
                    # برآورد استفاده حافظه
                    if algorithm == "rsa":
                        memory_usage.append(len(encrypted) + len(test_data) * 10)
                    else:
                        memory_usage.append(len(encrypted) + len(key_hex) + len(test_data))
                    
                    # تست رمزگشایی
                    start_time = time.perf_counter()
                    if algorithm == "rsa":
                        decrypted = crypto_sim.decrypt(encrypted, salt, algorithm, private_key)
                    else:
                        decrypted = crypto_sim.decrypt(encrypted, salt, algorithm)
                    decrypt_time = (time.perf_counter() - start_time) * 1000
                    decrypt_times.append(decrypt_time)
                    
                    # بررسی صحت
                    if test_data.strip() == decrypted.strip():
                        success_count += 1
                        print(f"      ✅ Iteration {iteration + 1}: OK")
                    else:
                        print(f"      ❌ Iteration {iteration + 1}: Data mismatch")
                    
                except Exception as e:
                    print(f"      ❌ Iteration {iteration + 1}: Error - {str(e)}")
                    continue
            
            if encrypt_times and decrypt_times:
                avg_encrypt = sum(encrypt_times) / len(encrypt_times)
                avg_decrypt = sum(decrypt_times) / len(decrypt_times)
                avg_key_gen = sum(key_gen_times) / len(key_gen_times)
                avg_memory = sum(memory_usage) / len(memory_usage)
                total_time = avg_encrypt + avg_decrypt + avg_key_gen
                
                results[size_name][algorithm] = {
                    'encrypt_time': avg_encrypt,
                    'decrypt_time': avg_decrypt, 
                    'key_gen_time': avg_key_gen,
                    'total_time': total_time,
                    'memory_usage': avg_memory,
                    'success_rate': (success_count / iterations) * 100
                }
                
                # نمایش نتایج
                print(f"      📈 {algorithm.upper()} Results:")
                print(f"         Key Generation: {avg_key_gen:.1f} ms")
                print(f"         Encryption: {avg_encrypt:.1f} ms") 
                print(f"         Decryption: {avg_decrypt:.1f} ms")
                print(f"         Total Time: {total_time:.1f} ms")
                print(f"         Memory Usage: {avg_memory:,.0f} bytes")
                print(f"         Success Rate: {results[size_name][algorithm]['success_rate']:.0f}%")
                
                # تحلیل عملکرد
                if total_time < 50:
                    performance = "🚀 Excellent"
                elif total_time < 200:
                    performance = "✅ Good"
                elif total_time < 500:
                    performance = "⚠️  Acceptable"  
                else:
                    performance = "❌ Slow"
                
                print(f"         Performance: {performance}")
            else:
                results[size_name][algorithm] = None
        
        print("-" * 50)
    
    return results

def print_algorithm_analysis(results):
    """Comprehensive analysis of algorithm comparison"""
    
    print("\n" + "="*70)
    print("🎯 ESP32 ALGORITHM COMPARISON ANALYSIS")
    print("="*70)
    
    algorithms = ["PPE", "aes", "rsa"]
    algorithm_names = {"PPE": "PPE", "aes": "AES-128", "rsa": "RSA-2048"}
    
    print("\n📊 ALGORITHM PERFORMANCE SUMMARY:")
    print("-" * 50)
    
    for algorithm in algorithms:
        print(f"\n🔸 {algorithm_names[algorithm]}")
        total_times = []
        memory_usages = []
        success_rates = []
        
        for size_name, algo_results in results.items():
            if algo_results and algorithm in algo_results and algo_results[algorithm]:
                total_times.append(algo_results[algorithm]['total_time'])
                memory_usages.append(algo_results[algorithm]['memory_usage'])
                success_rates.append(algo_results[algorithm]['success_rate'])
        
        if total_times:
            avg_time = sum(total_times) / len(total_times)
            avg_memory = sum(memory_usages) / len(memory_usages)
            avg_success = sum(success_rates) / len(success_rates)
            
            print(f"   Average Total Time: {avg_time:.1f} ms")
            print(f"   Average Memory Usage: {avg_memory:,.0f} bytes")
            print(f"   Average Success Rate: {avg_success:.0f}%")
            
            # توصیه‌ها
            if algorithm == "PPE":
                if avg_time < 100:
                    print(f"   ✅ Excellent for ESP32 - Fast and efficient")
                else:
                    print(f"   ⚠️  Acceptable but could be optimized")
            elif algorithm == "aes":
                if avg_time < 500:
                    print(f"   ✅ Good balance of security and performance")
                else:
                    print(f"   ⚠️  May be too slow for real-time applications")
            elif algorithm == "rsa":
                if avg_time < 2000:
                    print(f"   ⚠️  Very slow but secure - use only when necessary")
                else:
                    print(f"   ❌ Too slow for most ESP32 applications")
    
    print(f"\n🎯 ESP32 ALGORITHM RECOMMENDATIONS:")
    print("-" * 50)
    print("1. 🔓 PPE: Use for speed-critical applications with basic security needs")
    print("2. 🔐 AES: Use for balanced security and performance requirements")
    print("3. 🛡️  RSA: Use only for key exchange or small critical data")
    print("4. 📦 Keep data chunks under 1KB for optimal performance")
    print("5. 🧠 Monitor memory usage - RSA uses 10x more memory")
    print("6. ⚡ Consider hybrid approach: RSA for keys, AES for data")
    
    print(f"\n🔍 EXPECTED REAL ESP32 PERFORMANCE:")
    print("-" * 50)
    print("• PPE (32-128B): 10-50 ms")
    print("• AES (32-128B): 50-200 ms")  
    print("• RSA (32-128B): 500-2000 ms")
    print("• Memory efficiency: PPE < AES < RSA")
    print("• Security level: PPE < AES < RSA")

def plot_algorithm_comparison_charts(results):
    """Create comparison charts for all algorithms"""
    
    algorithms = ["PPE", "aes", "rsa"]
    algorithm_names = {"PPE": "PPE", "aes": "AES-128", "rsa": "RSA-2048"}
    colors = {"PPE": "skyblue", "aes": "lightgreen", "rsa": "lightcoral"}
    
    # Prepare data
    sizes = []
    PPE_times = []
    aes_times = []
    rsa_times = []
    PPE_memory = []
    aes_memory = []
    rsa_memory = []
    
    for size_name, algo_results in results.items():
        sizes.append(size_name)
        
        # Time data
        PPE_time = algo_results.get("PPE", {}).get('total_time', 0) if algo_results.get("PPE") else 0
        aes_time = algo_results.get("aes", {}).get('total_time', 0) if algo_results.get("aes") else 0
        rsa_time = algo_results.get("rsa", {}).get('total_time', 0) if algo_results.get("rsa") else 0
        
        PPE_times.append(PPE_time)
        aes_times.append(aes_time)
        rsa_times.append(rsa_time)
        
        # Memory data
        PPE_mem = algo_results.get("PPE", {}).get('memory_usage', 0) if algo_results.get("PPE") else 0
        aes_mem = algo_results.get("aes", {}).get('memory_usage', 0) if algo_results.get("aes") else 0
        rsa_mem = algo_results.get("rsa", {}).get('memory_usage', 0) if algo_results.get("rsa") else 0
        
        PPE_memory.append(PPE_mem / 1024)  # Convert to KB
        aes_memory.append(aes_mem / 1024)
        rsa_memory.append(rsa_mem / 1024)
    
    # Create charts
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    
    # 1. Execution Time Comparison
    x = np.arange(len(sizes))
    width = 0.25
    
    ax1.bar(x - width, PPE_times, width, label='PPE', color=colors['PPE'])
    ax1.bar(x, aes_times, width, label='AES-128', color=colors['aes'])
    ax1.bar(x + width, rsa_times, width, label='RSA-2048', color=colors['rsa'])
    
    ax1.set_title('Execution Time Comparison', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Time (milliseconds)')
    ax1.set_xticks(x)
    ax1.set_xticklabels(sizes, rotation=45)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. Memory Usage Comparison
    ax2.bar(x - width, PPE_memory, width, label='PPE', color=colors['PPE'])
    ax2.bar(x, aes_memory, width, label='AES-128', color=colors['aes'])
    ax2.bar(x + width, rsa_memory, width, label='RSA-2048', color=colors['rsa'])
    
    ax2.set_title('Memory Usage Comparison', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Memory (Kilobytes)')
    ax2.set_xticks(x)
    ax2.set_xticklabels(sizes, rotation=45)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # 3. Algorithm Performance Radar Chart (for first data size)
    if sizes:
        first_size = sizes[0]
        first_results = results[first_size]
        
        # Normalize values for radar chart
        max_time = max([first_results.get(algo, {}).get('total_time', 0) for algo in algorithms])
        max_memory = max([first_results.get(algo, {}).get('memory_usage', 0) for algo in algorithms])
        
        categories = ['Speed\n(Lower is better)', 'Memory\n(Lower is better)', 'Security\n(Higher is better)']
        security_scores = [1, 3, 5]  # PPE=1, AES=3, RSA=5
        
        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
        angles += angles[:1]  # Complete the circle
        
        for i, algorithm in enumerate(algorithms):
            if first_results.get(algorithm):
                speed_score = 5 - (first_results[algorithm]['total_time'] / max_time * 4) if max_time > 0 else 5
                memory_score = 5 - (first_results[algorithm]['memory_usage'] / max_memory * 4) if max_memory > 0 else 5
                
                values = [speed_score, memory_score, security_scores[i]]
                values += values[:1]  # Complete the circle
                
                ax3.plot(angles, values, 'o-', linewidth=2, label=algorithm_names[algorithm], color=colors[algorithm])
                ax3.fill(angles, values, alpha=0.25, color=colors[algorithm])
        
        ax3.set_xticks(angles[:-1])
        ax3.set_xticklabels(categories)
        ax3.set_ylim(0, 5)
        ax3.set_title(f'Algorithm Comparison ({first_size})', fontsize=14, fontweight='bold')
        ax3.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
        ax3.grid(True)
    
    # 4. Throughput Comparison
    throughput_data = []
    throughput_labels = []
    
    for size_name, algo_results in results.items():
        data_size = len(size_name.split('(')[1].split(')')[0].replace('B', '').replace('KB', '000'))
        if 'KB' in size_name:
            data_size = float(size_name.split('(')[1].split(')')[0].replace('KB', '')) * 1024
        
        for algorithm in algorithms:
            if algo_results.get(algorithm):
                time_sec = algo_results[algorithm]['total_time'] / 1000
                throughput = data_size / time_sec if time_sec > 0 else 0
                throughput_data.append(throughput)
                throughput_labels.append(f"{algorithm.upper()}\n{size_name}")
    
    bars = ax4.bar(throughput_labels, throughput_data, color=[colors[algo] for algo in algorithms * len(results)])
    ax4.set_title('Throughput Comparison', fontsize=14, fontweight='bold')
    ax4.set_ylabel('Bytes per Second')
    ax4.tick_params(axis='x', rotation=45)
    ax4.grid(True, alpha=0.3)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:,.0f}',
                ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    plt.show()
    
    print("\n📊 Algorithm comparison charts are displayed in a window.")
    print("💡 Key insights:")
    print("   • PPE is fastest but least secure")
    print("   • AES provides good balance of speed and security")
    print("   • RSA is most secure but slowest and memory-intensive")

if __name__ == "__main__":
    print("🚀 Starting ESP32 Algorithm Comparison Simulation")
    print("This will compare PPE, AES, and RSA algorithms on ESP32")
    print()
    
    # اجرای بنچمارک
    try:
        results = esp32_algorithm_benchmark()
        
        if results:
            print_algorithm_analysis(results)
            plot_algorithm_comparison_charts(results)
        else:
            print("❌ No results obtained from benchmark")
            
    except KeyboardInterrupt:
        print("\n⏹️  Benchmark interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during benchmark: {str(e)}")
    
    print(f"\n{'='*70}")
    print("🏁 ESP32 Algorithm Comparison Complete!")
    print("These results show the trade-offs between speed, memory, and security on ESP32.")
    print(f"{'='*70}")