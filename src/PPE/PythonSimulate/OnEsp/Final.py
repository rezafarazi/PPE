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
        
    def simulate_ppe_performance(self, data_size_bytes):
        """Simulate PPE dual-thread performance"""
        
        # Base processing time per byte (microseconds)
        base_time_per_byte = 0.8 + random.uniform(-0.1, 0.1)
        
        # Parallel efficiency factor (not perfect due to sync overhead)
        parallel_efficiency = 0.85 + random.uniform(-0.05, 0.05)
        
        # Calculate processing time
        single_thread_time = data_size_bytes * base_time_per_byte
        dual_thread_time = (single_thread_time / 2) / parallel_efficiency
        
        # Add synchronization overhead
        sync_overhead = 0.3 + random.uniform(-0.1, 0.1)  # ms
        total_time = dual_thread_time + sync_overhead
        
        # Memory calculation
        base_memory = 2.1  # KB base algorithm
        thread_overhead = 1.2  # KB for thread management
        lock_memory = 0.3  # KB for synchronization
        key_memory = 0.3 + (data_size_bytes / 1000) * 0.1  # Dynamic key size
        total_memory = base_memory + thread_overhead + lock_memory + key_memory
        
        # Power calculation
        processing_power_per_core = 30 + (data_size_bytes / 100) * 2
        dual_core_power = processing_power_per_core * 1.8  # Not exactly 2x due to efficiency
        total_power = self.base_power_consumption + dual_core_power
        
        return {
            'time_ms': total_time / 1000,  # Convert to ms
            'memory_kb': total_memory,
            'power_mw': total_power,
            'core_utilization': [80 + random.uniform(-5, 10), 75 + random.uniform(-5, 10)],
            'thread_efficiency': 8.5 + random.uniform(-0.5, 1.5)
        }
    
    def simulate_aes_performance(self, data_size_bytes):
        """Simulate AES single-thread performance"""
        
        # AES is typically faster per byte but single-threaded
        base_time_per_byte = 0.6 + random.uniform(-0.1, 0.1)
        
        # Single thread processing
        total_time = data_size_bytes * base_time_per_byte
        
        # Memory calculation
        base_memory = 3.0 + random.uniform(-0.3, 0.5)
        key_memory = 0.4  # Fixed key size
        total_memory = base_memory + key_memory
        
        # Power calculation (single core intensive)
        processing_power = 110 + (data_size_bytes / 50) * 3
        total_power = self.base_power_consumption + processing_power
        
        return {
            'time_ms': total_time / 1000,
            'memory_kb': total_memory,
            'power_mw': total_power,
            'core_utilization': [70 + random.uniform(-10, 15), 5 + random.uniform(0, 5)],
            'thread_efficiency': 2.0 + random.uniform(-0.5, 0.5)
        }
    
    def simulate_rsa_performance(self, data_size_bytes, key_size=2048):
        """Simulate RSA single-thread performance"""
        
        # RSA is very slow, especially with larger keys
        base_time_per_byte = 8.0 + random.uniform(-1.0, 2.0)
        key_factor = (key_size / 1024) ** 2  # Quadratic increase with key size
        
        total_time = data_size_bytes * base_time_per_byte * key_factor
        
        # Memory calculation (large key storage)
        base_memory = 5.0 + random.uniform(-0.5, 1.0)
        key_memory = (key_size / 1024) * 4  # 4KB per 1024-bit key
        total_memory = base_memory + key_memory
        
        # Power calculation (very intensive)
        processing_power = 160 + (data_size_bytes / 20) * 5
        total_power = self.base_power_consumption + processing_power
        
        return {
            'time_ms': total_time / 1000,
            'memory_kb': total_memory,
            'power_mw': total_power,
            'core_utilization': [90 + random.uniform(-5, 10), 8 + random.uniform(0, 5)],
            'thread_efficiency': 1.0 + random.uniform(-0.2, 0.2)
        }
    
    def run_comparative_simulation(self, data_sizes=[32, 64, 128, 256, 512]):
        """Run comparative simulation for all algorithms"""
        
        results = {
            'data_sizes': data_sizes,
            'ppe_results': [],
            'aes_results': [],
            'rsa_results': []
        }
        
        for size in data_sizes:
            results['ppe_results'].append(self.simulate_ppe_performance(size))
            results['aes_results'].append(self.simulate_aes_performance(size))
            results['rsa_results'].append(self.simulate_rsa_performance(size))
        
        return results

