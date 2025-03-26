import network
import time
import ucryptolib
import ubinascii
import _thread

# Decorator to calculate execution time
def calculate_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.ticks_ms()
        result = func(*args, **kwargs)
        end_time = time.ticks_ms()
        execution_time = time.ticks_diff(end_time, start_time)
        print(f"Function '{func.__name__}' executed in {execution_time} milliseconds")
        return result
    return wrapper

# Get global variables
results = {'Left_Cipher': None, 'Right_Cipher': None, 'Left_Text': None, 'Right_Text': None}
lock = _thread.allocate_lock()

# --------------------------------------------------WIFI and board functions start---------------------------------------------#

# @calculate_time
def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)  # Create WLAN object
    wlan.active(True)  # Activate station mode
    wlan.connect(ssid, password)  # Connect to network
    
    max_attempts = 10
    attempt = 0
    while not wlan.isconnected() and attempt < max_attempts:
        print('Connecting to network...')
        time.sleep(1)
        attempt += 1
    
    if wlan.isconnected():
        print('Connected successfully!')
        print('Network config:', wlan.ifconfig())
    else:
        print('Failed to connect')

connect_wifi('Reza', '@Key123456')

# --------------------------------------------------WIFI and board functions end---------------------------------------------#

# --------------------------------------------------Key generate functions start---------------------------------------------#
import urequests
import json

# @calculate_time
def get_unix_time():
    try:
        response = urequests.get("http://future.izino.ir/index.php")
        if response.status_code == 200:
            data = response.json()
            unix_time = data.get('unixtime', 'N/A')
        else:
            unix_time = 'N/A'
        response.close()
        return unix_time
    except Exception as e:
        return 'N/A'

