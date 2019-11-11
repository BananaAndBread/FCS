from hash import crack
#hash.py can be found here: https://github.com/s0md3v/Hash-Buster/blob/master/hash.py
file = open("/home/banana_and_bread/Downloads/hashes")
file_out = open("/home/banana_and_bread/Downloads/output", "w")
strings = set()
cracked_already = dict()
for line in file:
    line = line.strip()
    if line not in cracked_already:
        cracked = crack(line)
        cracked_already[line]=cracked
    else:
        cracked = cracked_already[line]
    print(cracked, end="")