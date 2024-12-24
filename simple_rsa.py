import random
from Crypto.Util.number import getPrime, inverse, GCD
from math import gcd

# RSA Implementation
def generate_rsa_keypair():
    key_size = 9

    p = getPrime(key_size // 2)
    q = getPrime(key_size // 2)
    while p == q:
        q = getPrime(key_size // 2)

    n = p * q
    phi = (p - 1) * (q - 1)

    e = 3
    while gcd(e, phi) != 1:
        e += 2

    d = inverse(e, phi)

    return ((e, n), (d, n)), (p, q)

# Utility functions for string conversion
def string_to_chunks(s, n):
    max_chunk_size = max(1, (n.bit_length() - 1) // 8)  # Ensure max_chunk_size is at least 1
    encoded = s.encode('utf-8')
    return [encoded[i:i + max_chunk_size] for i in range(0, len(encoded), max_chunk_size)]

def chunks_to_string(chunks):
    return b''.join(chunks).decode('utf-8')

def chunk_to_int(chunk):
    return int.from_bytes(chunk, byteorder='big')

def int_to_chunk(i, n):
    # Dynamically calculate the size required for the chunk
    byte_size = (i.bit_length() + 7) // 8
    return i.to_bytes(byte_size, byteorder='big')

import base64

# Encryption
def encrypt(public_key, plaintext):
    e, n = public_key
    chunks = string_to_chunks(plaintext, n)
    ciphertext_chunks = [pow(chunk_to_int(chunk), e, n) for chunk in chunks]
    # Convert ciphertext chunks into a single "nonsense" string
    ciphertext_bytes = b''.join(int_to_chunk(c, n) for c in ciphertext_chunks)
    return base64.b64encode(ciphertext_bytes).decode('utf-8')  # Encode to base64 string

# Decryption
def decrypt(private_key, ciphertext):
    d, n = private_key
    # Decode from base64 and split into chunks
    ciphertext_bytes = base64.b64decode(ciphertext.encode('utf-8'))
    chunk_size = (n.bit_length() + 7) // 8
    ciphertext_chunks = [
        chunk_to_int(ciphertext_bytes[i:i + chunk_size])
        for i in range(0, len(ciphertext_bytes), chunk_size)
    ]
    decrypted_chunks = [int_to_chunk(pow(c, d, n), n) for c in ciphertext_chunks]
    return chunks_to_string(decrypted_chunks)

def modular_inverse(e, phi):
    old_r, r = phi, e
    old_s, s = 1, 0
    old_t, t = 0, 1
    
    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t
    
    # Ensure the modular inverse is positive
    return old_t % phi

def reconstruct_private_key(e, p, q):
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # Check that e is valid
    if gcd(e, phi) != 1:
        raise ValueError("e is not coprime with φ(n). Choose a different e.")
    
    # Compute the private key exponent d
    d = modular_inverse(e, phi)
    return (d, n)
