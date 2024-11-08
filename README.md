# PPE (Parallel Processing Encryption) Library

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/rezafarazi/PPE/blob/main/LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/downloads/)
[![MicroPython](https://img.shields.io/badge/micropython-1.19%2B-green)](https://micropython.org/)

PPE is a cross-platform encryption library that leverages parallel processing to provide high-performance encryption and decryption capabilities. It's available for Python, MicroPython, C++, and Java, making it versatile for various applications from embedded systems to high-performance servers.

## Features

- **Multi-platform Support**: Run on any platform that supports Python, MicroPython, C++, or Java
- **Parallel Processing**: Utilize multiple cores for faster encryption/decryption operations
- **Multiple Encryption Algorithms**:
  - AES (128/256-bit)
  - ChaCha20
  - Blowfish
  - Custom hybrid encryption modes
- **Memory Efficient**: Optimized for both resource-constrained and high-performance systems
- **Thread Safety**: Safe for concurrent operations
- **Streaming Support**: Process large files without loading them entirely into memory

## Installation

### Python
```bash
pip install ppe-lib
```

### MicroPython
```bash
mpremote mip install ppe-lib
```

### C++
```bash
git clone https://github.com/rezafarazi/PPE.git
cd ppe/cpp
cmake .
make install
```

### Java
```xml
<dependency>
    <groupId>com.ppelib</groupId>
    <artifactId>ppe-core</artifactId>
    <version>1.0.0</version>
</dependency>
```

## Quick Start

### Python
```python
from ppe import ParallelEncryption

# Initialize with number of processes
pe = ParallelEncryption(processes=4)

# Encrypt data
encrypted_data = pe.encrypt(data, key)

# Decrypt data
decrypted_data = pe.decrypt(encrypted_data, key)
```

### MicroPython
```python
from ppe_micro import ParallelEncryption

# Initialize (automatically detects core count)
pe = ParallelEncryption()

# Encrypt data
encrypted_data = pe.encrypt(data, key)
```

### C++
```cpp
#include <ppe/parallel_encryption.hpp>

// Initialize with thread count
PPE::ParallelEncryption pe(4);

// Encrypt data
std::vector<uint8_t> encrypted = pe.encrypt(data, key);
```

### Java
```java
import com.ppelib.ParallelEncryption;

// Initialize with thread count
ParallelEncryption pe = new ParallelEncryption(4);

// Encrypt data
byte[] encrypted = pe.encrypt(data, key);
```

## Advanced Usage

### Custom Encryption Modes
```python
from ppe import ParallelEncryption, EncryptionMode

pe = ParallelEncryption(
    mode=EncryptionMode.HYBRID,
    block_size=1024,
    parallel_blocks=8
)
```

### Stream Processing
```python
with pe.encrypt_stream('input.file', 'encrypted.file', key) as stream:
    stream.process_chunks()
```

## Performance Considerations

- Optimal performance is achieved with data sizes > 1MB
- Default chunk size is optimized for most use cases
- Thread count should match available CPU cores
- Memory usage scales linearly with chunk size × thread count

## Contributing

1. Fork the repository from [https://github.com/rezafarazi/PPE](https://github.com/rezafarazi/PPE)
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Security Considerations

- All encryption keys should be properly generated using cryptographically secure methods
- The library uses standard encryption algorithms from trusted cryptographic libraries
- Regular security audits are performed
- See SECURITY.md for vulnerability reporting

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/rezafarazi/PPE/blob/main/LICENSE) file for details.

## Support

- Documentation: [PPE Wiki](https://github.com/rezafarazi/PPE/wiki)
- Issue Tracker: [GitHub Issues](https://github.com/rezafarazi/PPE/issues)
- Discussion Forum: [GitHub Discussions](https://github.com/rezafarazi/PPE/discussions)

## Acknowledgments

- OpenSSL for core cryptographic operations
- The MicroPython community for embedded systems support
- Contributors and maintainers

---
Made with ❤️ by the Rezafta
