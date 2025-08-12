import network
import time
import ucryptolib
import ubinascii
import _thread

# Decorator to calculate execution time
def calculate_time(func):
    """Decorator to measure and print the execution time of a function."""
    def wrapper(*args, **kwargs):
        start_time = time.ticks_ms()
        result = func(*args, **kwargs)
        end_time = time.ticks_ms()
        execution_time = time.ticks_diff(end_time, start_time)
        print(f"Function '{func.__name__}' executed in {execution_time} milliseconds")
        return result
    return wrapper

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

connect_wifi('Reza', '-------------')

# --------------------------------------------------Key generation functions---------------------------------------------#
import urequests
import json

def get_unix_time():
    """Fetches the current Unix time from an external server."""
    try:
        response = urequests.get("http://ip-api.com/json/?fields=status,message,timezone,offset")
        if response.status_code == 200:
            data = response.json()
            unix_time = data.get('offset', 'N/A')
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
        return b'\0' * 16  # Return 16 null bytes
    
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
    
    # Combine with salt and ensure length is 16 bytes
    final_key = (salt + key).encode('utf-8')
    # Pad or truncate to 16 bytes
    if len(final_key) < 16:
        final_key += b'\0' * (16 - len(final_key))
    else:
        final_key = final_key[:16]
    return final_key

# --------------------------------------------------Encryption/Decryption utilities---------------------------------------------#

def pad(s):
    """Pads a string to be a multiple of 16 bytes."""
    pad_len = 16 - (len(s) % 16)
    return s + (chr(pad_len) * pad_len)

def unpad(s):
    """Removes padding from a decrypted string."""
    return s[:-ord(s[-1])]

def single_core_encrypt(data, key):
    """Encrypts data using AES in ECB mode on a single core."""
    aes = ucryptolib.aes(key, 1)  # Initialize AES (ECB)
    plaintext = pad(data)
    ciphertext = aes.encrypt(plaintext.encode('utf-8'))
    return ubinascii.b2a_base64(ciphertext).decode('utf-8')

def single_core_decrypt(enc_data, key):
    """Decrypts data using AES in ECB mode on a single core."""
    aes = ucryptolib.aes(key, 1)  # Initialize AES (ECB)
    decoded_ciphertext = ubinascii.a2b_base64(enc_data.encode('utf-8'))
    decrypted = aes.decrypt(decoded_ciphertext).decode('utf-8')
    return unpad(decrypted)

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

@calculate_time
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

@calculate_time
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

@calculate_time
def parallel_process_encrypt(input_text, salt):
    """Main function to perform parallel encryption."""
    key = get_current_time_key(salt)
    return multi_core_encrypt(input_text, key)

@calculate_time
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