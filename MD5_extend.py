from textwrap import wrap

S = [7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,
    5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,
    4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,
    6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21]

K = [0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee,
    0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501,
    0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be,
    0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821,
    0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa,
    0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,
    0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed,
    0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a,
    0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c,
    0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70,
    0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05,
    0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665,
    0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039,
    0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1,
    0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1,
    0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391]

a0 = 0x67452301 
b0 = 0xefcdab89
c0 = 0x98badcfe
d0 = 0x10325476

def reverse(string, n):
    arr = wrap(string, n)
    arr.reverse()
    return ''.join(arr)

def result(arr):
    hash = ''
    for x in arr:
        literal = hex(x)[2:]
        literal = '0' * (8-len(literal)) + literal
        hash += (reverse(literal,2))
    return hash

def leftrotate(x, c):
    return ((x >> (32 - c)) | (x << c)) & 0xFFFFFFFF

def paddedMessage(message, oriLen=0, keyLen=0):
        message = ''.join(format(ord(i), '08b') for i in message)
        msglen = (len(message) + oriLen + keyLen) & 0xFFFFFFFFFFFFFFFF
        append = 448 - (msglen +8)%512
        append = append + 512 if append < 0 else append
        appendlen = bin(msglen)[2:]
        appendlen = '0' * (64-len(appendlen)) + appendlen
        message += '10000000' + '0' * append + reverse(appendlen, 8)
        return message

def getState(starthash):
    starthash = wrap(starthash,8)
    for i in range(4):
        starthash[i] = int(reverse(starthash[i], 2),16)
    return starthash

def MD5_extend(message, starthash='', known='',keyLen=0):

    messageBin = ''.join(format(ord(i), '08b') for i in message)
    if not starthash or not known:
        global a0, b0, c0, d0
    else:
        print("Calculating extension")
        a0, b0, c0, d0 = getState(starthash)
        known = paddedMessage(known,0,keyLen*8)
    
    message = paddedMessage(message,len(known)+keyLen*8,0)
    for chunk in wrap(message, 512):
        M = wrap(chunk, 32)
        A = a0
        B = b0
        C = c0
        D = d0
        for i in range(64):
            if 0 <= i <= 15:
                F = (B & C) | ((~B) & D)
                g = i
            elif 16 <= i <= 31:
                F = (D & B) | ((~D) & C)
                g = (5*i + 1) % 16
            elif 32 <= i <= 47:
                F = B ^ C ^ D
                g = (3*i + 5) % 16
            elif 48 <= i <= 63:
                F = C ^ (B | (~D))
                g = (7*i) % 16
            F = (F + A + K[i] + int(reverse(M[g], 8),2)) & 0xFFFFFFFF
            A = D
            D = C
            C = B
            B = B + leftrotate(F, S[i])
        a0 = (a0 + A) & 0xFFFFFFFF
        b0 = (b0 + B) & 0xFFFFFFFF
        c0 = (c0 + C) & 0xFFFFFFFF
        d0 = (d0 + D) & 0xFFFFFFFF

    return [result([a0,b0,c0,d0]), hex(int(known+messageBin,2))]

print(MD5_extend("TTEST"))
print(MD5_extend("TEST","057fde0ca4fe5ae19d15be06bdfa63c6","TEST",1))
