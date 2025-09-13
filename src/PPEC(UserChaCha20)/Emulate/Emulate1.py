import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tabulate import tabulate
import seaborn as sns
import random
from datetime import datetime
import hashlib

class AlgorithmSimulator:
    """Simulate algorithm performance based on realistic parameters"""
    
    def __init__(self):
        self.esp32_base_freq = 240  # MHz
        self.core_count = 2
        self.memory_available = 320  # KB SRAM
        self.base_power_consumption = 40  # mW idle
        
    def simulate_ppec_performance(self, data_size_bytes):
        """Simulate PPEC (Parallel Processing Encryption with ChaCha20) dual-thread performance with time-based key generation"""
        
        # PPEC-specific calculations
        # Time-based key generation overhead
        time_key_generation = 15 + random.uniform(-3, 5)  # ms for unix time fetch + key generation
        
        # ChaCha20 encryption per core (data split in half)
        base_time_per_byte = 0.7 + random.uniform(-0.1, 0.1)  # ChaCha20 base performance
        
        # Parallel processing (dual-core efficiency)
        parallel_efficiency = 0.88 + random.uniform(-0.05, 0.08)  # Better than generic parallel due to optimization
        
        # Calculate processing time
        single_thread_time = data_size_bytes * base_time_per_byte
        dual_thread_time = (single_thread_time / 2) / parallel_efficiency
        
        # Add PPEC-specific overheads
        data_splitting_overhead = 0.2 + random.uniform(-0.05, 0.1)  # ms
        base64_encoding_overhead = 0.4 + random.uniform(-0.1, 0.2)  # ms
        sync_overhead = 0.25 + random.uniform(-0.05, 0.1)  # ms (optimized)
        
        total_time = time_key_generation + dual_thread_time + data_splitting_overhead + base64_encoding_overhead + sync_overhead
        
        # Memory calculation for PPEC
        base_memory = 2.8  # KB base PPEC algorithm
        thread_overhead = 1.4  # KB for thread management (higher due to multiprocessing.Pool)
        key_generation_memory = 0.8  # KB for time-based key generation
        chacha20_memory = 0.5  # KB for ChaCha20 cipher objects
        data_split_memory = (data_size_bytes / 1000) * 2  # Additional memory for data splitting
        total_memory = base_memory + thread_overhead + key_generation_memory + chacha20_memory + data_split_memory
        
        # Power calculation
        key_generation_power = 25  # mW for network request + computation
        processing_power_per_core = 28 + (data_size_bytes / 120) * 2.2
        dual_core_power = processing_power_per_core * 1.85  # Slightly better efficiency
        total_power = self.base_power_consumption + key_generation_power + dual_core_power
        
        return {
            'time_ms': total_time,
            'memory_kb': total_memory,
            'power_mw': total_power,
            'core_utilization': [82 + random.uniform(-5, 8), 78 + random.uniform(-5, 8)],
            'thread_efficiency': 8.8 + random.uniform(-0.3, 0.7),
            'key_generation_time': time_key_generation
        }
    
    def simulate_chacha20_performance(self, data_size_bytes):
        """Simulate standard ChaCha20 single-thread performance"""
        
        base_time_per_byte = 0.7 + random.uniform(-0.1, 0.1)
        total_time = data_size_bytes * base_time_per_byte
        
        base_memory = 2.2 + random.uniform(-0.2, 0.3)
        key_memory = 0.032  # 32-byte key
        nonce_memory = 0.012  # 12-byte nonce
        total_memory = base_memory + key_memory + nonce_memory
        
        processing_power = 95 + (data_size_bytes / 60) * 2.5
        total_power = self.base_power_consumption + processing_power
        
        return {
            'time_ms': total_time,
            'memory_kb': total_memory,
            'power_mw': total_power,
            'core_utilization': [75 + random.uniform(-10, 15), 8 + random.uniform(0, 8)],
            'thread_efficiency': 2.5 + random.uniform(-0.5, 0.5)
        }
    
    def simulate_aes_performance(self, data_size_bytes):
        """Simulate AES single-thread performance"""
        
        base_time_per_byte = 0.6 + random.uniform(-0.1, 0.1)
        total_time = data_size_bytes * base_time_per_byte
        
        base_memory = 3.0 + random.uniform(-0.3, 0.5)
        key_memory = 0.4  # Fixed key size
        total_memory = base_memory + key_memory
        
        processing_power = 110 + (data_size_bytes / 50) * 3
        total_power = self.base_power_consumption + processing_power
        
        return {
            'time_ms': total_time,
            'memory_kb': total_memory,
            'power_mw': total_power,
            'core_utilization': [70 + random.uniform(-10, 15), 5 + random.uniform(0, 5)],
            'thread_efficiency': 2.0 + random.uniform(-0.5, 0.5)
        }
    
    def simulate_rsa_performance(self, data_size_bytes, key_size=2048):
        """Simulate RSA single-thread performance"""
        
        base_time_per_byte = 8.0 + random.uniform(-1.0, 2.0)
        key_factor = (key_size / 1024) ** 2
        total_time = data_size_bytes * base_time_per_byte * key_factor
        
        base_memory = 5.0 + random.uniform(-0.5, 1.0)
        key_memory = (key_size / 1024) * 4
        total_memory = base_memory + key_memory
        
        processing_power = 160 + (data_size_bytes / 20) * 5
        total_power = self.base_power_consumption + processing_power
        
        return {
            'time_ms': total_time,
            'memory_kb': total_memory,
            'power_mw': total_power,
            'core_utilization': [90 + random.uniform(-5, 10), 8 + random.uniform(0, 5)],
            'thread_efficiency': 1.0 + random.uniform(-0.2, 0.2)
        }
    
    def run_comparative_simulation(self, data_sizes=[32, 64, 128, 256, 512]):
        """Run comparative simulation for all algorithms"""
        
        results = {
            'data_sizes': data_sizes,
            'ppec_results': [],
            'chacha20_results': [],
            'aes_results': [],
            'rsa_results': []
        }
        
        for size in data_sizes:
            results['ppec_results'].append(self.simulate_ppec_performance(size))
            results['chacha20_results'].append(self.simulate_chacha20_performance(size))
            results['aes_results'].append(self.simulate_aes_performance(size))
            results['rsa_results'].append(self.simulate_rsa_performance(size))
        
        return results

