import network
import time
import ucryptolib
import ubinascii
import _thread
import hashlib


# Global variables
results = {'Left_Cipher': None, 'Right_Cipher': None, 'Left_Text': None, 'Right_Text': None}
lock = _thread.allocate_lock()

# --------------------------------------------------WIFI functions---------------------------------------------#

def connect_wifi(ssid, password):
    """Connects the device to a specified Wi-Fi network."""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to network...')
        wlan.connect(ssid, password)
        max_attempts = 10
        attempt = 0
        while not wlan.isconnected() and attempt < max_attempts:
            time.sleep(1)
            attempt += 1
    
    if wlan.isconnected():
        print('Connected successfully!')
        print('Network config:', wlan.ifconfig())
    else:
        print('Failed to connect')

connect_wifi('Reza', '----')

# --------------------------------------------------Key generation functions---------------------------------------------#
import urequests
import json

def get_unix_time():
    """Fetches the current Unix time from an external server."""
    try:
        response = urequests.get("https://worldtimeapi.org/api/timezone/asia/tehran")
        if response.status_code == 200:
            data = response.json()
            unix_time = data.get('unixtime', 'N/A')
            response.close()
            return unix_time
        else:
            response.close()
            return 'N/A'
    except Exception as e:
        return 'N/A'

def get_current_time_key(salt):
    """Generates a key based on the current Unix time and a salt."""
    keybase = ""
    unix_time_str = str(get_unix_time())
    
    if unix_time_str == 'N/A' or not unix_time_str.isdigit():
        # Handle case where unix time is not available or invalid
        return b'\0' * 16  # AES needs 16-byte key
    
    timestep8 = unix_time_str[:8]
    key_chars = list(timestep8)
    
    # Optimize string generation
    parts = [
        timestep8,
        ''.join(reversed(key_chars)),
        ''.join(key_chars),
        ''.join(reversed(key_chars)),
        ''.join(key_chars),
        ''.join(reversed(key_chars)),
        ''.join(key_chars),
        ''.join(reversed(key_chars)),
        ''.join(key_chars),
        ''.join(reversed(key_chars)),
        ''.join(key_chars),
        ''.join(reversed(key_chars)),
        ''.join(key_chars),
    ]
    keybase = ''.join(parts)
    
    key = ""
    for i in range(0, len(keybase) // 2, 2):
        num_a = keybase[i]
        num_b = keybase[i+1]
        add_num = int(num_a + num_b)
        key_char = chr(add_num)
        key += key_char
    
    # Combine with salt and use SHA-256 to generate 16-byte key for AES
    combined_key = salt + key
    hash_obj = hashlib.sha256(combined_key.encode('utf-8'))
    final_key = hash_obj.digest()[:16]  # Take first 16 bytes for AES-128
    
    return final_key

def generate_iv():
    """Generates a random 16-byte IV for AES."""
    import uos
    return uos.urandom(16)

# --------------------------------------------------Encryption/Decryption utilities---------------------------------------------#

def pad_data(data):
    """Pads data to be multiple of 16 bytes for AES."""
    pad_length = 16 - (len(data) % 16)
    return data + bytes([pad_length] * pad_length)

def unpad_data(data):
    """Removes padding from decrypted data."""
    pad_length = data[-1]
    return data[:-pad_length]

def single_core_encrypt(data, key):
    """Encrypts data using AES on a single core."""
    iv = generate_iv()
    
    # Pad the data
    plaintext_bytes = pad_data(data.encode('utf-8'))
    
    # Create AES cipher in CBC mode
    cipher = ucryptolib.aes(key, 2, iv)  # Mode 2 is CBC
    ciphertext = cipher.encrypt(plaintext_bytes)
    
    # Combine IV and ciphertext for storage
    combined = iv + ciphertext
    return ubinascii.b2a_base64(combined).decode('utf-8')

def single_core_decrypt(enc_data, key):
    """Decrypts data using AES on a single core."""
    # Decode the base64 data
    combined = ubinascii.a2b_base64(enc_data.encode('utf-8'))
    
    # Extract IV (first 16 bytes) and ciphertext
    iv = combined[:16]
    ciphertext = combined[16:]
    
    # Decrypt
    cipher = ucryptolib.aes(key, 2, iv)  # Mode 2 is CBC
    decrypted_bytes = cipher.decrypt(ciphertext)
    
    # Remove padding and return
    unpadded_data = unpad_data(decrypted_bytes)
    return unpadded_data.decode('utf-8')

# --------------------------------------------------Multi-core encryption/decryption functions---------------------------------------------#

def encrypt_left_thread(data, key):
    """Thread function to encrypt the left part of the data."""
    result = single_core_encrypt(data, key)
    with lock:
        results['Left_Cipher'] = result

def encrypt_right_thread(data, key):
    """Thread function to encrypt the right part of the data."""
    result = single_core_encrypt(data, key)
    with lock:
        results['Right_Cipher'] = result


def multi_core_encrypt(data, key):
    """Splits data and encrypts it in parallel using two cores."""
    midpoint = len(data) // 2
    left_data = data[:midpoint]
    right_data = data[midpoint:]
    
    _thread.start_new_thread(encrypt_left_thread, (left_data, key))
    _thread.start_new_thread(encrypt_right_thread, (right_data, key))
    
    # Wait for threads to finish
    while True:
        with lock:
            if results['Left_Cipher'] and results['Right_Cipher']:
                break
        time.sleep(0.005)
    
    cipher = f"{results['Left_Cipher']}~|~{results['Right_Cipher']}"
    cipher = cipher.replace("\n", "").replace("\r", "")
    encoded_bytes = ubinascii.b2a_base64(cipher.encode('utf-8'))
    encoded_string = encoded_bytes.decode('utf-8')
    
    # Reset results for next use
    results['Left_Cipher'] = None
    results['Right_Cipher'] = None
    
    return encoded_string

def decrypt_left_thread(data, key):
    """Thread function to decrypt the left part of the data."""
    result = single_core_decrypt(data, key)
    with lock:
        results['Left_Text'] = result

def decrypt_right_thread(data, key):
    """Thread function to decrypt the right part of the data."""
    result = single_core_decrypt(data, key)
    with lock:
        results['Right_Text'] = result


def multi_core_decrypt(data, key):
    """Splits encrypted data and decrypts it in parallel using two cores."""
    ciphers = ubinascii.a2b_base64(data).decode('utf-8')
    main_cipher = ciphers.split('~|~')
    
    _thread.start_new_thread(decrypt_left_thread, (main_cipher[0], key))
    _thread.start_new_thread(decrypt_right_thread, (main_cipher[1], key))
    
    # Wait for threads to finish
    while True:
        with lock:
            if results['Left_Text'] and results['Right_Text']:
                break
        time.sleep(0.005)
    
    # Combine and clean the results
    decrypted_text = results['Left_Text'] + results['Right_Text']
    
    # Reset results for next use
    results['Left_Text'] = None
    results['Right_Text'] = None
    
    return decrypted_text

# --------------------------------------------------Main functions---------------------------------------------#


def parallel_process_encrypt(input_text, salt):
    """Main function to perform parallel encryption."""
    key = get_current_time_key(salt)
    return multi_core_encrypt(input_text, key)

def parallel_process_decrypt(encrypted_data, salt):
    """Main function to perform parallel decryption."""
    key = get_current_time_key(salt)
    return multi_core_decrypt(encrypted_data, key)

# --------------------------------------------------Execution---------------------------------------------#

input_text = "Hello world my name is rezafta,"
salt = "reza"

enc1 = parallel_process_encrypt(input_text, salt)
dec1 = parallel_process_decrypt(enc1, salt)

print("Encrypted text is:", enc1)
print("Decrypted text is:", dec1)