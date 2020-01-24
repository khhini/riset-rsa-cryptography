import math
from random import randrange
from random import getrandbits


# -----------------------------------------------------------
# primality check dengan menggunakan algoritma Miller-Rabin
# ----------------------------------------------------------
def is_prime(n, k=128):
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False

    s = 0
    r = n - 1
    while r & 1 == 0:
        s += 1
        r //= 2

    for _ in range(1):
        a = randrange(2, n - 1)
        x = pow(a, r, n)
        if x != 1 and x != n - 1:
            j = 1
            while j < s and x != n - 1:
                x = pow(x, 2, n)
                if x == 1:
                    return False
                j += 1
            if x != n - 1:
                return False

    return True


def getPrime(n):
    while(True):
        p = getrandbits(n)
        p |= (1 << n - 1) | 1
        if(is_prime(p)):
            return p


# -----------------------------------------------------------
# menemukan gcd dua buah bilangan dengan Algoritma Euclidean
# -----------------------------------------------------------
def gcd(x, y):
    if(y == 0):
        return x
    else:
        return gcd(y, x % y)


# -----------------------------------------------------------
# menemukan lcm dengan formula x*y = lcm(x, y) * gcd(x, y)
# -----------------------------------------------------------
def lcm(x, y):
    return int(x*y / gcd(x, y))


# -----------------------------------------------------------
# menghitung kunci dekripsi dengan fungsi totient carmichael
# -----------------------------------------------------------
def calculate_d(e, totient):
    q = 1
    while(True):
        if((totient * q + 1) % e == 0):
            return int((totient*q+1) / e)
        else:
            q += 1


# ----------------------------------------------------------------------
# generate key dengan menentukan e dimana e realtif prima dengan totient
# ----------------------------------------------------------------------
def generateKey(e):
    while(True):
        p = getPrime(16)
        q = getPrime(16)
        totient = lcm(p-1, q-1)
        if(math.gcd(e, totient) == 1):
            return {
                'n': p*q,
                'd': calculate_d(e, totient),
                'e': e
                }


# ----------------------------------------------------
# encrypsi dengan formula c = m^e mod n
# ----------------------------------------------------
def encrypt(plaintext, e, n):
    ciphertext = ""
    for i in plaintext:
        m = ord(i)
        m = int(m)
        c = pow(m, e, n)
        if(len(str(c)) < 10):
            for i in range(10 - len(str(c))):
                ciphertext += '0'
        ciphertext += str(c)
    return ciphertext


# ----------------------------------------------------
# encrypsi dengan formula m = c^d mod n
# ----------------------------------------------------
def decrypt(ciphertext, d, n):
    ciphertext = [ciphertext[i:i+10] for i in range(0, len(ciphertext), 10)]
    plaintext = ''
    for c in ciphertext:
        m = pow(int(c), d, n)
        plaintext += chr(m)
    return plaintext


# ------------------------------------------
# main program
# ------------------------------------------
while(True):
    print("menu :\n1. Pembangkitan Kunci\n2. Enkripsi\n3. Dekripsi\n4. Exit")
    menu = int(input("Pilih menu : "))
    print("-------------------------------")
    if(menu == 1):
        e = int(input("Masukkan kunci publik (e) : "))
        key = generateKey(e)
        print("Output : ")
        print("-------------------------------")
        print("totient :", key['n'])
        print("Kunci Private (d) :", key['d'])

    elif(menu == 2):
        m = input("Masukkan plaintext : ")
        ciphertext = encrypt(m, key['e'], key['n'])
        print("Ciphertext :", ciphertext)

    elif(menu == 3):
        c = input("Masukkan ciphertext : ")
        plaintext = decrypt(c, key['d'], key['n'])
        print("Plaintext :", plaintext)

    elif(menu == 4):
        exit(0)
    print("-------------------------------")
    print("")
