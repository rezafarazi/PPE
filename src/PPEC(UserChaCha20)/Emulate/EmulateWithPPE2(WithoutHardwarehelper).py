import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tabulate import tabulate
import seaborn as sns
import psutil
import threading
import multiprocessing as mp
from datetime import datetime
import hashlib
import gc
import os
import sys
import importlib.util

# Disable AES-NI for fair benchmarking (force software AES)
# Set OPENSSL_ia32cap to mask AES-NI bit (~0x2000000 disables AES-NI)
os.environ['OPENSSL_ia32cap'] = '~0x2000000'
print("AES-NI disabled via OPENSSL_ia32cap for fair ESP32 simulation")

# Import the encryption modules (assuming they're in separate files)
# You'll need to save your two algorithms as ppe_algorithm.py and ppec_algorithm.py
try:
    # Load PPE algorithm dynamically
    spec_ppe = importlib.util.spec_from_file_location("ppe_algorithm", "ppe_algorithm.py")
    ppe_module = importlib.util.module_from_spec(spec_ppe)
    spec_ppe.loader.exec_module(ppe_module)  # Exec after env set
    
    # Load PPEC algorithm dynamically  
    spec_ppec = importlib.util.spec_from_file_location("ppec_algorithm", "ppec_algorithm.py")
    ppec_module = importlib.util.module_from_spec(spec_ppec)
    spec_ppec.loader.exec_module(ppec_module)
    
    print("Encryption modules loaded dynamically (AES-NI disabled)")
except ImportError:
    print("Warning: Make sure to save your algorithms as 'ppe_algorithm.py' and 'ppec_algorithm.py'")

class ESP32ConstrainedBenchmark:
    """ESP32-constrained benchmark system for 13650HX processor"""
    
    def __init__(self):
        self.esp32_freq_limit = 240  # MHz equivalent
        self.esp32_memory_limit = 520 * 1024  # 520KB in bytes
        self.esp32_core_count = 2
        self.system_freq = self._get_cpu_frequency()
        self.constraint_factor = self.esp32_freq_limit / self.system_freq
        
        # Power monitoring setup
        self.baseline_power = self._measure_baseline_power()
        
        print(f"System CPU Frequency: {self.system_freq:.0f} MHz")
        print(f"ESP32 Constraint Factor: {self.constraint_factor:.4f}")
        print(f"Baseline Power: {self.baseline_power:.2f}W")
        
    def _get_cpu_frequency(self):
        """Get current CPU frequency"""
        try:
            freq = psutil.cpu_freq()
            return freq.current if freq else 3000  # Default fallback
        except:
            return 3000  # Default fallback
            
    def _measure_baseline_power(self):
        """Estimate baseline power consumption"""
        try:
            # Simple CPU utilization based power estimation
            cpu_percent = psutil.cpu_percent(interval=1)
            # Rough estimation: idle ~15W, full load ~65W for mobile processor
            estimated_power = 15 + (cpu_percent / 100) * 50
            return estimated_power
        except:
            return 25.0  # Default estimation
            
    def _constrain_to_esp32(self, func, *args, **kwargs):
        """Apply ESP32-like constraints to function execution"""
        
        # Memory constraint simulation
        initial_memory = psutil.Process().memory_info().rss
        
        # CPU constraint simulation through artificial delays
        start_time = time.perf_counter()
        
        # Execute the function
        result = func(*args, **kwargs)
        
        execution_time = time.perf_counter() - start_time
        
        # Apply ESP32 speed constraint
        constrained_time = execution_time / self.constraint_factor
        
        # Simulate ESP32 delay
        if constrained_time > execution_time:
            time.sleep(constrained_time - execution_time)
            
        final_memory = psutil.Process().memory_info().rss
        memory_used = final_memory - initial_memory
        
        return result, constrained_time, memory_used
        
    def measure_power_consumption(self, duration=1.0):
        """Measure power consumption during execution"""
        power_samples = []
        start_time = time.time()
        
        while time.time() - start_time < duration:
            cpu_percent = psutil.cpu_percent(interval=0.1)
            # Power estimation based on CPU usage
            estimated_power = 15 + (cpu_percent / 100) * 50  # 15W idle to 65W full load
            power_samples.append(estimated_power)
            
        return np.mean(power_samples) if power_samples else self.baseline_power

