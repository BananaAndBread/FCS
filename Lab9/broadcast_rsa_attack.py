import base64
import math

import gmpy2
gmpy2.get_context().precision = 4096

from binascii import unhexlify
from functools import reduce
from gmpy2 import root

# Håstad's Broadcast Attack
# https://id0-rsa.pub/problem/11/

# Resources
# https://en.wikipedia.org/wiki/Coppersmith%27s_Attack
# https://github.com/sigh/Python-Math/blob/master/ntheory.py

EXPONENT = 3

CIPHERTEXT_1 = "ciphertext.1"
CIPHERTEXT_2 = "ciphertext.2"
CIPHERTEXT_3 = "ciphertext.3"

MODULUS_1 = "modulus.1"
MODULUS_2 = "modulus.2"
MODULUS_3 = "modulus.3"


def chinese_remainder_theorem(items):
    # Determine N, the product of all n_i
    N = 1
    for a, n in items:
        N *= n

    # Find the solution (mod N)
    result = 0
    for a, n in items:
        m = N // n
        r, s, d = extended_gcd(n, m)
        print(n)
        print(m)
        if d != 1:
            print("Input not pairwise co-prime")
        result += a * s * m

    # Make sure we return the canonical solution.
    return result % N


def extended_gcd(a, b):
    x, y = 0, 1
    lastx, lasty = 1, 0

    while b:
        a, (q, b) = b, divmod(a, b)
        x, lastx = lastx - q * x, x
        y, lasty = lasty - q * y, y

    return (lastx, lasty, a)


def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1:
        return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += b0
    return x1


def get_value(filename):
    with open(filename) as f:
        value = f.readline()
    return int(value, 16)

