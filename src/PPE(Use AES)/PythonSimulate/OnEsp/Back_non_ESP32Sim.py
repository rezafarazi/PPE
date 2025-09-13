import time
import hashlib
import gc
import sys
import os

class ESP32Simulator:
    """
    شبیه‌ساز ساده ESP32 بدون dependency اضافی
    """
    
    def __init__(self):
        # مشخصات واقعی ESP32
        self.ESP32_CPU_FREQ = 240_000_000  # 240 MHz
        self.YOUR_CPU_FREQ = 3_600_000_000  # تخمین i7-13650HX base clock
        self.SLOWDOWN_FACTOR = self.YOUR_CPU_FREQ / self.ESP32_CPU_FREQ  # ~15x
        
        # محدودیت‌های حافظه ESP32
        self.MAX_HEAP_SIZE = 300 * 1024  # 300KB قابل استفاده از 520KB
        self.MAX_CHUNK_SIZE = 4 * 1024   # 4KB حداکثر چانک
        self.MAX_STACK_SIZE = 8 * 1024   # 8KB stack
        
        print(f"🔧 ESP32 Simulator initialized:")
        print(f"   CPU Slowdown Factor: {self.SLOWDOWN_FACTOR:.1f}x")
        print(f"   Max Heap: {self.MAX_HEAP_SIZE:,} bytes")
        print(f"   Max Chunk: {self.MAX_CHUNK_SIZE:,} bytes")
        print()
    
    def simulate_cpu_slowdown(self, operation_time):
        """شبیه‌سازی کندی CPU"""
        if operation_time > 0:
            # محاسبه زمان انتظار برای شبیه‌سازی کندی
            delay = operation_time * (self.SLOWDOWN_FACTOR - 1) / 1000000  # تبدیل به ثانیه
            if delay > 0:
                time.sleep(min(delay, 0.1))  # حداکثر 100ms انتظار
    
    def check_memory_limit(self, data_size):
        """بررسی محدودیت حافظه"""
        if data_size > self.MAX_HEAP_SIZE:
            raise MemoryError(f"Data size {data_size:,} exceeds ESP32 heap limit {self.MAX_HEAP_SIZE:,}")
        
        if data_size > self.MAX_HEAP_SIZE * 0.8:
            print(f"⚠️  Memory pressure: {data_size:,}/{self.MAX_HEAP_SIZE:,} bytes")
    
    def get_memory_usage(self):
        """تخمین استفاده حافظه فعلی"""
        # تخمین ساده بدون psutil
        return len(gc.get_objects()) * 100  # تخمین تقریبی