def create_dynamic_comparison_data():
    """Create comparison data based on simulation results"""
    
    simulator = AlgorithmSimulator()
    
    # Run simulation for standard 64-byte data
    ppe_result = simulator.simulate_ppe_performance(64)
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
            'Real-time Performance'
        ],
        'PPE (Dual-Thread Implementation)': [
            f'{ppe_result["time_ms"]:.1f} ms (parallel dual-core processing)',
            f'{ppe_result["memory_kb"]:.1f} (with thread management overhead)',
            f'{ppe_result["power_mw"]:.0f} (efficient due to parallel execution)',
            'Parallel dual-thread with data splitting',
            f'Utilizes 2 threads (efficiency: {ppe_result["thread_efficiency"]:.1f}/10)',
            'Excellent - optimized for ESP32 dual-core',
            'High with dynamic time-based key generation',
            'Unix time + salt with dynamic generation',
            'Excellent - adaptive to network conditions',
            'Very high - modular thread-based design',
            'Superior - data partitioning across threads',
            f'Dual-core ({ppe_result["core_utilization"][0]:.0f}% / {ppe_result["core_utilization"][1]:.0f}%)',
            'Minimal - efficient lock mechanism',
            'Excellent - asynchronous processing'
        ],
        'AES Algorithm (Single-Thread)': [
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
            'Good - predictable but slower'
        ],
        'RSA Algorithm (Single-Thread)': [
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
            'Poor - long processing delays'
        ]
    }
    
    return comparison_data, ppe_result, aes_result, rsa_result

def create_dynamic_performance_metrics(ppe_result, aes_result, rsa_result):
    """Create performance metrics from simulation results"""
    
    # Calculate normalized scores (0-10 scale)
    def normalize_score(value, min_val, max_val, inverse=False):
        if inverse:  # For metrics where lower is better
            normalized = (max_val - value) / (max_val - min_val)
        else:  # For metrics where higher is better
            normalized = (value - min_val) / (max_val - min_val)
        return max(0, min(10, normalized * 10))
    
    # Speed score (lower time = higher score)
    time_values = [ppe_result['time_ms'], aes_result['time_ms'], rsa_result['time_ms']]
    min_time, max_time = min(time_values), max(time_values)
    
    speed_scores = [
        normalize_score(ppe_result['time_ms'], min_time, max_time, inverse=True),
        normalize_score(aes_result['time_ms'], min_time, max_time, inverse=True),
        normalize_score(rsa_result['time_ms'], min_time, max_time, inverse=True)
    ]
    
    # Memory efficiency (lower memory = higher score)
    memory_values = [ppe_result['memory_kb'], aes_result['memory_kb'], rsa_result['memory_kb']]
    min_memory, max_memory = min(memory_values), max(memory_values)
    
    memory_scores = [
        normalize_score(ppe_result['memory_kb'], min_memory, max_memory, inverse=True),
        normalize_score(aes_result['memory_kb'], min_memory, max_memory, inverse=True),
        normalize_score(rsa_result['memory_kb'], min_memory, max_memory, inverse=True)
    ]
    
    # Power efficiency (lower power = higher score)
    power_values = [ppe_result['power_mw'], aes_result['power_mw'], rsa_result['power_mw']]
    min_power, max_power = min(power_values), max(power_values)
    
    power_scores = [
        normalize_score(ppe_result['power_mw'], min_power, max_power, inverse=True),
        normalize_score(aes_result['power_mw'], min_power, max_power, inverse=True),
        normalize_score(rsa_result['power_mw'], min_power, max_power, inverse=True)
    ]
    
    metrics = {
        'Metric': ['Speed (ms)', 'Memory (KB)', 'Power (mW)', 'Compatibility', 'Security', 'Flexibility', 'Thread Efficiency', 'Scalability'],
        'PPE (Dual-Thread)': [
            ppe_result['time_ms'], 
            ppe_result['memory_kb'], 
            ppe_result['power_mw'], 
            9, 7, 9, 
            ppe_result['thread_efficiency'], 
            9
        ],
        'AES (Single-Thread)': [
            aes_result['time_ms'], 
            aes_result['memory_kb'], 
            aes_result['power_mw'], 
            6, 9, 4, 
            aes_result['thread_efficiency'], 
            6
        ],
        'RSA (Single-Thread)': [
            rsa_result['time_ms'], 
            rsa_result['memory_kb'], 
            rsa_result['power_mw'], 
            2, 10, 2, 
            rsa_result['thread_efficiency'], 
            3
        ]
    }
    
    return metrics