if __name__ == '__main__':
    modulus1 = "BED09481E6C5438DEA330688659FB0DDA3B934924B86D522F131D41A4FDD49CA066346BA716D2B2AE6B0AA655EA1C72FC78672532E21B4EA5E268AA321B8A31C5FFAB1A0F7E83BC37892999729D9BA322465237FCB00AC683B16CA9AA40C84496857C6018D8FC7C58F397D0656E8B6C85553F9A14F61965FECE0B85EEEE99B8128BF8B4CFFE25BE78A4B269944320138D45F4A16C84192AB5895FC64A4F2796A87234B48C46F2DF8719F28EFDAD022118652E3D25E44DA3E51FC13344E1C3ABD75E40C624949B29375BAB36E1FF9A692DF39EADCA179F26B4417CD5D71201F7DEEF7BD0533394157EB9CD292602C481448C3C20A36E189D7733B12AC39888F3B".lower()
    modulus2 = "BA05F0CCE54B987C3EDADD20FE386AFC91BBA05F6BC9592D5EE3D4FD430D7DC31503F5857A6C75695B46AA93FF792C55C3F7FC814A59B50F01037C7A66BD9A8AB2813B459FC7604F0CBF3E7B4AECA875B6C080685759F84E0956A276A9F789DF9A6CF5D32ED0ED28D05730D068089FBFA2CE6C4DAC9A2B82090A1B84019A3F699E0D26B8E0CD19B90980970D3231BF9BE17C12E970B05F4252D98B78470E75C61B4157489D41CDDA72B2E0EC9F7E310ADFB8BFF29DE344654CBFEE7243280B1F821FE5C90239A850AA4BE43D50C4202352CC97B211D7CB728A142CF2DF7AD73999119D478DFB676A943C5B7CAE30BA0E1A274E23D4CC635504B4B454C717F621".lower()
    modulus3 = "ABC757E220D1F0DA46D017D0542273FAAEACA99D68EA3B400F99752B5DEBDB67AE3107D8F491F917BA079E14708F702FC8FC1A6189FC1F41EBA334482695642AFC8083D53DDA77B0B58C251926ED779446A137BBC4EFE3572B0D61DFC1A524C2C7891A6DE6BDA5B15B1604284CCA98B97F6E60974CB17F0A5B1A17BEF2007E02FA8A8BF0E0269DE44DAC25C7C7826CBAC2019435373E887658E5FAF733E08AE04A052FA51447FFFB3B9EEDF7FEEC0C8E62AB0E51C516DB537EE93D9F780B20E1665D8E9E541D5E8DE9AA2EA1447B56D07770A2E5B72CAA0891988D97B77F38274830814BD48E338800B0837FEF4135BAD88F5178941406CFDB831FE18171A13F".lower()
    N1 = int(modulus1, 16)
    N2 = int(modulus2, 16)
    N3 = int(modulus3, 16)
    c1 = "vjXJvWis95tc25G+wxC5agClCJFB9vUslFyV+I4bSiwS4Sm6k8eF61EizKo4hZFwROlO3Ci3YQaTrAm+Y9/qEbM7asvwKTePKX+cLVN61l0xxfTL8CdoXkRE2rSczp1AzzmFz83OHgszX/Wf7kgWU4M73+efPvU9FmcWOauakrdJZx8B0ErJ5cYWNS0ZCam0Nlz+pISqdSJ6MSz0Ek62Ulb3ei8I41FOdHtd8mhC7dfpdfmVLOSEW4yEnn5iuMW0ydvW055dodLc9RKcvJafH9e3zf8/S1/RORXZoUHWnBXBEFOl8iVXz70GcDTPzIhxh6imi0ynLbV68qW2vw2XRQ=="
    c2 = "Mi4MnobVabt1+Q7R/0aIYBBpeRxPRuR6gkhr/Wbw/D23ywu2KbUYBab2XbEguRz8yzBlxScbFjjb98DuILxURoFN8lNKVJLS3d/IrGGr0hjocbz27uBS97hseX0S4nd+BL6LUn0o7qe/yCqk7Y0tEhhcuSMrGn/l9N/6UjgN38TyoyvVbd1UH6BHGLdj9g5JRBKAvcGumymfiE0qS7IOnM3mN5W8gRJaEGDkhDim21Pm1Yg2GRBJ+z7C8AEy+Dz6OFvWuDsY24Gb+643D7KrmFObJ1n8Qyme/Y1bfvBkG+xdvGoBzyQrlDT12Qjkfoqb37HNrGUUD5cj2q54gyp80w=="
    c3 = "hMQVVspFGh7NxCqLf7DVto3OxgDLn9n9gOCjOjEOYhi/VwZ3adFsbBL+zLZxYNdkKLNWCNRktRwpnWriEsW1uDnVt2LbxSLvjvRKbR/hyvpY+0UUZFS6wCWQjGyxUydDxQ88jNM5dY58/1nxsd04I3n3Mt97SuqwBN1+4VS3SsqtbR0GU1C7ODkPoCeGVd3PNkGHPgbT7QzMwxl63Pl3i/sp0I2/gqSnKu5CDS7e2WELz0hfiOJ2v2RvIon2EEbPwx1/6zxZlMhHuGXHNZKDtyqe6Dd+EIjpwhQFW3eH7fDIirRbaPPXAYsoypS5eFD3mIWUs4yVOH9ykkdKQ9FNwg=="
    c1 = base64.b64decode(c1)
    c2 = base64.b64decode(c2)
    c3 = base64.b64decode(c3)
    print("Modulus")
    print(N1)
    print(N2)
    print(N3)
    C1 = int.from_bytes(c1, byteorder="big")
    C2 = int.from_bytes(c2, byteorder="big")
    C3 = int.from_bytes(c3, byteorder="big")

    C = chinese_remainder_theorem([(C1, N1), (C2, N2), (C3, N3)])
    M = int(root(C, 3))
    M = hex(M)[2:]

    print(unhexlify(M).decode('utf-8'))
    print("GCD")
    print(math.gcd(N1, N2))
    print(math.gcd(N2, N3))
    print(math.gcd(N1, N3))

