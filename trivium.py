import random


# Randomly generate IV
def generate_IV():
    IV = ''
    for i in range(80):
        IV += str(random.randint(0, 1))
    return IV


# Push element e in string X
def push(X, e):
    X = str(e) + X
    X = X[:-1]
    return X


# run one period to generate s_i
def trivium(A, B, C):
    A_xor_post = (int(A[90]) * int(A[92])) ^ int(A[65]) ^ int(A[92])
    B_xor_post = (int(B[81]) * int(B[82])) ^ int(B[68]) ^ int(B[83])
    C_xor_post = (int(C[108]) * int(C[109])) ^ int(C[65]) ^ int(C[110])

    A_xor_pre = int(A[68]) ^ C_xor_post
    B_xor_pre = int(B[77]) ^ A_xor_post
    C_xor_pre = int(C[86]) ^ B_xor_post

    s = A_xor_post ^ B_xor_post ^ C_xor_post

    A = push(A, A_xor_pre)
    B = push(B, B_xor_pre)
    C = push(C, C_xor_pre)

    return A, B, C, str(s)


def encode_trivium(X, key):
    X = bin(int.from_bytes(X.encode(), 'big')).replace('b', '')

    IV = generate_IV()
    A = IV
    while len(A) != 93: A += '0'
    B = key
    while len(B) != 84: B += '0'
    C = '0' * 108 + '111'

    s = ''
    len_s = len(X)

    for i in range(1152):
        A, B, C, s_i = trivium(A, B, C)

    for i in range(len_s):
        A, B, C, s_i = trivium(A, B, C)
        s += s_i

    Y = ''
    for i in range(len_s):
        Y += str((int(X[i]) + int(s[i])) % 2)

    Y = hex(int(Y, 2))

    return Y


if __name__ == '__main__':
    input_file = open("input.txt", "r")
    X = input_file.read()

    # get key from key.txt
    keyfile = open("key.txt", "r")
    key = keyfile.read()

    # encode twice with the same key
    # got 2 different encoded texts
    cipher1 = open("cipher1.txt", "w+")
    Y = encode_trivium(X, key)
    print("Wrote to file cipher1.txt: ", Y)
    cipher1.write(Y)

    cipher2 = open("cipher2.txt", "w+")
    Y = encode_trivium(X, key)
    print("Wrote to file cipher2.txt: ", Y)
    cipher2.write(Y)