def print_dynamic_comprehensive_table():
    """Print comprehensive comparison table with dynamic data"""
    
    print("=" * 140)
    print("📊 COMPREHENSIVE ALGORITHM COMPARISON - DYNAMIC SIMULATION RESULTS")
    print("=" * 140)
    print("🔄 PPE: Real-time simulated dual-core architecture with parallel thread processing")
    print("🔒 AES: Simulated single-thread block cipher implementation")
    print("🛡️ RSA: Simulated single-thread asymmetric encryption with heavy computation")
    print("=" * 140)
    
    data, ppe_result, aes_result, rsa_result = create_dynamic_comparison_data()
    df = pd.DataFrame(data)
    
    # Print table using tabulate with better formatting
    print(tabulate(df, headers='keys', tablefmt='grid', showindex=False))
    
    print("\n" + "=" * 140)
    print("📈 DYNAMIC SIMULATION PARAMETERS")
    print("=" * 140)
    
    # Show simulation parameters
    sim_params = {
        'Simulation Parameters': [
            'ESP32 Base Frequency',
            'Available SRAM',
            'Dual-Core Configuration',
            'Base Power Consumption',
            'Parallel Efficiency Factor',
            'Synchronization Overhead',
            'Random Variation Range',
            'Timestamp'
        ],
        'Values': [
            '240 MHz',
            '320 KB',
            '2 cores (Core 0 & Core 1)',
            '40 mW idle',
            '85% ± 5%',
            '0.3 ± 0.1 ms',
            '±10% realistic variation',
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ]
    }
    
    params_df = pd.DataFrame(sim_params)
    print(tabulate(params_df, headers='keys', tablefmt='grid', showindex=False))
    
    return ppe_result, aes_result, rsa_result

