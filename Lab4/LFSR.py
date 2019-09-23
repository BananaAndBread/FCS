def LFSR(string, num_states):
    answer = ""
    for i in range(num_states):
        last=str(int(string[0])^int(string[2])^int(string[5]))
        answer = string[0] + answer
        for i in range(len(string)-1):
            string= string[:i] + string[i+1] + string[i + 1:]

        string = string[:7] +last
        print(string)
    return answer

def LFSR_back(string, num_states):
    for i in range(num_states):
        part_xor=str(int(string[1])^int(string[4]))
        result_xor = string[7]
        zero_char = str(int(result_xor)^int(part_xor))
        for i in range(len(string)-1, 0, -1):
            string= string[:i] + string[i-1] + string[i + 1:]

        string = zero_char + string[1:]
        print(string)



def LFSR(string, num_states):
    answer = ""
    for i in range(num_states):
        last=str(int(string[0])^int(string[2])^int(string[5]))
        answer = answer + string[0]
        for i in range(len(string)-1):
            string= string[:i] + string[i+1] + string[i + 1:]

        string = string[:7] +last
        print(string)
    return answer

def decrypt(encrypted, key):
    decrypted = ""
    for i in range(len(encrypted)):
        decrypted = decrypted + str(int(encrypted[i])^int(key[i]))
    return decrypted

key = LFSR("01011101", 4)
print()
LFSR_back("01011101", 4)

encrypted = "1111"
print()
print(decrypt(encrypted, key))


