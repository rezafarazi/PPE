import network
import time
import ucryptolib
import ubinascii
import _thread

# Get global variables
results = {'Left_Cipher': None, 'Right_Cipher': None, 'Left_Text': None, 'Right_Text': None}
lock = _thread.allocate_lock()

# --------------------------------------------------WIFI and board functions start---------------------------------------------#

def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)  # Create WLAN object
    wlan.active(True)  # Enable station mode
    wlan.connect(ssid, password)  # Connect to network

    # Wait for connection
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

# Call the function with network SSID and password
connect_wifi('Reza', '-------')

# --------------------------------------------------WIFI and board functions end---------------------------------------------#

# --------------------------------------------------Key generate functions start---------------------------------------------#
import urequests
import json

def get_unix_time():
    try:
        # Fetch the JSON response from the API
        response = urequests.get("http://ip-api.com/json/?fields=status,message,timezone,offset")
        
        # Debugging: Print the raw response
        #print("Raw Response:", response.text)
        
        # Check if the request was successful
        if response.status_code == 200:
            try:
                # Parse the JSON response
                data = response.json()
                #print("Parsed JSON:", data)
                
                # Extract the Unix time
                unix_time = data.get('offset', 'N/A')
            except ValueError:
                #print("Error: Invalid JSON response")
                unix_time = 'N/A'
        else:
            #print(f"Error: API request failed with status code {response.status_code}")
            unix_time = 'N/A'
        
        # Close the response
        response.close()
        
        return unix_time
    
    except Exception as e:
        #print(f"An error occurred: {e}")
        return 'N/A'

# Get generate key from unixtime
def get_current_time_key(salt):
    keybase = ""
    key = ""

    # Simulate the TimeStep.GetTimeStep() method
    unix__time=get_unix_time()
    #print(unix__time)
    timestep = int(unix__time)
    timestep8 = str(timestep)[:8]
    timestep8char = list(timestep8)

    # Get keybase first 8 numbers
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

def remove_x10_from_string(input_str):
    # Convert string to bytes
    byte_data = input_str.encode('utf-8')

    print(byte_data)

    # Remove all occurrences of \x
    cleaned_byte_data = byte_data.replace(b'\x01', b'')
    cleaned_byte_data = cleaned_byte_data.replace(b'\x02', b'')
    cleaned_byte_data = cleaned_byte_data.replace(b'\x03', b'')
    cleaned_byte_data = cleaned_byte_data.replace(b'\x04', b'')
    cleaned_byte_data = cleaned_byte_data.replace(b'\x05', b'')
    cleaned_byte_data = cleaned_byte_data.replace(b'\x06', b'')
    cleaned_byte_data = cleaned_byte_data.replace(b'\x07', b'')
    cleaned_byte_data = cleaned_byte_data.replace(b'\x08', b'')
    cleaned_byte_data = cleaned_byte_data.replace(b'\x09', b'')
    cleaned_byte_data = cleaned_byte_data.replace(b'\x10', b'')
    cleaned_byte_data = cleaned_byte_data.replace(b'\x0a', b'')
    cleaned_byte_data = cleaned_byte_data.replace(b'\x0b', b'')
    cleaned_byte_data = cleaned_byte_data.replace(b'\x0c', b'')
    cleaned_byte_data = cleaned_byte_data.replace(b'\x0d', b'')
    cleaned_byte_data = cleaned_byte_data.replace(b'\x0e', b'')
    cleaned_byte_data = cleaned_byte_data.replace(b'\x0f', b'')

    # Convert bytes back to string
    cleaned_str = cleaned_byte_data.decode('utf-8')

    return cleaned_str

# --------------------------------------------------Other functions end---------------------------------------------#

# --------------------------------------------------Single Process encryption/decryption functions start---------------------------------------------#

def pad(s):
    pad_len = 16 - len(s) % 16
    return s + (chr(pad_len) * pad_len)

def unpad(s):
    return s[:-ord(s[-1])]

def single_core_encrypt(data, key_str):
    byte_data = key_str[0:16]
    key = byte_data.decode('latin-1')

    # initilize AES (ECB)
    aes = ucryptolib.aes(key, 1)

    # get encrypt
    plaintext = pad(data)
    ciphertext = aes.encrypt(plaintext.encode('utf-8'))
    encoded_ciphertext = ubinascii.b2a_base64(ciphertext).decode('utf-8')
    return encoded_ciphertext

def single_core_decrypt(enc_data, key_str):
    byte_data = key_str[0:16]
    key = byte_data.decode('latin-1')

    # initilize AES (ECB)
    aes = ucryptolib.aes(key, 1)

    decoded_ciphertext = ubinascii.a2b_base64(enc_data.encode('utf-8'))
    aes = ucryptolib.aes(key, 1)
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

# Multi core encryption function
def multi_core_encrypt(data, key_str):
    global result

    # Calculate the midpoint of the string
    midpoint = len(data) // 2

    # Divide the string into two halves
    Left_Data = data[:midpoint]
    Right_Data = data[midpoint:]

    # Parallel on thread start
    _thread.start_new_thread(encrypt_left, (Left_Data, key_str))
    _thread.start_new_thread(encrypt_right, (Right_Data, key_str))

    # Wait for threads to finish
    while True:
        with lock:
            if results['Left_Cipher'] and results['Right_Cipher']:
                break
        time.sleep(1)
    # Parallel on thread end

    cipher = "%s~|~%s" % (results['Left_Cipher'], results['Right_Cipher'])
    cipher = cipher.replace("\n", "");
    cipher = cipher.replace("\r", "");
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

# Multi core decryption function
def multi_core_decrypt(data, key_str):
    Ciphers = ubinascii.a2b_base64(data).decode('utf-8')

    # Ciphers_str = Ciphers.decode('utf-8')
    main_cipher = Ciphers.split('~|~')

    # Get parallel processing satrt
    _thread.start_new_thread(decrypt_left, (main_cipher[0], key_str))
    _thread.start_new_thread(decrypt_right, (main_cipher[1], key_str))

    # Wait for threads to finish
    while True:
        with lock:
            if results['Left_Text'] and results['Right_Text']:
                break
        time.sleep(1)
    # Get parallel processing end

    # Get trim left and right string start
    left = remove_x10_from_string(results['Left_Text'])
    right = remove_x10_from_string(results['Right_Text'])
    # Get trim left and right string end

    return left + right

# --------------------------------------------------Multi Process encryption/decryption functions end---------------------------------------------#

# --------------------------------------------------Main PPE functions start---------------------------------------------#

def PPE(inp, salt):
    key = ubinascii.b2a_base64(get_current_time_key(salt))
    return multi_core_encrypt(inp, key)

def PPD(inp, salt):
    key = ubinascii.b2a_base64(get_current_time_key(salt))
    return multi_core_decrypt(inp, key)

# --------------------------------------------------Main PPE functions end---------------------------------------------#

enc1 = PPE("Helli world my names is rezafta", "reza")
dec1 = PPD(enc1, "reza")

print("Text encript is : ", enc1)
print("Text decript is : ", dec1)