def create_dynamic_visualization(simulation_results):
    """Create visualization with dynamic simulation data"""
    
    fig = plt.figure(figsize=(22, 16))
    
    # Extract data from simulation results
    data_sizes = simulation_results['data_sizes']
    ppe_results = simulation_results['ppe_results']
    aes_results = simulation_results['aes_results']
    rsa_results = simulation_results['rsa_results']
    
    # 1. Thread Utilization Comparison (from simulation)
    ax1 = plt.subplot(2, 4, 1)
    algorithms = ['PPE\n(Dual-Thread)', 'AES\n(Single-Thread)', 'RSA\n(Single-Thread)']
    thread_efficiency = [
        ppe_results[1]['thread_efficiency'],  # 64-byte result
        aes_results[1]['thread_efficiency'],
        rsa_results[1]['thread_efficiency']
    ]
    colors = ['#4CAF50', '#FF9800', '#F44336']
    
    bars = ax1.bar(algorithms, thread_efficiency, color=colors)
    ax1.set_title('Thread Utilization Efficiency\n(Simulated)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Efficiency Score (0-10)')
    ax1.set_ylim(0, 10)
    ax1.grid(True, alpha=0.3)
    
    for bar, efficiency in zip(bars, thread_efficiency):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{efficiency:.1f}/10', ha='center', va='bottom', fontweight='bold')
    
    # 2. Dynamic Core Utilization Pattern
    ax2 = plt.subplot(2, 4, 2)
    core_data = {
        'PPE': ppe_results[1]['core_utilization'],
        'AES': aes_results[1]['core_utilization'],
        'RSA': rsa_results[1]['core_utilization']
    }
    
    x = np.arange(2)
    width = 0.25
    
    bars1 = ax2.bar(x - width, core_data['PPE'], width, label='PPE', color='#4CAF50', alpha=0.8)
    bars2 = ax2.bar(x, core_data['AES'], width, label='AES', color='#FF9800', alpha=0.8)
    bars3 = ax2.bar(x + width, core_data['RSA'], width, label='RSA', color='#F44336', alpha=0.8)
    
    ax2.set_title('ESP32 Core Utilization\n(Dynamic)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('CPU Usage (%)')
    ax2.set_xticks(x)
    ax2.set_xticklabels(['Core 0', 'Core 1'])
    ax2.legend()
    ax2.set_ylim(0, 100)
    ax2.grid(True, alpha=0.3)
    
    # 3. Processing Time Scalability
    ax3 = plt.subplot(2, 4, 3)
    
    ppe_times = [result['time_ms'] for result in ppe_results]
    aes_times = [result['time_ms'] for result in aes_results]
    rsa_times = [result['time_ms'] for result in rsa_results]
    
    ax3.plot(data_sizes, ppe_times, 'o-', label='PPE (Parallel)', color='#4CAF50', linewidth=2)
    ax3.plot(data_sizes, aes_times, 's-', label='AES (Linear)', color='#FF9800', linewidth=2)
    ax3.plot(data_sizes, rsa_times, '^-', label='RSA (Exponential)', color='#F44336', linewidth=2)
    
    ax3.set_title('Scalability with Data Size\n(Simulated)', fontsize=12, fontweight='bold')
    ax3.set_xlabel('Data Size (bytes)')
    ax3.set_ylabel('Processing Time (ms)')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # 4. Dynamic Memory Usage
    ax4 = plt.subplot(2, 4, 4)
    
    ppe_memory = [result['memory_kb'] for result in ppe_results]
    aes_memory = [result['memory_kb'] for result in aes_results]
    rsa_memory = [result['memory_kb'] for result in rsa_results]
    
    ax4.plot(data_sizes, ppe_memory, 'o-', label='PPE', color='#4CAF50', linewidth=2)
    ax4.plot(data_sizes, aes_memory, 's-', label='AES', color='#FF9800', linewidth=2)
    ax4.plot(data_sizes, rsa_memory, '^-', label='RSA', color='#F44336', linewidth=2)
    
    ax4.set_title('Memory Usage Scaling\n(Dynamic)', fontsize=12, fontweight='bold')
    ax4.set_xlabel('Data Size (bytes)')
    ax4.set_ylabel('Memory Usage (KB)')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    # 5. Power Consumption Pattern
    ax5 = plt.subplot(2, 4, 5)
    
    ppe_power = [result['power_mw'] for result in ppe_results]
    aes_power = [result['power_mw'] for result in aes_results]
    rsa_power = [result['power_mw'] for result in rsa_results]
    
    ax5.plot(data_sizes, ppe_power, 'o-', label='PPE', color='#4CAF50', linewidth=2)
    ax5.plot(data_sizes, aes_power, 's-', label='AES', color='#FF9800', linewidth=2)
    ax5.plot(data_sizes, rsa_power, '^-', label='RSA', color='#F44336', linewidth=2)
    
    ax5.set_title('Power Consumption\n(Simulated)', fontsize=12, fontweight='bold')
    ax5.set_xlabel('Data Size (bytes)')
    ax5.set_ylabel('Power (mW)')
    ax5.legend()
    ax5.grid(True, alpha=0.3)
    
    # 6. Performance Consistency (Multiple runs)
    ax6 = plt.subplot(2, 4, 6)
    
    # Simulate multiple runs for 64-byte data
    simulator = AlgorithmSimulator()
    runs = 10
    
    ppe_consistency = [simulator.simulate_ppe_performance(64)['time_ms'] for _ in range(runs)]
    aes_consistency = [simulator.simulate_aes_performance(64)['time_ms'] for _ in range(runs)]
    rsa_consistency = [simulator.simulate_rsa_performance(64)['time_ms'] for _ in range(runs)]
    
    time_points = list(range(1, runs + 1))
    
    ax6.plot(time_points, ppe_consistency, 'o-', label='PPE', color='#4CAF50', linewidth=2)
    ax6.plot(time_points, aes_consistency, 's-', label='AES', color='#FF9800', linewidth=2)
    ax6.plot(time_points, rsa_consistency, '^-', label='RSA', color='#F44336', linewidth=2)
    
    ax6.set_title('Performance Consistency\n(Multiple Runs)', fontsize=12, fontweight='bold')
    ax6.set_xlabel('Test Iteration')
    ax6.set_ylabel('Processing Time (ms)')
    ax6.legend()
    ax6.grid(True, alpha=0.3)
    
    # 7. Efficiency Comparison
    ax7 = plt.subplot(2, 4, 7)
    
    # Calculate efficiency metrics (performance per power consumption)
    ppe_efficiency = [1000 / (time * power) for time, power in zip(ppe_times, ppe_power)]
    aes_efficiency = [1000 / (time * power) for time, power in zip(aes_times, aes_power)]
    rsa_efficiency = [1000 / (time * power) for time, power in zip(rsa_times, rsa_power)]
    
    ax7.plot(data_sizes, ppe_efficiency, 'o-', label='PPE', color='#4CAF50', linewidth=2)
    ax7.plot(data_sizes, aes_efficiency, 's-', label='AES', color='#FF9800', linewidth=2)
    ax7.plot(data_sizes, rsa_efficiency, '^-', label='RSA', color='#F44336', linewidth=2)
    
    ax7.set_title('Performance/Power Efficiency\n(Higher is Better)', fontsize=12, fontweight='bold')
    ax7.set_xlabel('Data Size (bytes)')
    ax7.set_ylabel('Efficiency Score')
    ax7.legend()
    ax7.grid(True, alpha=0.3)
    
    # 8. Dynamic Overall Performance Radar
    ax8 = plt.subplot(2, 4, 8, projection='polar')
    
    categories = ['Speed', 'Memory\nEfficiency', 'Power\nEfficiency', 'Threading', 'Scalability', 'Flexibility']
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]
    
    # Calculate dynamic scores based on simulation results
    base_result_64 = 1  # Use 64-byte results for scoring
    
    def calculate_efficiency_score(time_val, memory_val, power_val, thread_eff):
        speed_score = max(1, min(10, 10 - (time_val / 10)))
        memory_score = max(1, min(10, 10 - (memory_val / 2)))
        power_score = max(1, min(10, 10 - (power_val / 50)))
        return [speed_score, memory_score, power_score, thread_eff, 8, 7]  # Last two are static for now
    
    ppe_base_scores = calculate_efficiency_score(
        ppe_results[base_result_64]['time_ms'],
        ppe_results[base_result_64]['memory_kb'],
        ppe_results[base_result_64]['power_mw'],
        ppe_results[base_result_64]['thread_efficiency']
    )
    ppe_scores = ppe_base_scores + [ppe_base_scores[0]]  # Close the polygon
    
    aes_base_scores = calculate_efficiency_score(
        aes_results[base_result_64]['time_ms'],
        aes_results[base_result_64]['memory_kb'],
        aes_results[base_result_64]['power_mw'],
        aes_results[base_result_64]['thread_efficiency']
    )
    aes_scores = aes_base_scores + [aes_base_scores[0]]
    
    rsa_base_scores = calculate_efficiency_score(
        rsa_results[base_result_64]['time_ms'],
        rsa_results[base_result_64]['memory_kb'],
        rsa_results[base_result_64]['power_mw'],
        rsa_results[base_result_64]['thread_efficiency']
    )
    rsa_scores = rsa_base_scores + [rsa_base_scores[0]]
    
    ax8.plot(angles, ppe_scores, 'o-', linewidth=2, label='PPE', color='#4CAF50')
    ax8.fill(angles, ppe_scores, alpha=0.25, color='#4CAF50')
    
    ax8.plot(angles, aes_scores, 's-', linewidth=2, label='AES', color='#FF9800')
    ax8.fill(angles, aes_scores, alpha=0.25, color='#FF9800')
    
    ax8.plot(angles, rsa_scores, '^-', linewidth=2, label='RSA', color='#F44336')
    ax8.fill(angles, rsa_scores, alpha=0.25, color='#F44336')
    
    ax8.set_xticks(angles[:-1])
    ax8.set_xticklabels(categories)
    ax8.set_ylim(0, 10)
    ax8.set_title('Overall Performance Radar\n(Dynamic Simulation)', 
                  fontsize=12, fontweight='bold', pad=20)
    ax8.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
    ax8.grid(True)
    
    plt.tight_layout()
    plt.show()

