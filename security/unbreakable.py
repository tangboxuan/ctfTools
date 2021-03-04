#https://www.youtube.com/watch?v=6ZYnA6tguec&t=184s

from Crypto.Random.random import randint
from textwrap import wrap

""""""""""""""""""""""""""""""""""""""""""""""""""""""""
cipherlen = 100     #edit according to security requirement
caesar = False      #implements a caesar shift using key
keyForNext = False  #uses cipher[index + key[i]] instead of cipher[index + 1]
""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def encrypt(plain='',key='',cipherlen=cipherlen,caesar=caesar):
    if not plain:
        plain = input("Enter message here: ").upper()
    else:
        plain = plain.upper()
    if not key:
        key = input("Enter key here: ").upper()
    else:
        key = key.upper()
    keylen = len(key)
    cipher = [[]] * len(plain)
    shift = keylen
    for i in range(len(plain)):
        cipher[i] = ['.'] * cipherlen
        for j in range(cipherlen):
            cipher[i][j] = chr(randint(64,90))
        ordKey = ord(key[i%keylen])
        index = (shift + ordKey - 64) % cipherlen
        plainchar = ord(plain[i]) if plain[i] != ' ' else 64
        newint = ((plainchar - 64 + (ordKey - 65 if caesar else 0)) % 27) + 64
        cipher[i][index] = chr(newint)
        #modified to take the next ordKey - 65 instead of next 1
        nextint = cipher[i][(index + (ordKey - 65 if keyForNext else 1)) % cipherlen]
        shift = ord(nextint) - newint
        cipher[i] = ''.join(cipher[i])
    ciphertext = ''.join(cipher)
    return ciphertext

def decrypt(ciphertext='', key='',cipherlen=cipherlen,caesar=caesar):
    if not ciphertext:
        ciphertext = input("Enter ciphertext: ").upper()
    else:
        ciphertext = ciphertext.upper()
    if not key:
        key = input("Enter key here: ").upper()
    else:
        key = key.upper()
    keylen = len(key)
    cipher = wrap(ciphertext, cipherlen)
    plainlen = len(cipher)
    plain = ['.'] * plainlen
    shift = keylen
    for i in range(plainlen):
        curKey = ord(key[i % keylen])
        index = (shift + curKey - 64) % cipherlen
        newplain = chr(((ord(cipher[i][index]) - 64) - (curKey - 65 if caesar else 0))%27 + 64)
        plain[i] = newplain if newplain != '@' else ' '
        #modified to take the next curKey - 65 instead of next 1
        shift = ord(cipher[i][(index + (curKey -65 if keyForNext else 1))%cipherlen]) - ord(cipher[i][index])
    plain = ''.join(plain)
    return plain

def test():
    for i in range(1,100):
        plain = 'TEST TEST'
        key = 'GUYBNHMUBYGJVHBK'
        value = decrypt(encrypt(plain,key,i),key,i)
        if plain != value:
            print("ERROR")
            break
    print("SUCCESS")

test()