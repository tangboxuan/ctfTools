from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#Public modulus
p = 0
if not p:
    p = input("Enter public modulus (p):")

#Public base
g = 0
if not g:
    g = input("Enter public base (g):")

#Alice' public key
#A = (g ^ a) mod p
A = 0
if not A:
    A = input("Enter Alice's public key (A = (g ^ a) mod p):")

#Bob's public key
#B = (g ^ b) mod p
B = 0
if not B:
    B = input("Enter Bob's public key (B = (g ^ b) mod p):")

def dla(base, power1, power2, mod):
    driver = webdriver.Firefox()
    driver.get("https://www.alpertron.com.ar/DILOG.HTM")
    driver.find_element_by_id("base").send_keys(str(base))
    controlPow = driver.find_element_by_id("pow")
    driver.find_element_by_id("mod").send_keys(str(mod))
    driver.find_element_by_id("digits").send_keys("100")
    controlSubmit = driver.find_element_by_id("dlog")
    controlPow.send_keys(str(power1))
    controlSubmit.click()
    a = driver.find_element_by_id("result").text.splitlines()[1].split()[2]
    controlPow.clear()
    controlPow.send_keys(str(power2))
    controlSubmit.click()
    b = driver.find_element_by_id("result").text.splitlines()[1].split()[2]
    driver.close()
    return (int(a), int(b))


a, b = dla(g, A, B, p)

secret = pow(g, a*b, p)
if secret == pow(A, b, p) and secret == pow(B, a, p):
    print("Secret key:", secret)
else:
    print("Error with values")