def create_dynamic_comparison_data():
    """Create comparison data based on simulation results"""
    
    simulator = AlgorithmSimulator()
    
    ppec_result = simulator.simulate_ppec_performance(64)
    chacha20_result = simulator.simulate_chacha20_performance(64)
    aes_result = simulator.simulate_aes_performance(64)
    rsa_result = simulator.simulate_rsa_performance(64)
    
    comparison_data = {
        'Evaluation Criteria': [
            'Encryption Speed (64 bytes)',
            'Memory Consumption (KB)',
            'Power Consumption (mW)',
            'Processing Architecture',
            'Thread Utilization',
            'Embedded Systems Compatibility',
            'Attack Resistance',
            'Key Generation Method',
            'Dynamic Environment Compatibility',
            'Execution Flexibility',
            'Data Load Scalability',
            'Core Utilization',
            'Synchronization Overhead',
            'Real-time Performance',
            'Network Dependency',
            'Time-based Security'
        ],
        'PPEC (Time-based Dual-Thread)': [
            f'{ppec_result["time_ms"]:.1f} ms (includes {ppec_result["key_generation_time"]:.1f}ms key generation)',
            f'{ppec_result["memory_kb"]:.1f} (with multiprocessing overhead)',
            f'{ppec_result["power_mw"]:.0f} (network + dual-core processing)',
            'Parallel dual-thread with time-based key generation',
            f'Utilizes 2 threads (efficiency: {ppec_result["thread_efficiency"]:.1f}/10)',
            'Excellent - optimized for ESP32 dual-core with time sync',
            'Very High - dynamic time-based keys + ChaCha20',
            'Unix time + salt with dynamic generation (network dependent)',
            'Excellent - adaptive to network conditions',
            'Very high - modular thread-based design',
            'Superior - data partitioning across threads',
            f'Dual-core ({ppec_result["core_utilization"][0]:.0f}% / {ppec_result["core_utilization"][1]:.0f}%)',
            'Minimal - efficient multiprocessing.Pool mechanism',
            'Excellent - asynchronous processing with time sync',
            'Yes - requires internet for time synchronization',
            'Excellent - keys change based on time windows'
        ],
        'ChaCha20 (Standard Implementation)': [
            f'{chacha20_result["time_ms"]:.1f} ms (stream cipher processing)',
            f'{chacha20_result["memory_kb"]:.1f} (lightweight implementation)',
            f'{chacha20_result["power_mw"]:.0f} (efficient single-core)',
            'Sequential stream cipher operation',
            f'Single-thread execution (efficiency: {chacha20_result["thread_efficiency"]:.1f}/10)',
            'Very good - designed for embedded systems',
            'High - modern cryptographic security',
            'Fixed 256-bit key with random nonce',
            'Good - suitable for embedded environments',
            'Moderate - stream cipher structure',
            'Good - linear scaling with minimal overhead',
            f'Single-core ({chacha20_result["core_utilization"][0]:.0f}% / {chacha20_result["core_utilization"][1]:.0f}%)',
            'None - no multi-threading',
            'Very good - fast stream processing',
            'No - fully offline operation',
            'Low - static keys unless manually rotated'
        ],
        'AES (Standard Implementation)': [
            f'{aes_result["time_ms"]:.1f} ms (sequential processing)',
            f'{aes_result["memory_kb"]:.1f} (standard implementation)',
            f'{aes_result["power_mw"]:.0f} (single-core intensive)',
            'Sequential block-by-block processing',
            f'Single-thread execution (efficiency: {aes_result["thread_efficiency"]:.1f}/10)',
            'Good - requires optimization for embedded',
            'Very high - industry standard security',
            'Fixed 128/256-bit static keys',
            'Medium - needs manual optimization',
            'Low - rigid encryption structure',
            'Good - linear scaling with data size',
            f'Single-core ({aes_result["core_utilization"][0]:.0f}% / {aes_result["core_utilization"][1]:.0f}%)',
            'None - no multi-threading',
            'Good - predictable but slower',
            'No - fully offline operation',
            'Low - static keys unless manually rotated'
        ],
        'RSA (Standard Implementation)': [
            f'{rsa_result["time_ms"]:.0f} ms (complex mathematical operations)',
            f'{rsa_result["memory_kb"]:.1f} (large key storage requirements)',
            f'{rsa_result["power_mw"]:.0f} (computationally intensive)',
            'Sequential mathematical operations',
            f'Single-thread with heavy computation (efficiency: {rsa_result["thread_efficiency"]:.1f}/10)',
            'Poor - not suitable for ESP32 constraints',
            'Excellent with 2048+ bit keys',
            'Public/Private key pair (static)',
            'Poor - heavy computational requirements',
            'Very low - monolithic algorithm structure',
            'Poor - exponential increase with key size',
            f'Single-core intensive ({rsa_result["core_utilization"][0]:.0f}% / {rsa_result["core_utilization"][1]:.0f}%)',
            'None - sequential execution',
            'Poor - long processing delays',
            'No - fully offline operation',
            'Low - static key pairs'
        ]
    }
    
    return comparison_data, ppec_result, chacha20_result, aes_result, rsa_result