# @calculate_time
def get_current_time_key(salt):
    keybase = ""
    key = ""
    unix__time = get_unix_time()
    timestep = int(unix__time)
    timestep8 = str(timestep)[:8]
    timestep8char = list(timestep8)
    
    keybase = timestep8
    for i in range(len(timestep8char) - 1, -1, -1):
        keybase += timestep8char[i]
    for i in range(len(timestep8char)):
        keybase += timestep8char[i]
    for i in range(len(timestep8char) - 1, -1, -1):
        keybase += timestep8char[i]
    for i in range(len(timestep8char)):
        keybase += timestep8char[i]
    for i in range(len(timestep8char) - 1, -1, -1):
        keybase += timestep8char[i]
    for i in range(len(timestep8char)):
        keybase += timestep8char[i]
    for i in range(len(timestep8char) - 1, -1, -1):
        keybase += timestep8char[i]
    for i in range(len(timestep8char)):
        keybase += timestep8char[i]
    for i in range(len(timestep8char) - 1, -1, -1):
        keybase += timestep8char[i]
    for i in range(len(timestep8char)):
        keybase += timestep8char[i]
    for i in range(len(timestep8char) - 1, -1, -1):
        keybase += timestep8char[i]
    for i in range(len(timestep8char)):
        keybase += timestep8char[i]
    
    keybasechar = list(keybase)
    for i in range(0, len(keybasechar) // 2, 2):
        num_a = keybasechar[i]
        num_b = keybasechar[i + 1]
        add_num = int(num_a + num_b)
        key_char = chr(add_num)
        key += key_char
    
    key = salt + key
    key = key[:16]
    result = ubinascii.b2a_base64(key.encode()).decode()
    return result

def get_key(key_str):
    # Ensure the key is 16 characters long
    key_str = key_str.ljust(16)[:16]
    return key_str

def get_key2(key_str):
    # Ensure the key is 16 characters long
    key = key_str[0:16]
    return key

# --------------------------------------------------Key generate functions end---------------------------------------------#

# --------------------------------------------------Other functions start---------------------------------------------#

# @calculate_time
def remove_x10_from_string(input_str):
    # Convert string to bytes
    byte_data = input_str.encode('utf-8')
    # print(byte_data)
    
    # Remove all occurrences of control characters
    cleaned_byte_data = byte_data.replace(b'\x01', b'').replace(b'\x02', b'').replace(b'\x03', b'').replace(b'\x04', b'').replace(b'\x05', b'').replace(b'\x06', b'').replace(b'\x07', b'').replace(b'\x08', b'').replace(b'\x09', b'').replace(b'\x10', b'').replace(b'\x0a', b'').replace(b'\x0b', b'').replace(b'\x0c', b'').replace(b'\x0d', b'').replace(b'\x0e', b'').replace(b'\x0f', b'')
    
    # Convert bytes back to string
    cleaned_str = cleaned_byte_data.decode('utf-8')
    return cleaned_str

# --------------------------------------------------Other functions end---------------------------------------------#

# --------------------------------------------------Single Process encryption/decryption functions start---------------------------------------------#

def pad(s):
    # Add padding to make string length multiple of 16
    pad_len = 16 - len(s) % 16
    return s + (chr(pad_len) * pad_len)

def unpad(s):
    # Remove padding from string
    return s[:-ord(s[-1])]

# @calculate_time
def single_core_encrypt(data, key_str):
    byte_data = key_str[0:16]
    key = byte_data.decode('latin-1')
    aes = ucryptolib.aes(key, 1)  # Initialize AES (ECB)
    plaintext = pad(data)
    ciphertext = aes.encrypt(plaintext.encode('utf-8'))
    encoded_ciphertext = ubinascii.b2a_base64(ciphertext).decode('utf-8')
    return encoded_ciphertext

# @calculate_time
def single_core_decrypt(enc_data, key_str):
    byte_data = key_str[0:16]
    key = byte_data.decode('latin-1')
    aes = ucryptolib.aes(key, 1)  # Initialize AES (ECB)
    decoded_ciphertext = ubinascii.a2b_base64(enc_data.encode('utf-8'))
    decrypted = aes.decrypt(decoded_ciphertext).decode('utf-8')
    return decrypted.strip()

# --------------------------------------------------Single Process encryption/decryption functions end---------------------------------------------#

# --------------------------------------------------Multi Process encryption/decryption functions start---------------------------------------------#

def encrypt_left(data, key):
    global result
    result = single_core_encrypt(data, key)
    with lock:
        results['Left_Cipher'] = result

def encrypt_right(data, key):
    global result
    result = single_core_encrypt(data, key)
    with lock:
        results['Right_Cipher'] = result

# @calculate_time
def multi_core_encrypt(data, key_str):
    global result
    # Calculate the midpoint of the string
    midpoint = len(data) // 2
    Left_Data = data[:midpoint]
    Right_Data = data[midpoint:]
    
    # Start parallel threads
    _thread.start_new_thread(encrypt_left, (Left_Data, key_str))
    _thread.start_new_thread(encrypt_right, (Right_Data, key_str))
    
    # Wait for threads to finish
    while True:
        with lock:
            if results['Left_Cipher'] and results['Right_Cipher']:
                break
        time.sleep(1)
    
    cipher = "%s~|~%s" % (results['Left_Cipher'], results['Right_Cipher'])
    cipher = cipher.replace("\n", "").replace("\r", "")
    encoded_bytes = ubinascii.b2a_base64(cipher.encode('utf-8'))
    encoded_string = encoded_bytes.decode('utf-8')
    return encoded_string

def decrypt_left(data, key):
    result = single_core_decrypt(data, key)
    with lock:
        results['Left_Text'] = result

def decrypt_right(data, key):
    result = single_core_decrypt(data, key)
    with lock:
        results['Right_Text'] = result

# @calculate_time
def multi_core_decrypt(data, key_str):
    Ciphers = ubinascii.a2b_base64(data).decode('utf-8')
    main_cipher = Ciphers.split('~|~')
    
    # Start parallel processing
    _thread.start_new_thread(decrypt_left, (main_cipher[0], key_str))
    _thread.start_new_thread(decrypt_right, (main_cipher[1], key_str))
    
    # Wait for threads to finish
    while True:
        with lock:
            if results['Left_Text'] and results['Right_Text']:
                break
        time.sleep(1)
    
    # Trim left and right strings
    left = remove_x10_from_string(results['Left_Text'])
    right = remove_x10_from_string(results['Right_Text'])
    return left + right

# --------------------------------------------------Multi Process encryption/decryption functions end---------------------------------------------#

# --------------------------------------------------Main PPE functions start---------------------------------------------#

@calculate_time
def PPE(inp, salt):
    key = ubinascii.b2a_base64(get_current_time_key(salt))
    return multi_core_encrypt(inp, key)

@calculate_time
def PPD(inp, salt):
    key = ubinascii.b2a_base64(get_current_time_key(salt))
    return multi_core_decrypt(inp, key)

# --------------------------------------------------Main PPE functions end---------------------------------------------#

enc1 = PPE("Helli world my names is rezafta", "reza")
dec1 = PPD(enc1, "reza")

print("Text encript is : ", enc1)
print("Text decript is : ", dec1)