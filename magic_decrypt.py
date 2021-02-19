# decrypt function from https://github.com/AlexFSmirnov/xor-decrypt

def decrypt(bytearr, key):
    output = bytearray()
    for i in range(len(bytearr)):
        output.append(bytearr[i] ^ key[i % len(key)])
    return output

inFile = input("Enter input filename: ")
fileType = inFile.split(".")[-1]
if fileType == "png":
    magic = "89 50 4E 47 0D 0A 1A 0A".split()
else:
    print("https://asecuritysite.com/forensics/magic")
    magic = input("Enter magic in hex, split by space: ").split()
check = [int(i, 16) for i in magic]

with open(inFile, 'rb') as f:
    for i in range(len(check)):
        byte = f.read(1)
        b = int.from_bytes(byte, 'big')
        for a in range(256):
            xor = a ^ b
            if xor == check[i]:
                print(magic[i], chr(a))
                break

key = input("Enter key chosen:").encode("utf-8")
outFile = input("Enter output filename: ")
source = open(inFile ,'rb').read()

with open(outFile, 'wb') as fout: 
    fout.write(decrypt(source, key))