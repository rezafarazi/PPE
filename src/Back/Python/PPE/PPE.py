from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64
import time
import re

#Get generate key from unixtime
def get_current_time_key(salt):
    keybase = ""
    key = ""

    # Simulate the TimeStep.GetTimeStep() method
    timestep = int(time.time())
    timestep8 = str(timestep)[:8]
    timestep8char = list(timestep8)

    # Get keybase first 8 numbers
    keybase = timestep8

    for i in range(len(timestep8char)-1, -1, -1):
        keybase += timestep8char[i]

    for i in range(len(timestep8char)):
        keybase += timestep8char[i]

    for i in range(len(timestep8char)-1, -1, -1):
        keybase += timestep8char[i]

    for i in range(len(timestep8char)):
        keybase += timestep8char[i]

    for i in range(len(timestep8char)-1, -1, -1):
        keybase += timestep8char[i]

    for i in range(len(timestep8char)):
        keybase += timestep8char[i]

    for i in range(len(timestep8char)-1, -1, -1):
        keybase += timestep8char[i]

    for i in range(len(timestep8char)):
        keybase += timestep8char[i]

    for i in range(len(timestep8char)-1, -1, -1):
        keybase += timestep8char[i]

    for i in range(len(timestep8char)):
        keybase += timestep8char[i]

    for i in range(len(timestep8char)-1, -1, -1):
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

    key += salt
    key = key[:24]
    result = base64.b64encode(key.encode()).decode()
    return result


def get_key(key_str):
    # Ensure the key is 24 characters long
    key_str = key_str.ljust(24)[:24]
    return key_str

#Encrypt function
def single_core_encrypt(data, key_str):
    key = get_key(key_str)
    cipher = AES.new(key, AES.MODE_ECB)
    ct_bytes = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
    ct = base64.b64encode(ct_bytes).decode('utf-8')
    return ct

#Decrypt function
def single_core_decrypt(enc_data, key_str):
    key = get_key(key_str)
    ct = base64.b64decode(enc_data)
    cipher = AES.new(key, AES.MODE_ECB)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt.decode('utf-8')

#Multi core encryption function
def multi_core_encrypt(data,key_str):
    # Calculate the midpoint of the string
    midpoint = len(data) // 2

    # Divide the string into two halves
    Left_Data = data[:midpoint]
    Right_Data = data[midpoint:]

    Left_Cipher = single_core_encrypt(Left_Data, key_str)
    Right_Cipher = single_core_encrypt(Right_Data, key_str)

    cipher = "%s~|~%s" % (Left_Cipher, Right_Cipher)
    encoded_bytes = base64.b64encode(cipher.encode('ascii'))
    encoded_string = encoded_bytes.decode('ascii')
    return encoded_string

#Multi core decryption function
def multi_core_decrypt(data,key_str):

    Ciphers = base64.b64decode(data)
    Ciphers_str = Ciphers.decode('utf-8')
    main_cipher = Ciphers_str.split('~|~')

    Left_Text = single_core_decrypt(main_cipher[0], key_str)
    Right_Text = single_core_decrypt(main_cipher[1], key_str)

    return Left_Text+Right_Text

#main run
if __name__ == '__main__':
    key=base64.b64decode(get_current_time_key("Asia/Tehran"))
    data = "Hello world my name is rezafta"

    encrypted_data = multi_core_encrypt(data, key)
    print(f"Encrypted: {encrypted_data}")

    decrypted_data = multi_core_decrypt(encrypted_data, key)
    print(f"Decrypted: {decrypted_data}")