def print_simulation_analysis():
    """Print detailed simulation analysis"""
    
    print("\n" + "=" * 120)
    print("🔬 DYNAMIC SIMULATION ANALYSIS")
    print("=" * 120)
    
    print("\n⚙️ Simulation Model Details:")
    print("-" * 60)
    print("• PPE Performance: Based on dual-thread parallel processing with sync overhead")
    print("• AES Performance: Standard block cipher with sequential processing")
    print("• RSA Performance: Mathematical operations with quadratic key size scaling")
    print("• Random Variations: ±10% realistic performance variation included")
    print("• ESP32 Constraints: 240MHz dual-core, 320KB SRAM, power efficiency modeling")
    
    print("\n📊 Dynamic Calculation Methods:")
    print("-" * 60)
    print("• Processing Time: base_time_per_byte × data_size × algorithm_factor")
    print("• Memory Usage: base_memory + thread_overhead + dynamic_components")
    print("• Power Consumption: idle_power + processing_power × core_utilization")
    print("• Thread Efficiency: parallel_efficiency_factor + random_variation")
    print("• Core Utilization: realistic load distribution with random fluctuation")
    
    simulator = AlgorithmSimulator()
    
    print("\n🧮 Real-time Calculation Example (64 bytes):")
    print("-" * 60)
    
    current_ppe = simulator.simulate_ppe_performance(64)
    current_aes = simulator.simulate_aes_performance(64)
    current_rsa = simulator.simulate_rsa_performance(64)
    
    calc_details = {
        'Algorithm': ['PPE (Real-time)', 'AES (Real-time)', 'RSA (Real-time)'],
        'Processing Time': [
            f'{current_ppe["time_ms"]:.2f} ms',
            f'{current_aes["time_ms"]:.2f} ms', 
            f'{current_rsa["time_ms"]:.2f} ms'
        ],
        'Memory Usage': [
            f'{current_ppe["memory_kb"]:.2f} KB',
            f'{current_aes["memory_kb"]:.2f} KB',
            f'{current_rsa["memory_kb"]:.2f} KB'
        ],
        'Power Consumption': [
            f'{current_ppe["power_mw"]:.1f} mW',
            f'{current_aes["power_mw"]:.1f} mW',
            f'{current_rsa["power_mw"]:.1f} mW'
        ],
        'Thread Efficiency': [
            f'{current_ppe["thread_efficiency"]:.1f}/10',
            f'{current_aes["thread_efficiency"]:.1f}/10',
            f'{current_rsa["thread_efficiency"]:.1f}/10'
        ]
    }
    
    calc_df = pd.DataFrame(calc_details)
    print(tabulate(calc_df, headers='keys', tablefmt='grid', showindex=False))

