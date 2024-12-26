from shor import *
from simple_rsa import *

print("######################################")
(public_key, private_key), (p, q) = generate_rsa_keypair()
print(f"Generated RSA Keypair:\n")
print(f"Public Key: {public_key}")
print(f"Private Key: {private_key}\n")
print("######################################")

plaintext = 'Quant.Bond'
ciphertext = encrypt(public_key, plaintext)
print(f"\nPlaintext: {plaintext}")
print("\nEncrypting...")
print(f"Ciphertext: {ciphertext}")
print("######################################")

print("Breaking Encryption...")
n = public_key[1]
p = shor_factorization(n)
print("Encryption Broken!/n")
q = n // p
reconstructed_key = reconstruct_private_key(public_key[0], p, q)
print("This is the reconstructed Private Key:", reconstructed_key)

broken = decrypt(reconstructed_key, ciphertext)
print("\nDecrypting...")
print(f"Decrypted Text: {broken}")
