p = 845529816183328832288826827978944092433
g = 419182772165909068703324756801961881648

ga = 803331951724823196054726562340183173391
gb = 382083902245594277300548430928765321436


#https://www.alpertron.com.ar/DILOG.HTM
#enter base = g
#enter modulus = p
#enter power = ga
a = 0 #replace with exponent
#enter base = g
#enter modulus = p
#enter power = gb
b = 0 #replace with exponent

print(pow(ga, b, p))
print(pow(gb, a, p))
print(pow(g, a*b, p))