class EncryptionBenchmark:
    """Comprehensive encryption algorithm benchmark"""
    
    def __init__(self):
        self.esp32_benchmark = ESP32ConstrainedBenchmark()
        self.results = []
        
    def benchmark_ppe_algorithm(self, data, salt, iterations=10):
        """Benchmark PPE (AES) algorithm"""
        times = []
        memory_usage = []
        power_consumption = []
        
        # Load PPE module dynamically (already loaded globally, but reload if needed)
        try:
            spec = importlib.util.spec_from_file_location("ppe_algorithm", "ppe_algorithm.py")
            ppe_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(ppe_module)
        except:
            # Fallback simulation if module not found
            return self._simulate_ppe_performance(len(data), iterations)
        
        for i in range(iterations):
            gc.collect()  # Clean memory before test
            
            start_time = time.perf_counter()
            start_memory = psutil.Process().memory_info().rss
            
            try:
                # Encrypt
                encrypted = ppe_module.PPE(data, salt)
                
                # Decrypt
                decrypted = ppe_module.PPD(encrypted, salt)
                
                end_time = time.perf_counter()
                end_memory = psutil.Process().memory_info().rss
                
                # Apply ESP32 constraints
                execution_time = end_time - start_time
                constrained_time = execution_time / self.esp32_benchmark.constraint_factor
                memory_used = end_memory - start_memory
                
                times.append(constrained_time)
                memory_usage.append(memory_used / 1024)  # Convert to KB
                
                # Estimate power consumption
                power = self.esp32_benchmark.measure_power_consumption(constrained_time)
                power_consumption.append(power)
                
            except Exception as e:
                print(f"Error in PPE algorithm: {e}")
                return self._simulate_ppe_performance(len(data), iterations)
                
        return {
            'algorithm': 'PPE (AES)',
            'avg_time_ms': np.mean(times) * 1000,
            'std_time_ms': np.std(times) * 1000,
            'avg_memory_kb': np.mean(memory_usage),
            'avg_power_w': np.mean(power_consumption),
            'throughput_kbps': (len(data) * 2) / (np.mean(times) * 1024),  # Encrypt + Decrypt
            'times': times,
            'memory_samples': memory_usage,
            'power_samples': power_consumption
        }
    
    def benchmark_ppec_algorithm(self, data, salt, iterations=10):
        """Benchmark PPEC (ChaCha20) algorithm"""
        times = []
        memory_usage = []
        power_consumption = []
        
        # Load PPEC module dynamically
        try:
            spec = importlib.util.spec_from_file_location("ppec_algorithm", "ppec_algorithm.py")
            ppec_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(ppec_module)
        except Exception as e:
            print(f"Could not load PPEC algorithm: {e}")
            print("Using simulation instead...")
            return self._simulate_ppec_performance(len(data), iterations)
        
        for i in range(iterations):
            gc.collect()  # Clean memory before test
            
            start_time = time.perf_counter()
            start_memory = psutil.Process().memory_info().rss
            
            try:
                # Encrypt
                encrypted = ppec_module.PPE(data, salt)  # Using same interface
                
                # Decrypt
                decrypted = ppec_module.PPD(encrypted, salt)
                
                end_time = time.perf_counter()
                end_memory = psutil.Process().memory_info().rss
                
                # Apply ESP32 constraints
                execution_time = end_time - start_time
                constrained_time = execution_time / self.esp32_benchmark.constraint_factor
                memory_used = end_memory - start_memory
                
                times.append(constrained_time)
                memory_usage.append(max(memory_used / 1024, 1.0))  # Convert to KB, minimum 1KB
                
                # Estimate power consumption
                power = self.esp32_benchmark.measure_power_consumption(min(constrained_time, 1.0))
                power_consumption.append(power)
                
            except Exception as e:
                print(f"Error in PPEC algorithm execution: {e}")
                return self._simulate_ppec_performance(len(data), iterations)
                
        return {
            'algorithm': 'PPEC (ChaCha20)',
            'avg_time_ms': np.mean(times) * 1000,
            'std_time_ms': np.std(times) * 1000,
            'avg_memory_kb': np.mean(memory_usage),
            'avg_power_w': np.mean(power_consumption),
            'throughput_kbps': (len(data) * 2) / (np.mean(times) * 1024),  # Encrypt + Decrypt
            'times': times,
            'memory_samples': memory_usage,
            'power_samples': power_consumption
        }
    
    def _simulate_ppe_performance(self, data_size, iterations):
        """Simulate PPE performance if algorithm not available (now with software AES in mind)"""
        # Adjusted for software AES (slower than hardware)
        base_time = (data_size * 1.2e-6) * iterations  # Increased time for software AES
        constrained_time = base_time / self.esp32_benchmark.constraint_factor
        
        return {
            'algorithm': 'PPE (AES) - Simulated (Software)',
            'avg_time_ms': constrained_time * 1000,
            'std_time_ms': constrained_time * 100,
            'avg_memory_kb': 3.5 + (data_size / 1000),
            'avg_power_w': 45 + (data_size / 100),
            'throughput_kbps': (data_size * 2) / (constrained_time * 1024),
            'times': [constrained_time] * iterations,
            'memory_samples': [3.5 + (data_size / 1000)] * iterations,
            'power_samples': [45 + (data_size / 100)] * iterations
        }
    
    def _simulate_ppec_performance(self, data_size, iterations):
        """Simulate PPEC performance if algorithm not available"""
        # Based on ChaCha20 characteristics (unchanged, as it's software)
        base_time = (data_size * 0.7e-6) * iterations  # microseconds to seconds
        constrained_time = base_time / self.esp32_benchmark.constraint_factor
        
        return {
            'algorithm': 'PPEC (ChaCha20) - Simulated',
            'avg_time_ms': constrained_time * 1000,
            'std_time_ms': constrained_time * 80,
            'avg_memory_kb': 2.8 + (data_size / 1200),
            'avg_power_w': 38 + (data_size / 120),
            'throughput_kbps': (data_size * 2) / (constrained_time * 1024),
            'times': [constrained_time] * iterations,
            'memory_samples': [2.8 + (data_size / 1200)] * iterations,
            'power_samples': [38 + (data_size / 120)] * iterations
        }
    
def setup_algorithm_files():
    pass 

def main():
    pass 

if __name__ == "__main__":
    main()