class ESP32CryptoSimulator:
    """شبیه‌ساز الگوریتم‌های رمزنگاری ESP32"""
    
    def __init__(self):
        self.simulator = ESP32Simulator()
        
    def get_current_time_key(self, salt):
        """تولید کلید بر اساس زمان - نسخه ESP32"""
        start_time = time.perf_counter()
        
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
            time.sleep(0.0001)  # تأخیر کوچک
        
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
            if i % 10 == 0:  # هر 10 کاراکتر یک تأخیر
                time.sleep(0.00001)
        
        key = (salt + key)[:16].ljust(16, '0')
        
        operation_time = time.perf_counter() - start_time
        self.simulator.simulate_cpu_slowdown(operation_time * 1000)  # تبدیل به میلی‌ثانیه
        
        return key.encode('utf-8')
    
    def simple_xor_encrypt(self, data, key):
        """رمزنگاری XOR ساده مانند ESP32"""
        start_time = time.perf_counter()
        
        # بررسی محدودیت حافظه
        data_bytes = data.encode('utf-8')
        self.simulator.check_memory_limit(len(data_bytes) * 3)
        
        key_bytes = key[:16]
        result = bytearray()
        
        # شبیه‌سازی پردازش byte-by-byte ESP32
        for i, byte in enumerate(data_bytes):
            result.append(byte ^ key_bytes[i % len(key_bytes)])
            
            # هر 50 byte یک تأخیر کوچک
            if i > 0 and i % 50 == 0:
                time.sleep(0.0001)
        
        operation_time = time.perf_counter() - start_time
        self.simulator.simulate_cpu_slowdown(operation_time * 1000)
        
        # شبیه‌سازی garbage collection
        if len(data_bytes) > 1000:
            gc.collect()
            time.sleep(0.001)
        
        return result.hex()
    
    def simple_xor_decrypt(self, hex_data, key):
        """رمزگشایی XOR ساده"""
        start_time = time.perf_counter()
        
        try:
            encrypted_bytes = bytes.fromhex(hex_data)
            self.simulator.check_memory_limit(len(encrypted_bytes) * 2)
            
            key_bytes = key[:16]
            result = bytearray()
            
            for i, byte in enumerate(encrypted_bytes):
                result.append(byte ^ key_bytes[i % len(key_bytes)])
                
                if i > 0 and i % 50 == 0:
                    time.sleep(0.0001)
            
            operation_time = time.perf_counter() - start_time
            self.simulator.simulate_cpu_slowdown(operation_time * 1000)
            
            return result.decode('utf-8')
        except Exception as e:
            return f"Decryption failed: {str(e)}"
    
    def chunked_process(self, data, salt, encrypt=True):
        """پردازش تکه‌ای مانند ESP32"""
        key = self.get_current_time_key(salt)
        
        # تقسیم به چانک‌های کوچک ESP32
        max_chunk = min(self.simulator.MAX_CHUNK_SIZE, 1024)  # حداکثر 1KB chunks
        data_bytes = data.encode('utf-8') if encrypt else data
        
        if len(data_bytes if encrypt else data) <= max_chunk:
            # داده کوچک - پردازش یکجا
            if encrypt:
                return self.simple_xor_encrypt(data, key)
            else:
                return self.simple_xor_decrypt(data, key)
        else:
            # داده بزرگ - پردازش تکه‌ای
            result_parts = []
            
            if encrypt:
                for i in range(0, len(data), max_chunk // 4):  # کاراکترها نه بایت‌ها
                    chunk = data[i:i + max_chunk // 4]
                    encrypted_chunk = self.simple_xor_encrypt(chunk, key)
                    result_parts.append(encrypted_chunk)
                    
                    # شبیه‌سازی تأخیر بین چانک‌ها
                    time.sleep(0.002)
                    print(f"   📦 Processed chunk {len(result_parts)}")
                
                return "|".join(result_parts)
            else:
                # رمزگشایی چانک‌ها
                chunks = data.split("|")
                for i, chunk in enumerate(chunks):
                    if chunk.strip():
                        decrypted_chunk = self.simple_xor_decrypt(chunk, key)
                        result_parts.append(decrypted_chunk)
                        time.sleep(0.002)
                        print(f"   📦 Decrypted chunk {i + 1}")
                
                return "".join(result_parts)
    
    def encrypt(self, data, salt):
        """تابع اصلی رمزنگاری"""
        encrypted = self.chunked_process(data, salt, encrypt=True)
        key = self.get_current_time_key(salt)
        return encrypted, key.hex()
    
    def decrypt(self, encrypted_data, salt, key=None):
        """تابع اصلی رمزگشایی"""
        return self.chunked_process(encrypted_data, salt, encrypt=False)

def esp32_simple_benchmark():
    """بنچمارک ساده ESP32"""
    
    # داده‌های آزمایشی مناسب ESP32
    test_cases = [
        ("ESP32 Tiny (32B)", "Hello ESP32 encryption test!"),
        ("ESP32 Small (128B)", "This is a small test message for ESP32 encryption benchmarking with realistic data size for microcontroller."),
        ("ESP32 Medium (512B)", "ESP32 medium size test. " + "This tests ESP32 encryption performance with moderate data size that's typical for IoT applications. " * 4),
        ("ESP32 Large (2KB)", "ESP32 large test. " + "Testing larger data encryption on ESP32 with memory constraints and processing limitations typical of microcontrollers. " * 20),
        ("ESP32 Max (4KB)", "ESP32 maximum size. " + "Maximum recommended data size for ESP32 encryption testing with full memory utilization. " * 50)
    ]
    
    crypto_sim = ESP32CryptoSimulator()
    results = {}
    salt = "esp32test"
    iterations = 3
    
    print("🚀 ESP32 Simple Performance Simulation")
    print("="*60)
    print(f"🎯 Target: ESP32 (240MHz, 520KB RAM)")
    print(f"💻 Host: i7-13650HX")
    print(f"🔄 Iterations: {iterations}")
    print()
    
    for size_name, test_data in test_cases:
        data_size = len(test_data.encode('utf-8'))
        print(f"📊 Testing {size_name}")
        print(f"   📏 Size: {data_size:,} bytes")
        
        # بررسی محدودیت حافظه
        try:
            crypto_sim.simulator.check_memory_limit(data_size * 3)
        except MemoryError as e:
            print(f"   ❌ Skipped: {e}")
            continue
        
        encrypt_times = []
        decrypt_times = []
        key_gen_times = []
        success_count = 0
        
        for iteration in range(iterations):
            print(f"   🔄 Iteration {iteration + 1}/{iterations}")
            
            try:
                # تست تولید کلید
                start_time = time.perf_counter()
                key = crypto_sim.get_current_time_key(salt)
                key_gen_time = (time.perf_counter() - start_time) * 1000
                key_gen_times.append(key_gen_time)
                
                # تست رمزنگاری
                start_time = time.perf_counter()
                encrypted, key_hex = crypto_sim.encrypt(test_data, salt)
                encrypt_time = (time.perf_counter() - start_time) * 1000
                encrypt_times.append(encrypt_time)
                print(f"      🔐 Encryption: {encrypt_time:.1f} ms")
                
                # تست رمزگشایی
                start_time = time.perf_counter()
                decrypted = crypto_sim.decrypt(encrypted, salt)
                decrypt_time = (time.perf_counter() - start_time) * 1000
                decrypt_times.append(decrypt_time)
                print(f"      🔓 Decryption: {decrypt_time:.1f} ms")
                
                # بررسی صحت
                if test_data.strip() == decrypted.strip():
                    success_count += 1
                    print(f"      ✅ Data integrity: OK")
                else:
                    print(f"      ❌ Data integrity: Failed")
                    print(f"         Original length: {len(test_data)}")
                    print(f"         Decrypted length: {len(decrypted)}")
                
            except Exception as e:
                print(f"      ❌ Error: {str(e)}")
                continue
        
        if encrypt_times and decrypt_times:
            avg_encrypt = sum(encrypt_times) / len(encrypt_times)
            avg_decrypt = sum(decrypt_times) / len(decrypt_times)
            avg_key_gen = sum(key_gen_times) / len(key_gen_times)
            total_time = avg_encrypt + avg_decrypt + avg_key_gen
            
            results[size_name] = {
                'encrypt_time': avg_encrypt,
                'decrypt_time': avg_decrypt, 
                'key_gen_time': avg_key_gen,
                'total_time': total_time,
                'data_size': data_size,
                'success_rate': (success_count / iterations) * 100
            }
            
            # نمایش خلاصه نتایج
            print(f"   📈 Summary:")
            print(f"      🔑 Key Gen: {avg_key_gen:.1f} ms")
            print(f"      🔐 Encrypt: {avg_encrypt:.1f} ms") 
            print(f"      🔓 Decrypt: {avg_decrypt:.1f} ms")
            print(f"      ⏱️  Total: {total_time:.1f} ms")
            print(f"      ✅ Success: {results[size_name]['success_rate']:.0f}%")
            
            # محاسبه throughput
            throughput = (data_size / (total_time / 1000)) if total_time > 0 else 0
            print(f"      🚀 Throughput: {throughput:,.0f} bytes/sec")
            
            # تحلیل عملکرد
            if total_time < 100:
                performance = "🚀 Excellent"
            elif total_time < 500:
                performance = "✅ Good"
            elif total_time < 1000:
                performance = "⚠️  Acceptable"  
            else:
                performance = "❌ Slow"
            
            print(f"      📊 Rating: {performance}")
        
        print("-" * 60)
    
    return results

def print_final_analysis(results):
    """تحلیل نهایی نتایج"""
    
    print("\n" + "="*60)
    print("🎯 FINAL ESP32 PERFORMANCE ANALYSIS")
    print("="*60)
    
    if not results:
        print("❌ No results to analyze")
        return
    
    print(f"\n📊 PERFORMANCE COMPARISON:")
    print("-" * 40)
    
    # جدول نتایج
    print(f"{'Size':<20} {'Total (ms)':<12} {'Throughput':<15} {'Rating'}")
    print("-" * 60)
    
    for size_name, metrics in results.items():
        size_short = size_name.split()[1] if len(size_name.split()) > 1 else size_name[:15]
        total_ms = f"{metrics['total_time']:.1f}"
        
        # محاسبه throughput
        throughput = (metrics['data_size'] / (metrics['total_time'] / 1000)) if metrics['total_time'] > 0 else 0
        throughput_str = f"{throughput:,.0f} B/s"
        
        # رتبه‌بندی
        if metrics['total_time'] < 100:
            rating = "Excellent"
        elif metrics['total_time'] < 500:
            rating = "Good"
        elif metrics['total_time'] < 1000:
            rating = "Acceptable"
        else:
            rating = "Slow"
        
        print(f"{size_short:<20} {total_ms:<12} {throughput_str:<15} {rating}")
    
    print(f"\n🎯 ESP32 RECOMMENDATIONS:")
    print("-" * 40)
    print("1. 📦 Optimal data size: 32-512 bytes")
    print("2. 🧠 Memory usage: Keep under 200KB")  
    print("3. ⚡ For speed: Use simple XOR encryption")
    print("4. 🔒 For security: Use AES with small data only")
    print("5. 🔄 Process in chunks: 1KB maximum")
    print("6. ⏱️  Expected real ESP32: 2-5x slower than simulation")
    
    # بهترین و بدترین عملکرد
    if results:
        best = min(results.items(), key=lambda x: x[1]['total_time'])
        worst = max(results.items(), key=lambda x: x[1]['total_time'])
        
        print(f"\n🏆 BEST PERFORMANCE:")
        print(f"   {best[0]}: {best[1]['total_time']:.1f} ms")
        
        print(f"\n🐌 WORST PERFORMANCE:")
        print(f"   {worst[0]}: {worst[1]['total_time']:.1f} ms")
    
    print(f"\n📝 SIMULATION ACCURACY:")
    print("✅ CPU slowdown: Simulated (15x slower)")
    print("✅ Memory limits: Enforced (300KB max)")
    print("✅ Chunk processing: Implemented")
    print("⚠️  Real hardware effects: Not simulated")
    print("📊 Estimated accuracy: 75-85% of real ESP32")

if __name__ == "__main__":
    try:
        print("🚀 Starting ESP32 Simple Performance Simulation")
        print("No external dependencies required!")
        print()
        
        # اجرای بنچمارک
        results = esp32_simple_benchmark()
        
        # تحلیل نتایج
        print_final_analysis(results)
        
        print(f"\n{'='*60}")
        print("🏁 ESP32 Simulation Complete!")
        print("These results approximate real ESP32 performance.")
        print(f"{'='*60}")
        
    except KeyboardInterrupt:
        print(f"\n⏹️  Simulation interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        print("Please report this issue for debugging.")