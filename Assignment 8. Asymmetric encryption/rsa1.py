p = 398075086424064937397125500550386491199064362342526708406385189575946388957261768583317
q = 472772146107435302536223071973048224632914695302097116459852171130520711256363590397527
e = 0x010001
n = 0xC2CBB24FDBF923B61268E3F11A3896DE4574B3BA58730CBD652938864E2223EEEB704A17CFD08D16B46891A61474759939C6E49AAFE7F2595548C74C1D7FB8D24CD15CB23B4CD0A3
phi = (p -1)*(q-1)
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def modinv(a, m):
    gcd, x, y = egcd(a, m)
    if gcd != 1:
        return None  # modular inverse does not exist
    else:
        return x % m

d = modinv(e, phi)
from Crypto.PublicKey import RSA
key = RSA.construct((n,e,d))
f = open("private.pem", "wb")
f.write(key.export_key())
f.close()