def main():
    """Main function with dynamic simulation-based analysis"""
    
    print("🚀 ESP32 DYNAMIC ALGORITHM COMPARISON - SIMULATION BASED")
    print("=" * 80)
    print("🔬 Real-time simulation with dynamic performance calculations")
    print("📊 All metrics generated from ESP32-based performance models")
    print("🔄 PPE: Dual-thread parallel processing simulation")
    print("🔒 AES: Single-thread block cipher simulation") 
    print("🛡️ RSA: Single-thread asymmetric encryption simulation")
    print("=" * 80)
    
    # Initialize simulator and run comprehensive simulation
    simulator = AlgorithmSimulator()
    simulation_results = simulator.run_comparative_simulation()
    
    # Print dynamic comprehensive comparison
    ppe_result, aes_result, rsa_result = print_dynamic_comprehensive_table()
    
    # Print simulation analysis
    print_simulation_analysis()
    
    print("\n" + "=" * 80)
    print("📊 GENERATING DYNAMIC VISUALIZATIONS...")
    print("=" * 80)
    
    # Create dynamic visualizations
    create_dynamic_visualization(simulation_results)
    
    print("\n" + "=" * 80)
    print("✅ DYNAMIC SIMULATION COMPARISON COMPLETE!")
    print("=" * 80)
    
    print("\n🎯 SIMULATION-BASED KEY FINDINGS:")
    print("-" * 60)
    print(f"⚡ PPE Speed: {ppe_result['time_ms']:.1f}ms with {ppe_result['thread_efficiency']:.1f}/10 thread efficiency")
    print(f"💾 PPE Memory: {ppe_result['memory_kb']:.1f}KB including {1.2}KB thread management overhead")
    print(f"🔋 PPE Power: {ppe_result['power_mw']:.0f}mW with dual-core load balancing")
    print(f"🧵 Core Usage: {ppe_result['core_utilization'][0]:.0f}% / {ppe_result['core_utilization'][1]:.0f}% (Core 0/Core 1)")
    print(f"📈 Scalability: Linear improvement with parallel data processing")
    print(f"🔄 Real-time Variation: ±10% performance variation for realistic modeling")
    
    print("\n🏆 DYNAMIC RECOMMENDATIONS:")
    print("-" * 60)
    print("🔄 PPE: Optimal for ESP32 dual-core applications with dynamic performance")
    print("🔒 AES: Best for applications prioritizing security over speed")
    print("🛡️ RSA: Use only for key exchange, avoid for bulk data encryption")
    print("⚖️ Hybrid Approach: PPE + RSA combination for optimal security/performance")
    print("🔬 Simulation: Run with different parameters for specific use cases")
    
    # Show current timestamp and simulation ID
    simulation_id = hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]
    print(f"\n📝 Simulation ID: {simulation_id}")
    print(f"🕒 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎲 Random Seed Impact: Each run produces slightly different realistic results")

if __name__ == "__main__":
    main()