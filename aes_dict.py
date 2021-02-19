#offline dictionary attack on AES password encryption

from Crypto.Cipher import AES
from binascii import hexlify, unhexlify, b2a_base64, a2b_base64

IV = "" #enter IV

common = ["123456",
        "123456789"
        "qwerty"
        "password"
        "1234567"
        "12345678"
        "12345"
        "iloveyou"
        "111111"
        "123123"
        'abc123'
        "qwerty123"
        "1q2w3e4r"
        "admin"
        "qwertyuiop"
        "654321"
        "555555"
        "lovely"
        "7777777"
        "888888"
        "princess"
        "dragon"
        "password1"
        "123qwe"
        "666666"]

#enter keywords for password permutations
info = ["Keyword1",
        "Keyword2",
        "Keyword3"]

def pad_key(key: str):
    """Pad the key with 0s"""

    # Variables
    length = len(key)
    default_length = 32

    # Check if key exceeds length
    if length > 32:
        raise ValueError("Key value too long")

    # Padding for Cipher
    if length < default_length:
        key += '0' * (default_length - length)

    # Return the padded key
    return key

def create_cipher(key, iv):
    """Create the cipher to decode the text"""
    return AES.new(key.encode(), AES.MODE_CBC, iv.encode())

def encrypt(key: str, iv:str, message: str):
    """Encrypt the text with iv"""
    cipher = create_cipher(key, iv)

    # Cipher text in base64
    return b2a_base64(cipher.encrypt(message.encode())).decode()

def decrypt(key: str, iv:str, cipher_text: str):
    """Decrypt the text with iv"""
    ct = a2b_base64(cipher_text)
    cipher = create_cipher(key, iv)
    return cipher.decrypt(ct).decode()


if __name__ == '__main__':

    try:
        with open('ciphertext') as file:
            cipher = file.read()
    except:
        cipher = input("Enter ciphertext:")

    infoLower = [x.lower() for x in info]
    infoOne = info + infoLower

    infoTwo = []
    for x in infoOne:
        for y in infoOne:
            infoTwo.append(x + y)
            infoTwo.append(x + "-" + y)
            infoTwo.append(x + "_" + y)

    infoThree = []
    for x in infoTwo:
        for y in infoOne:
            infoThree.append(x + y)
            infoThree.append(x + "-" + y)
            infoThree.append(x + "_" + y)

    for password in infoOne + infoTwo + infoThree:
        try:
            key = pad_key(password)
        except:
            continue
        else:
            try:
                flag = decrypt(key, IV, cipher)
            except:
                print(password, "not correct")
            else:
                print(password)
                print(flag)
                break

