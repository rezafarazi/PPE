from Crypto.Cipher import ChaCha20
from Crypto.Random import get_random_bytes
import base64
import time
import re
import multiprocessing as mp
import requests


# Get online unix time
def get_unix_time():
    # Fetch the JSON response from the API
    response = requests.get("https://worldtimeapi.org/api/timezone/asia/tehran")
    # response = requests.get("http://ip-api.com/json/?fields=status,message,timezone,offset")

    if response.status_code == 200:
        data = response.json()
        # Extract the Unix time
        unix_time = data.get('unixtime', 'N/A')

    response.close()
    return unix_time


# Get generate key from unixtime
def get_current_time_key(salt):
    keybase = ""
    key = ""

    # Simulate the TimeStep.GetTimeStep() method
    try:
        timestep = int(get_unix_time())
    except print(0):
        timestep = int(time.time())
        pass

    timestep8 = str(timestep)[:8]
    # print(timestep8);
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
        # Ensure the number is within valid ASCII range (32-126)
        key_char = chr((add_num % 95) + 32)
        key += key_char

    key = salt + key
    key = key[:32]  # ChaCha20 requires 32-byte key
    result = base64.b64encode(key.encode()).decode()
    return result


def get_key(key_str):
    # Ensure the key is 32 characters long for ChaCha20
    key_str = key_str.ljust(32)[:32]
    return key_str


# Encrypt function
def single_core_encrypt(data, key_str):
    key = key_str[0:32]  # ChaCha20 uses 32-byte keys
    
    # Generate a random 12-byte nonce for ChaCha20
    nonce = get_random_bytes(12)
    cipher = ChaCha20.new(key=key.encode('utf-8'), nonce=nonce)
    ct_bytes = cipher.encrypt(data.encode('utf-8'))
    
    # Combine nonce and ciphertext, then encode
    combined = nonce + ct_bytes
    ct = base64.b64encode(combined).decode('utf-8')
    return ct


# Decrypt function
def single_core_decrypt(enc_data, key_str):
    key = key_str[0:32]  # ChaCha20 uses 32-byte keys
    
    # Decode the base64 data
    combined = base64.b64decode(enc_data)
    
    # Extract nonce (first 12 bytes) and ciphertext (remaining bytes)
    nonce = combined[:12]
    ct_bytes = combined[12:]
    
    cipher = ChaCha20.new(key=key.encode('utf-8'), nonce=nonce)
    pt = cipher.decrypt(ct_bytes)
    return pt.decode('utf-8')


# Multi core encryption function
def multi_core_encrypt(data, key_str):
    # Calculate the midpoint of the string
    midpoint = len(data) // 2

    # Divide the string into two halves
    Left_Data = data[:midpoint]
    Right_Data = data[midpoint:]

    with mp.Pool(1) as pool:
        Left_Cipher = single_core_encrypt(Left_Data, key_str)

    with mp.Pool(1) as pool:
        Right_Cipher = single_core_encrypt(Right_Data, key_str)

    cipher = "%s~|~%s" % (Left_Cipher, Right_Cipher)
    encoded_bytes = base64.b64encode(cipher.encode('utf-8'))
    encoded_string = encoded_bytes.decode('utf-8')
    return encoded_string


# Multi core decryption function
def multi_core_decrypt(data, key_str):
    Ciphers = base64.b64decode(data)
    Ciphers_str = Ciphers.decode('utf-8')
    main_cipher = Ciphers_str.split('~|~')

    # Get parallel processing start
    with mp.Pool(1) as pool:
        Left_Text = single_core_decrypt(main_cipher[0], key_str)

    with mp.Pool(1) as pool:
        Right_Text = single_core_decrypt(main_cipher[1], key_str)
    # Get parallel processing end

    return Left_Text + Right_Text


# Main functions for call PPE

def PPE(inp, salt):
    key_bytes = base64.b64encode(get_current_time_key(salt).encode('utf-8'))
    key = key_bytes.decode('utf-8')
    return multi_core_encrypt(inp, key)


def PPD(inp, salt):
    key_bytes = base64.b64encode(get_current_time_key(salt).encode('utf-8'))
    key = key_bytes.decode('utf-8')
    return multi_core_decrypt(inp, key)


# main run
if __name__ == '__main__':

    data = "salam"

    encrypted_data = PPE(data, "reza")
    print(f"Encrypted: {encrypted_data}")
    
    decrypted_data = PPD(encrypted_data, "reza")
    print(f"Decrypted: {decrypted_data}")