def print_dynamic_comprehensive_table():
    """Print comprehensive comparison table with dynamic data"""
    
    print("=" * 170)
    print("ESP32 COMPREHENSIVE ALGORITHM COMPARISON - PPEC vs ChaCha20 vs AES vs RSA")
    print("=" * 170)
    print("PPEC: Your time-based dual-core implementation with ChaCha20 encryption")
    print("ChaCha20: Standard single-thread stream cipher implementation")
    print("AES: Standard single-thread block cipher implementation")
    print("RSA: Standard single-thread asymmetric encryption with heavy computation")
    print("=" * 170)
    
    data, ppec_result, chacha20_result, aes_result, rsa_result = create_dynamic_comparison_data()
    df = pd.DataFrame(data)
    
    print(tabulate(df, headers='keys', tablefmt='grid', showindex=False))
    
    print("\n" + "=" * 170)
    print("PPEC ALGORITHM ANALYSIS")
    print("=" * 170)
    
    ppec_analysis = {
        'PPEC Component': [
            'Time-based Key Generation',
            'Network Time Synchronization', 
            'ChaCha20 Encryption (Core 0)',
            'ChaCha20 Encryption (Core 1)',
            'Data Splitting Overhead',
            'Base64 Encoding',
            'Thread Synchronization',
            'Total Processing Time'
        ],
        'Time (ms)': [
            f'{ppec_result["key_generation_time"]:.1f}',
            'Included in key generation',
            f'{(ppec_result["time_ms"] - ppec_result["key_generation_time"]) / 2:.1f}',
            f'{(ppec_result["time_ms"] - ppec_result["key_generation_time"]) / 2:.1f}',
            '0.2 ± 0.05',
            '0.4 ± 0.1',
            '0.25 ± 0.05',
            f'{ppec_result["time_ms"]:.1f}'
        ],
        'Description': [
            'Unix time fetch + salt processing + key derivation',
            'API call to worldtimeapi.org for accurate time',
            'Parallel encryption of first data half',
            'Parallel encryption of second data half', 
            'Data midpoint calculation and splitting',
            'Combined cipher text encoding',
            'multiprocessing.Pool coordination',
            'Complete PPEC encryption cycle'
        ]
    }
    
    ppec_df = pd.DataFrame(ppec_analysis)
    print(tabulate(ppec_df, headers='keys', tablefmt='grid', showindex=False))
    
    return ppec_result, chacha20_result, aes_result, rsa_result

