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

Clone the repository:
```bash
git clone https://github.com/rezafarazi/PPE.git
```

## Usage

### Python
```python
from PPE.Python.PPE import ParallelEncryption

# Initialize encryption
pe = ParallelEncryption()

# Encrypt data
encrypted_data = pe.encrypt("Your text here")

# Decrypt data
decrypted_data = pe.decrypt(encrypted_data)

print(decrypted_data)
```

### MicroPython
```python
from PPE.MicroPython.PPE import ParallelEncryption

# Initialize encryption
pe = ParallelEncryption()

# Encrypt data
encrypted_data = pe.encrypt("Your text here")

# Decrypt data
decrypted_data = pe.decrypt(encrypted_data)

print(decrypted_data)
```

### C++
```cpp
#include "PPE/C++/PPE.h"

int main() {
    // Initialize encryption
    PPE pe;

    // Encrypt data
    string encrypted = pe.Encrypt("Your text here");

    // Decrypt data
    string decrypted = pe.Decrypt(encrypted);

    cout << decrypted << endl;
    return 0;
}
```

### Java
```java
import PPE.Java.PPE;

public class Main {
    public static void main(String[] args) {
        // Initialize encryption
        PPE pe = new PPE();

        // Encrypt data
        String encrypted = pe.Encrypt("Your text here");

        // Decrypt data
        String decrypted = pe.Decrypt(encrypted);

        System.out.println(decrypted);
    }
}
```

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
Made with ❤️ by the PPE Library Team
