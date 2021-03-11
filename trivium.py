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
def trivium_one_period(A, B, C):
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


def trivium_gen_s(key, IV, len_s):
    A = IV
    while len(A) != 93: A += '0'
    B = key
    while len(B) != 84: B += '0'
    C = '0' * 108 + '111'
    s = ''

    for i in range(1152):
        A, B, C, s_i = trivium_one_period(A, B, C)
    for i in range(len_s):
        A, B, C, s_i = trivium_one_period(A, B, C)
        s += s_i
    return s


def encode(a):
    a = bin(int.from_bytes(a.encode(), 'big')).replace('b', '')

    # generate IV randomly
    IV = generate_IV()

    # get key from key.txt
    keyfile = open("key.txt", "r")
    key = keyfile.read()

    # get trivium output
    s = trivium_gen_s(key, IV, len(a))

    b = ''
    for i in range(len(s)):
        b += str((int(a[i]) + int(s[i])) % 2)

    b = IV + b
    return b


def decode(b):
    IV = b[:80]
    b = b[80:]
    keyfile = open("key.txt", "r")
    key = keyfile.read()

    s = trivium_gen_s(key, IV, len(b))
    a = ''
    for i in range(len(s)):
        a += str((int(s[i]) + int(b[i])) % 2)

    return a


if __name__ == '__main__':
    # # generate IV randomly
    # IV = generate_IV()
    #
    # # read input file
    # input_file = open("input.txt", "r")
    # X = input_file.read()
    #
    # # encode X twice with the same key
    # cipher1 = open("cipher1.txt", "w+")
    # Y = encode(X)
    # print("Wrote to file cipher1.txt")
    # cipher1.write(Y)
    #
    # cipher2 = open("cipher2.txt", "w+")
    # Y = encode(X)
    # print("Wrote to file cipher2.txt")
    # cipher2.write(Y)

    # decode from cipher1 and cipher2
    cipher1_dec = open("cipher1.txt", "r")
    Y1 = cipher1_dec.read()
    X1 = decode(Y1)

    cipher2_dec = open("cipher2.txt", "r")
    Y2 = cipher2_dec.read()
    X2 = decode(Y2)

    print("X1 is similar to X2: " + str(X1 == X2))