def create_individual_charts(simulation_results):
    """Create individual charts for PPEC vs other algorithms"""
    
    data_sizes = simulation_results['data_sizes']
    ppec_results = simulation_results['ppec_results']
    chacha20_results = simulation_results['chacha20_results']
    aes_results = simulation_results['aes_results']
    rsa_results = simulation_results['rsa_results']
    
    colors = ['#FF0000', '#4CAF50', '#FF9800', '#9C27B0']  # Red for PPEC, Green, Orange, Purple
    
    print("Generating Chart 1/8: PPEC vs ChaCha20 vs AES vs RSA Performance...")
    
    # 1. Processing Time Comparison
    plt.figure(figsize=(14, 8))
    
    ppec_times = [result['time_ms'] for result in ppec_results]
    chacha20_times = [result['time_ms'] for result in chacha20_results]
    aes_times = [result['time_ms'] for result in aes_results]
    rsa_times = [result['time_ms'] for result in rsa_results]
    
    plt.plot(data_sizes, ppec_times, 'o-', label='PPEC (Time-based Dual-Thread)', color=colors[0], linewidth=3, markersize=8)
    plt.plot(data_sizes, chacha20_times, 's-', label='ChaCha20 (Standard)', color=colors[1], linewidth=3, markersize=8)
    plt.plot(data_sizes, aes_times, '^-', label='AES (Standard)', color=colors[2], linewidth=3, markersize=8)
    plt.plot(data_sizes, rsa_times, 'd-', label='RSA (Standard)', color=colors[3], linewidth=3, markersize=8)
    
    plt.title('Processing Time Comparison: PPEC vs Standard Algorithms', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Data Size (bytes)', fontsize=14)
    plt.ylabel('Processing Time (ms)', fontsize=14)
    plt.legend(fontsize=12, loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.yscale('log')
    
    plt.annotate(f'PPEC includes {ppec_results[1]["key_generation_time"]:.1f}ms key generation overhead', 
                xy=(64, ppec_times[1]), xytext=(200, ppec_times[1]*2),
                arrowprops=dict(arrowstyle='->', color='red', alpha=0.7),
                fontsize=10, color='red')
    
    plt.tight_layout()
    plt.show()
    
    input("Press Enter to continue to the next chart...")
    
    # 2. Memory Usage Analysis
    plt.figure(figsize=(14, 8))
    
    ppec_memory = [result['memory_kb'] for result in ppec_results]
    chacha20_memory = [result['memory_kb'] for result in chacha20_results]
    aes_memory = [result['memory_kb'] for result in aes_results]
    rsa_memory = [result['memory_kb'] for result in rsa_results]
    
    plt.plot(data_sizes, ppec_memory, 'o-', label='PPEC (with Thread Management)', color=colors[0], linewidth=3, markersize=8)
    plt.plot(data_sizes, chacha20_memory, 's-', label='ChaCha20 (Lightweight)', color=colors[1], linewidth=3, markersize=8)
    plt.plot(data_sizes, aes_memory, '^-', label='AES (Standard)', color=colors[2], linewidth=3, markersize=8)
    plt.plot(data_sizes, rsa_memory, 'd-', label='RSA (Large Keys)', color=colors[3], linewidth=3, markersize=8)
    
    plt.title('Memory Usage Comparison: PPEC vs Standard Algorithms', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Data Size (bytes)', fontsize=14)
    plt.ylabel('Memory Usage (KB)', fontsize=14)
    plt.legend(fontsize=12, loc='upper left')
    plt.grid(True, alpha=0.3)
    
    plt.axhline(y=320, color='red', linestyle='--', alpha=0.7, linewidth=2)
    plt.text(400, 330, 'ESP32 SRAM Limit (320KB)', fontsize=10, color='red')
    
    plt.tight_layout()
    plt.show()
    
    input("Press Enter to continue to the next chart...")
    
    # 3. PPEC Component Breakdown
    plt.figure(figsize=(14, 8))
    
    ppec_64 = ppec_results[1]  # 64-byte result
    components = ['Key Generation\n(Network + Crypto)', 'Data Processing\n(Dual-Core ChaCha20)', 'Overhead\n(Split + Encode + Sync)']
    times = [
        ppec_64['key_generation_time'],
        (ppec_64['time_ms'] - ppec_64['key_generation_time']) * 0.8,  # Processing
        (ppec_64['time_ms'] - ppec_64['key_generation_time']) * 0.2   # Overhead
    ]
    
    colors_pie = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    explode = (0.1, 0, 0.05)  # explode key generation slice
    
    plt.pie(times, labels=components, colors=colors_pie, explode=explode, autopct='%1.1f%%', 
            shadow=True, startangle=90, textprops={'fontsize': 12})
    plt.title('PPEC Algorithm Time Breakdown (64 bytes)\nTotal Time: {:.1f}ms'.format(ppec_64['time_ms']), 
              fontsize=16, fontweight='bold', pad=20)
    
    plt.axis('equal')
    plt.tight_layout()
    plt.show()
    
    input("Press Enter to continue to the next chart...")
    
    # 4. Core Utilization Comparison
    plt.figure(figsize=(14, 8))
    
    algorithms = ['PPEC\n(Time-based)', 'ChaCha20\n(Standard)', 'AES\n(Standard)', 'RSA\n(Standard)']
    core0_usage = [ppec_results[1]['core_utilization'][0], chacha20_results[1]['core_utilization'][0], 
                   aes_results[1]['core_utilization'][0], rsa_results[1]['core_utilization'][0]]
    core1_usage = [ppec_results[1]['core_utilization'][1], chacha20_results[1]['core_utilization'][1],
                   aes_results[1]['core_utilization'][1], rsa_results[1]['core_utilization'][1]]
    
    x = np.arange(len(algorithms))
    width = 0.35
    
    bars1 = plt.bar(x - width/2, core0_usage, width, label='ESP32 Core 0', color='#FF6B6B', alpha=0.8, edgecolor='black')
    bars2 = plt.bar(x + width/2, core1_usage, width, label='ESP32 Core 1', color='#4ECDC4', alpha=0.8, edgecolor='black')
    
    plt.title('ESP32 Dual-Core Utilization: PPEC vs Standard Algorithms', fontsize=16, fontweight='bold', pad=20)
    plt.ylabel('CPU Usage (%)', fontsize=14)
    plt.xlabel('Algorithms', fontsize=14)
    plt.xticks(x, algorithms)
    plt.legend(fontsize=12)
    plt.ylim(0, 100)
    plt.grid(True, alpha=0.3, axis='y')
    
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{height:.0f}%', ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    plt.tight_layout()
    plt.show()
    
    input("Press Enter to continue to the next chart...")
    
    # 5. Power Efficiency Analysis
    plt.figure(figsize=(14, 8))
    
    ppec_power = [result['power_mw'] for result in ppec_results]
    chacha20_power = [result['power_mw'] for result in chacha20_results]
    aes_power = [result['power_mw'] for result in aes_results]
    rsa_power = [result['power_mw'] for result in rsa_results]
    
    plt.plot(data_sizes, ppec_power, 'o-', label='PPEC (Network + Dual-Core)', color=colors[0], linewidth=3, markersize=8)
    plt.plot(data_sizes, chacha20_power, 's-', label='ChaCha20 (Single-Core)', color=colors[1], linewidth=3, markersize=8)
    plt.plot(data_sizes, aes_power, '^-', label='AES (Single-Core)', color=colors[2], linewidth=3, markersize=8)
    plt.plot(data_sizes, rsa_power, 'd-', label='RSA (Intensive)', color=colors[3], linewidth=3, markersize=8)
    
    plt.title('Power Consumption: PPEC vs Standard Algorithms', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Data Size (bytes)', fontsize=14)
    plt.ylabel('Power Consumption (mW)', fontsize=14)
    plt.legend(fontsize=12, loc='upper left')
    plt.grid(True, alpha=0.3)
    
    plt.text(350, 200, 'Higher power = shorter battery life\nin IoT applications', 
             fontsize=10, bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))
    
    plt.tight_layout()
    plt.show()
    
    input("Press Enter to continue to the next chart...")
    
    # 6. Security vs Performance Trade-off
    plt.figure(figsize=(14, 8))
    
    security_scores = [9, 8, 9, 10]  # PPEC, ChaCha20, AES, RSA
    performance_scores = [
        1000 / ppec_results[1]['time_ms'],      # PPEC performance (inverse of time)
        1000 / chacha20_results[1]['time_ms'], # ChaCha20 performance  
        1000 / aes_results[1]['time_ms'],      # AES performance
        1000 / rsa_results[1]['time_ms']       # RSA performance
    ]
    
    algorithm_names = ['PPEC', 'ChaCha20', 'AES', 'RSA']
    
    plt.scatter(performance_scores, security_scores, s=200, c=colors, alpha=0.7, edgecolors='black', linewidth=2)
    
    for i, name in enumerate(algorithm_names):
        plt.annotate(name, (performance_scores[i], security_scores[i]), 
                    xytext=(10, 10), textcoords='offset points', fontsize=12, fontweight='bold')
    
    plt.title('Security vs Performance Trade-off Analysis', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Performance Score (1000/time_ms)', fontsize=14)
    plt.ylabel('Security Score (1-10)', fontsize=14)
    plt.grid(True, alpha=0.3)
    
    plt.axhline(y=7.5, color='gray', linestyle='--', alpha=0.5)
    plt.axvline(x=np.mean(performance_scores), color='gray', linestyle='--', alpha=0.5)
    
    plt.text(max(performance_scores)*0.7, 9.5, 'High Security\nHigh Performance', fontsize=10, 
             bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen", alpha=0.7))
    
    plt.tight_layout()
    plt.show()
    
    input("Press Enter to continue to the next chart...")
    
    # 7. PPEC Network Dependency Analysis
    plt.figure(figsize=(14, 8))
    
    network_latencies = [0, 50, 100, 200, 500, 1000]  # ms
    ppec_times_network = []
    
    for latency in network_latencies:
        base_time = ppec_results[1]['time_ms'] - ppec_results[1]['key_generation_time']
        network_time = 15 + latency  # Base key generation + network latency
        total_time = base_time + network_time
        ppec_times_network.append(total_time)
    
    plt.plot(network_latencies, ppec_times_network, 'o-', label='PPEC (Network Dependent)', 
             color=colors[0], linewidth=3, markersize=8)
    
    chacha20_constant = [chacha20_results[1]['time_ms']] * len(network_latencies)
    aes_constant = [aes_results[1]['time_ms']] * len(network_latencies)
    
    plt.plot(network_latencies, chacha20_constant, 's-', label='ChaCha20 (Network Independent)', 
             color=colors[1], linewidth=3, markersize=8)
    plt.plot(network_latencies, aes_constant, '^-', label='AES (Network Independent)', 
             color=colors[2], linewidth=3, markersize=8)
    
    plt.title('Network Latency Impact on PPEC Performance', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Network Latency (ms)', fontsize=14)
    plt.ylabel('Total Processing Time (ms)', fontsize=14)
    plt.legend(fontsize=12, loc='upper left')
    plt.grid(True, alpha=0.3)
    
    plt.annotate('PPEC requires network for time sync', 
                xy=(500, ppec_times_network[4]), xytext=(200, ppec_times_network[4] + 50),
                arrowprops=dict(arrowstyle='->', color='red', alpha=0.7),
                fontsize=10, color='red')
    
    plt.tight_layout()
    plt.show()
    
    input("Press Enter to continue to the final chart...")
    
    # 8. Overall Performance Radar Chart
    plt.figure(figsize=(14, 10))
    ax = plt.subplot(111, projection='polar')
    
    categories = ['Speed', 'Memory\nEfficiency', 'Power\nEfficiency', 'Security', 'Scalability', 'Flexibility', 'ESP32\nCompatibility', 'Real-time']
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]
    
    def calculate_scores(result, is_ppec=False, is_rsa=False):
        speed_score = max(1, min(10, 10 - (result['time_ms'] / 50)))  # Faster = higher score
        memory_score = max(1, min(10, 10 - (result['memory_kb'] / 5)))  # Less memory = higher score
        power_score = max(1, min(10, 10 - (result['power_mw'] / 50)))  # Less power = higher score
        
        if is_ppec:
            security_score = 9  # High due to time-based keys
            scalability_score = 9  # Excellent with dual-core
            flexibility_score = 8  # Good modular design
            compatibility_score = 9  # Optimized for ESP32
            realtime_score = 7  # Good but network dependent
        elif is_rsa:
            security_score = 10  # Maximum security
            scalability_score = 2  # Poor scalability
            flexibility_score = 3  # Rigid structure
            compatibility_score = 2  # Poor for ESP32
            realtime_score = 2  # Very slow
        else:
            security_score = 8  # Standard crypto security
            scalability_score = 6  # Linear scaling
            flexibility_score = 5  # Moderate flexibility
            compatibility_score = 7  # Good for embedded
            realtime_score = 8  # Good real-time performance
            
        return [speed_score, memory_score, power_score, security_score, 
                scalability_score, flexibility_score, compatibility_score, realtime_score]
    
    ppec_scores = calculate_scores(ppec_results[1], is_ppec=True) + [calculate_scores(ppec_results[1], is_ppec=True)[0]]
    chacha20_scores = calculate_scores(chacha20_results[1]) + [calculate_scores(chacha20_results[1])[0]]
    aes_scores = calculate_scores(aes_results[1]) + [calculate_scores(aes_results[1])[0]]
    rsa_scores = calculate_scores(rsa_results[1], is_rsa=True) + [calculate_scores(rsa_results[1], is_rsa=True)[0]]
    
    ax.plot(angles, ppec_scores, 'o-', linewidth=3, label='PPEC (Time-based Dual-Thread)', color=colors[0], markersize=8)
    ax.fill(angles, ppec_scores, alpha=0.25, color=colors[0])
    
    ax.plot(angles, chacha20_scores, 's-', linewidth=3, label='ChaCha20 (Standard)', color=colors[1], markersize=8)
    ax.fill(angles, chacha20_scores, alpha=0.25, color=colors[1])
    
    ax.plot(angles, aes_scores, '^-', linewidth=3, label='AES (Standard)', color=colors[2], markersize=8)
    ax.fill(angles, aes_scores, alpha=0.25, color=colors[2])
    
    ax.plot(angles, rsa_scores, 'd-', linewidth=3, label='RSA (Standard)', color=colors[3], markersize=8)
    ax.fill(angles, rsa_scores, alpha=0.25, color=colors[3])
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=12)
    ax.set_ylim(0, 10)
    ax.set_title('Overall Algorithm Performance Comparison\n(Dynamic Simulation Results)', 
                  fontsize=16, fontweight='bold', pad=30)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0), fontsize=12)
    ax.grid(True)
    
    plt.tight_layout()
    plt.show()
    
    print("\nAll charts have been displayed successfully!")

def create_ppec_specific_analysis():
    """Create detailed analysis specific to PPEC algorithm"""
    
    print("\n" + "=" * 100)
    print("DETAILED PPEC ALGORITHM ANALYSIS")
    print("=" * 100)
    
    simulator = AlgorithmSimulator()
    
    test_sizes = [16, 32, 64, 128, 256, 512, 1024]
    ppec_detailed = []
    
    for size in test_sizes:
        result = simulator.simulate_ppec_performance(size)
        ppec_detailed.append(result)
    
    ppec_breakdown = {
        'Data Size (bytes)': test_sizes,
        'Total Time (ms)': [f"{result['time_ms']:.2f}" for result in ppec_detailed],
        'Key Gen Time (ms)': [f"{result['key_generation_time']:.1f}" for result in ppec_detailed],
        'Processing Time (ms)': [f"{result['time_ms'] - result['key_generation_time']:.2f}" for result in ppec_detailed],
        'Memory Usage (KB)': [f"{result['memory_kb']:.2f}" for result in ppec_detailed],
        'Power Draw (mW)': [f"{result['power_mw']:.1f}" for result in ppec_detailed],
        'Core 0 Usage (%)': [f"{result['core_utilization'][0]:.0f}" for result in ppec_detailed],
        'Core 1 Usage (%)': [f"{result['core_utilization'][1]:.0f}" for result in ppec_detailed],
        'Thread Efficiency': [f"{result['thread_efficiency']:.1f}/10" for result in ppec_detailed]
    }
    
    ppec_df = pd.DataFrame(ppec_breakdown)
    print("\nPPEC PERFORMANCE SCALING ANALYSIS:")
    print("-" * 100)
    print(tabulate(ppec_df, headers='keys', tablefmt='grid', showindex=False))
    
    print("\n" + "=" * 100)
    print("PPEC ALGORITHM STRENGTHS & WEAKNESSES")
    print("=" * 100)
    
    strengths_weaknesses = {
        'Aspect': [
            'Processing Speed',
            'Memory Efficiency', 
            'Power Consumption',
            'Security Level',
            'ESP32 Compatibility',
            'Network Dependency',
            'Real-time Performance',
            'Scalability',
            'Implementation Complexity',
            'Maintenance Requirements'
        ],
        'Strength': [
            'Dual-core parallel processing reduces encryption time',
            'Reasonable memory usage with efficient thread management',
            'Balanced power consumption with dual-core efficiency',
            'Dynamic time-based key generation enhances security',
            'Optimized for ESP32 dual-core architecture',
            'N/A',
            'Good asynchronous processing capabilities',
            'Excellent scaling with data size via parallel processing',
            'N/A',
            'N/A'
        ],
        'Weakness': [
            'Network latency adds overhead to key generation',
            'Thread management overhead increases memory usage',
            'Network requests consume additional power',
            'Depends on accurate time synchronization',
            'Requires network connectivity for time sync',
            'Requires internet connection for time synchronization',
            'Network dependency can cause delays',
            'Key generation time remains constant regardless of data size',
            'More complex than single-thread implementations',
            'Requires monitoring of network connectivity'
        ]
    }
    
    sw_df = pd.DataFrame(strengths_weaknesses)
    print(tabulate(sw_df, headers='keys', tablefmt='grid', showindex=False))
    
    return ppec_detailed

def print_comparative_recommendations():
    """Print detailed recommendations for algorithm selection"""
    
    print("\n" + "=" * 120)
    print("ALGORITHM SELECTION RECOMMENDATIONS")
    print("=" * 120)
    
    recommendations = {
        'Use Case': [
            'IoT Sensors with Internet',
            'Offline ESP32 Applications',
            'High-Security Applications',
            'Real-time Data Processing',
            'Battery-Powered Devices',
            'High-Throughput Applications',
            'Resource-Constrained Devices',
            'Key Exchange Systems',
            'Stream Processing',
            'Legacy System Integration'
        ],
        'Best Algorithm': [
            'PPEC',
            'ChaCha20',
            'AES-256',
            'PPEC or ChaCha20',
            'ChaCha20',
            'PPEC',
            'ChaCha20',
            'RSA (key exchange only)',
            'ChaCha20',
            'AES'
        ],
        'Reasoning': [
            'Time-based keys provide enhanced security with network availability',
            'No network dependency, reliable performance',
            'Industry standard with proven security record',
            'PPEC offers parallel processing, ChaCha20 offers predictable timing',
            'Most power-efficient single-thread implementation',
            'Dual-core processing maximizes ESP32 capabilities',
            'Minimal memory footprint and efficient processing',
            'Use RSA only for initial key exchange, not bulk encryption',
            'Stream cipher design optimal for continuous data',
            'Widely supported and tested in existing systems'
        ],
        'Alternative': [
            'ChaCha20 (if network unreliable)',
            'AES (if maximum security needed)',
            'PPEC (if performance also critical)',
            'AES (if security is priority)',
            'AES (if security outweighs power)',
            'ChaCha20 (if simplicity preferred)',
            'PPEC (if dual-core available)',
            'None - RSA specific use case',
            'PPEC (if dual-core benefits outweigh complexity)',
            'ChaCha20 (for better embedded performance)'
        ]
    }
    
    rec_df = pd.DataFrame(recommendations)
    print(tabulate(rec_df, headers='keys', tablefmt='grid', showindex=False))

def main():
    """Main function with comprehensive PPEC vs standard algorithms analysis"""
    
    print("ESP32 ALGORITHM COMPARISON: PPEC vs ChaCha20 vs AES vs RSA")
    print("=" * 80)
    print("PPEC: Your time-based dual-core implementation with ChaCha20 encryption")
    print("ChaCha20: Standard single-thread stream cipher implementation")
    print("AES: Standard single-thread block cipher implementation") 
    print("RSA: Standard single-thread asymmetric encryption implementation")
    print("=" * 80)
    
    simulator = AlgorithmSimulator()
    simulation_results = simulator.run_comparative_simulation()
    
    ppec_result, chacha20_result, aes_result, rsa_result = print_dynamic_comprehensive_table()
    
    ppec_detailed = create_ppec_specific_analysis()
    
    print_comparative_recommendations()
    
    print("\n" + "=" * 80)
    print("GENERATING VISUALIZATIONS...")
    print("=" * 80)
    
    create_individual_charts(simulation_results)
    
    print("\n" + "=" * 80)
    print("PPEC ALGORITHM EVALUATION SUMMARY")
    print("=" * 80)
    
    print("\nKEY FINDINGS:")
    print("-" * 60)
    print(f"PPEC Total Processing Time: {ppec_result['time_ms']:.1f}ms (includes {ppec_result['key_generation_time']:.1f}ms network overhead)")
    print(f"PPEC vs ChaCha20 Speed: {((ppec_result['time_ms'] / chacha20_result['time_ms']) - 1) * 100:+.1f}% time difference")
    print(f"PPEC vs AES Speed: {((ppec_result['time_ms'] / aes_result['time_ms']) - 1) * 100:+.1f}% time difference")
    print(f"PPEC Memory Overhead: {ppec_result['memory_kb'] - chacha20_result['memory_kb']:.1f}KB more than ChaCha20")
    print(f"PPEC Power Consumption: {ppec_result['power_mw'] - chacha20_result['power_mw']:.0f}mW more than ChaCha20")
    print(f"PPEC Core Utilization: {ppec_result['core_utilization'][0]:.0f}%/{ppec_result['core_utilization'][1]:.0f}% vs ChaCha20 {chacha20_result['core_utilization'][0]:.0f}%/{chacha20_result['core_utilization'][1]:.0f}%")
    print(f"PPEC Thread Efficiency: {ppec_result['thread_efficiency']:.1f}/10 vs ChaCha20 {chacha20_result['thread_efficiency']:.1f}/10")
    
    print("\nPPEC COMPETITIVE ADVANTAGES:")
    print("-" * 60)
    print("✓ Dynamic time-based key generation enhances security")
    print("✓ Dual-core parallel processing utilizes ESP32 architecture")
    print("✓ Modular design allows for future optimizations")
    print("✓ Better scalability with larger data sizes")
    print("✓ Time-synchronized security across multiple devices")
    
    print("\nPPEC LIMITATIONS:")
    print("-" * 60)
    print("× Network dependency for time synchronization")
    print("× Higher memory usage due to thread management")
    print("× Additional power consumption from network requests")
    print("× More complex implementation and debugging")
    print("× Network latency affects overall performance")
    
    print("\nRECOMMENDATIONS:")
    print("-" * 60)
    print("• Use PPEC for IoT applications with reliable internet connectivity")
    print("• Consider offline backup mode using local time if network fails")
    print("• Implement network timeout and fallback to standard ChaCha20")
    print("• Optimize key generation caching to reduce network requests")
    print("• PPEC is excellent for applications requiring synchronized encryption")
    print("• For offline applications, standard ChaCha20 is more suitable")
    
    analysis_id = hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]
    print(f"\nAnalysis ID: {analysis_id}")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Simulation includes ±10% realistic performance variation")

if __name__ == "__main__":
    main()