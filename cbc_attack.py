import requests
from textwrap import wrap
import math
import string

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

URL = "" #enter link here
ciphertext = '' #enter ciphertext here
paddingScheme = 'PKCS7' #choose padding scheme

def getResponse(stringToSend):          #customise how to get response
    payload = {                         #
        'data': stringToSend            #
    }                                   #
    response = s.post(URL, data=payload)#
    return response                     #

def checkSuccess(response):                     #customise success metric
    for line in response.text.split("\n")[-10:]:#
        if "Successful" in line:                #
            return 1                            # 1 for success
    return 0                                    # 0 for failure

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
s = requests.Session()
originalList = wrap(ciphertext, 32)

def getData(data, i, x):
    response = getResponse(data)
    if checkSuccess(response):
        value = hex(i^x)
        print('value:',value)
        return value[2:]
    return 0

def xor(initial, value):
    '''
    takes 2 strings in hexadecimal form and returns a string of the two values xored
    '''
    if not value:
        return initial
    newvalue = hex(int(initial,16) ^ int(value,16))[2:]
    return newvalue

def pad(n):
    '''
    generates padding of according to chose scheme
    '''
    if paddingScheme == 'PKCS7':
        string = n * '0' + str(n+1)
    elif paddingScheme == 'increment':
        for i in range(2,n+2):
            if i < 10:
                string += '0' + str(i)
            else:
                if i < 16:
                    string += '0'
                string += hex(i)[2:]
    #add encryption scheme here where n = number of bytes known
    else:
        print("ADD CUSTOM ENCRYPTION SCHEME UNDER PAD AND GUESS")
        #string undefined to throw error
    return string

def guess(known):
    print('known (hex):', known)
    print('known (asc):', bytearray.fromhex(known).decode())

    length = len(known)
    if length % 2 != 0: #check that number of hex chars is even
        print("known wrong length")
        return 1
    block = math.floor(length/32)
    attackLength = length- block * 32

    padding = pad(int(attackLength/2)) 
    if paddingScheme == 'PKCS7':
        checkByte = int(attackLength/2)
    elif paddingScheme == 'Decrement':
        checkByte = 1
    #add encryption scheme here where checkByte = byte expected for padding oracle

    if attackLength: 
        frontStringReset = ''.join(originalList[:-(1+block)])[:-attackLength] # drops number of known characters and irrelevant blocks
        dropped = originalList[-(2+block)][-attackLength:] # gets dropped known characters
        back = xor(dropped, known[:attackLength]) # xors dropped with known
        padding = xor(back, padding) # xor with intended padding
        if len(padding) % 2 != 0: # appends 0 in front if dropped has odd number of chars
            padding = '0' + padding
    else: #if known is empty
        frontStringReset = ''.join(originalList[:-(1+block)])
    backString = originalList[-(1+block)] # block being attacked

    success = 0
    for i in range(256):
        string = xor(frontStringReset, hex(i)[2:]) + padding + backString
        value = getData(string, i, checkByte)
        if value:
            success += 1
            if len(value) == 1:
                value = '0' + value
            toAdd = value
    if success == 1:
        return toAdd
    if success == 0:
        print("ERROR")
        return 0
    # else success > 1
    print("MORE THAN ONE POSSIBLE VALUE FOUND")
    return 0

def getCipher(known=''):
    toAdd = 1
    while(toAdd):
        toAdd = guess(known)
        known = toAdd + known
    return known

getCipher()
