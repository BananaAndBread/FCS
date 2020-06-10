import copy
from fractions import Fraction
from math import sqrt
import string

def create_vector(text):
    alphabet = string.ascii_lowercase
    vector = []
    for i in text:
        vector.append([alphabet.index(i)])
    return vector
def determinant_recursive(A, total=0):
    indices = list(range(len(A)))
    if len(A) == 2 and len(A[0]) == 2:
        val = A[0][0] * A[1][1] - A[1][0] * A[0][1]
        return val
    for fc in indices:
        As = copy.deepcopy(A)
        As = As[1:]
        height = len(As)

        for i in range(height):
            As[i] = As[i][0:fc] + As[i][fc + 1:]

        sign = (-1) ** (fc % 2)
        sub_det = determinant_recursive(As)
        total += sign * A[0][fc] * sub_det

    return total

def matmult(a,b):
    zip_b = zip(*b)
    zip_b = list(zip_b)
    return [[sum(ele_a*ele_b for ele_a, ele_b in zip(row_a, col_b))
             for col_b in zip_b] for row_a in a]

first_matrix =[[1,2], [3,4]]
second_matrix = [[1],[2]]


def create_A_matrix(key):
    n=int(sqrt(len(key)))
    alphabet = string.ascii_lowercase
    j=0
    matrix = []
    for _ in range(n):
        temp = []
        for _ in range(n):
            temp.append(Fraction(alphabet.index(key[j]), 1))
            j=j+1
        matrix.append(temp)
    return matrix

def modInverse(a, m):
    a = a%m
    for x in range(1, m):
       if ((a*x) % m == 1):
          return x
    raise Exception('No modular inverse of this matrix, choose another key ')


def create_i_matrix(num_rows, scalar=1):
    matrix = list()
    for j in range(num_rows):
        temp = []
        for i in range(num_rows):
            if j==i:
                temp.append(Fraction(1*scalar,1))
            else:
                temp.append(Fraction(0,1))
        matrix.append(temp)
    return matrix


def transposeMatrix(m):
    N = len(m)
    B = create_i_matrix(N)
    for i in range(N):
        for j in range(N):
            B[i][j] = m[j][i]
    return B

def getMatrixMinor(m,i,j):
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

def getMatrixInverse(m):
    determinant = determinant_recursive(m)
    if determinant==0:
        raise ("this matrix is not invertible, choose another key ")
    #special case for 2x2 matrix:
    if len(m) == 2:
        return [[m[1][1]/determinant, -1*m[0][1]/determinant],
                [-1*m[1][0]/determinant, m[0][0]/determinant]]

    #find matrix of cofactors
    cofactors = []
    for r in range(len(m)):
        cofactorRow = []
        for c in range(len(m)):
            minor = getMatrixMinor(m,r,c)
            cofactorRow.append(((-1)**(r+c)) * determinant_recursive(minor))
        cofactors.append(cofactorRow)
    cofactors = transposeMatrix(cofactors)
    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] = cofactors[r][c]/determinant
    return cofactors

def invert_matrix(m):
    IM = getMatrixInverse(m)
    determinant = determinant_recursive(m)
    if determinant==0:
        raise Exception("this matrix is not invertible, choose another key ")
    n = len(m)
    IM = matmult(IM, create_i_matrix(n, determinant))

    determinant = modInverse(determinant, 26)
    IM = matmult(IM, create_i_matrix(n, determinant))
    for i in range(len(IM)):
        for j in range(len(IM)):
            IM[i][j] = IM[i][j] % 26


    return IM

def encrypt(key, text):
    print("\nEncryption")
    key = key.lower()
    text = text.lower()
    print(f"key: {key} text: {text}")
    alphabet = string.ascii_lowercase
    key_matrix =create_A_matrix(key)
    print(f"Key matrix created:\n {key_matrix}")
    n=int(sqrt(len(key)))
    temp=[]
    for i in range(0,len(text),n):
        vector = create_vector(text[i:i+n])
        print(f"{i} text vector created:\n {vector}")
        new_vector = matmult(key_matrix, vector)
        temp.append(new_vector)
    text=''
    print(f"Encrypted text matrix created: \n {temp}")
    for i in temp:
        for j in i:
            temp_2 = j[0].numerator
            text = text + alphabet[temp_2%26]
    print(f"Encrypted text: \n {text}")
    return text

def decrypt(key, text):
    print("\nDecryption")
    key = key.lower()
    text = text.lower()
    print(f"key: {key} encrypted_text: {text}")
    alphabet = string.ascii_lowercase
    key_matrix =create_A_matrix(key)
    key_matrix=invert_matrix(key_matrix)
    print(f"Inverted key matrix created:\n {key_matrix}")
    n=int(sqrt(len(key)))
    temp=[]
    for i in range(0,len(text),n):
        vector = create_vector(text[i:i+n])
        new_vector = matmult(key_matrix, vector)
        print(f"{i} e encrypted text vector created:\n {vector}")
        temp.append(new_vector)
    text=''
    print(f"Decrypted text matrix created:\n {temp}")
    for i in temp:
        for j in i:
            text = text + alphabet[j[0].numerator%26]
    print(f"Decrypted text {text}")
    return text



A = [[1,5],[3,4]]
for i in range(len(A)):
    for j in range(len(A)):
        A[i][j]=Fraction(A[i][j], 1)

key = "bowl"
text = "letsencodesometext"
encrypted = encrypt(key, text)
decrypt(key, encrypted)
