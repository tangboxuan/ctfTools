import requests
from textwrap import wrap
import math

URL = "" #enter url here
s = requests.Session()
chars = list('0123456789:_abcdefghijklmnopqrstuvwxyz{}') #edit chars to guess

#edit based on how the encryption is obtained
def getCred(cred):
    payload = {
        'creds': cred
    }
    response = s.post(URL, data=payload)
    for line in response.text.split("\n")[-10:]:
        if "new-creds" in line:
            newcred = line.strip().split(">")[1].split("<")[0]
            chunks = wrap(newcred, 32)
            return chunks

def getNext(n, known):
    attack = n*'0'+"\n"
    compare = getCred(attack)
    for i in chars:
        block = math.floor(len(attack+known)/16)
        chunk = getCred(attack+known+i)
        if compare[block] == chunk[block]:
            return i
    return ""

def getBlocks(n, known):
    start = n * 16 - 2 - len(known)
    for i in range(start, 0, -1):
        print(i, known)
        add = getNext(i, known)
        if not add:
            return 0
        known += add
    return known

def getMax():
    i = 1
    known = getBlocks(i, "")
    while known:
        i += 1
        known_copy = known
        known = getBlocks(i, known)
    return known

if __name__ == "__main__":
    getMax()