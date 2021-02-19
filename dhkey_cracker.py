#Public modulus
p = 845529816183328832288826827978944092433

#Public base
g = 419182772165909068703324756801961881648

#Alice' public key
#A = (g ^ a) mod p
A = 803331951724823196054726562340183173391

#Bob's public key
#B = (g ^ b) mod p
B = 382083902245594277300548430928765321436


#https://www.alpertron.com.ar/DILOG.HTM
#enter base = g
#enter modulus = p
#enter power = ga
a = 0 #replace with exponent
#enter base = g
#enter modulus = p
#enter power = gb
b = 0 #replace with exponent

secret = pow(g, a*b, p)
if secret == pow(A, b, p) and secret == pow(B, a, p):
    print("Secret key:", secret)
else:
    print("Error with values")