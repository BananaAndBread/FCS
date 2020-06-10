import argparse
import base64
import math
import sys

from fractions import gcd


c1 = "BzFd4riBUZdFuPCkB3LOh+5iyMImeQ/saFLVD+ca2L8VKSz0+wtTaL55RRpHBAQdl24Fb3XyVg2N9UDcx3slT+vZs7tr03W7oJZxVp3M0ihoCwer3xZNieem8WZQvQvyNP5s5gMT+K6pjB9hDFWWmHzsn7eOYxRJZTIDgxA4k2w="
c2 = "jmVRiKyVPy1CHiYLl8fvpsDAhz8rDa/Ug87ZUXZ//rMBKfcJ5MqZnQbyTJZwSNASnQfgel3J/xJsjlnf8LoChzhgT28qSppjMfWtQvR6mar1GA0Ya1VRHkhggX1RUFA4uzL56X5voi0wZEpJITUXubbujDXHjlAfdLC7BvL/5+w="
c1 = base64.b64decode(c1)
c2 = base64.b64decode(c2)


def os2ip(X):
    xLen = len(X)
    X = X[::-1]
    x = 0
    for i in range(xLen):
        x += X[i] * 256 ^ i
    return x

c1 = int.from_bytes(c1, byteorder="big")
c2 = int.from_bytes(c2, byteorder="big")
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise ValueError('Modular inverse does not exist.')
    else:
        return x % m

def attack(c1, c2, e1, e2, N):
    if gcd(e1, e2) != 1:
        raise ValueError("Exponents e1 and e2 must be coprime")
    s1 = modinv(e1,e2)
    s2 = int((math.gcd(e1,e2) - e1 * s1) / e2)

    temp = modinv(c2, N)
    m1 = pow(c1,s1,N)
    print("1" ,temp, -s2, N)
    m2 = pow(temp,-s2,N)
    return (m1 * m2) % N

# def main():
#
#     print '[+] Started attack...'
#     try:
#         message = attack(args.ct1, args.ct2, args.e1, args.e2, args.modulus)
#         print '[+] Attack finished!'
#         print '\nPlaintext message:\n%s' % format(message, 'x').decode('hex')
#     except Exception as e:
#         print '[+] Attack failed!'
#         print e.message

# main()

N = int("AD6DD400CDD68EEC61D7C54B1567E16671D7401EBBA0ABE6B391575F8271EEEAD78ADE10D0964D0174DCFD2E5413DC1A075E0E7F83D143BF76C1C1ABA5A501103E518C5171149D0009EBD29255A2F11DBE5699BD2FA97FEAC9229CF07B1EAADE706D79253AB9D97872771E6DE651E22996958F7F5F42EA0A0DDDB506AEB9E2C3", 16)
e1 = 65537
e2 = 343223
print(c1)
print(c2)
print(N)

answer = (attack(c1, c2, e1, e2, N))
print((answer).to_bytes(math.ceil(math.log(256, answer))+10000, byteorder='big'))