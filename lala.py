"""
1. Key Generation:
   - Choose two large prime numbers: p, q
   - Compute n = p * q (modulus)
   - Compute φ(n) = (p-1) * (q-1) (Euler's totient function)
   - Choose a public exponent e (commonly 65537)
   - Compute the private exponent d such that d * e ≡ 1 (mod φ(n))

2. Encryption:
   - Convert plaintext message to an integer m
   - Compute ciphertext c = m^e mod n

3. Decryption:
   - Compute plaintext m = c^d mod n
   - Convert the integer back to the original message
"""
from Crypto.Util.number import isPrime, long_to_bytes
from string import ascii_letters, digits
from itertools import combinations
from sympy import divisors
from math import log2

def get_prime_candidates(modulus: int):
    """Find prime candidates from the divisors of (modulus - 1)."""
    return [x + 1 for x in divisors(modulus - 1) if isPrime(x + 1)]

def filter_valid_primes(prime_list):
    """Filter primes that are close to 127-bit size."""
    return [p for p in prime_list if log2(p) // 1 == 127]

def decrypt_message(ciphertext: int, exponent: int, primes: list):
    """Attempt decryption using different prime combinations."""
    charset = ascii_letters + digits    
    for p, q in combinations(primes, 2):
        try:
            decrypted = long_to_bytes(pow(ciphertext, exponent, p * q))
            decoded_message = decrypted.decode("ascii")
            if all(c in charset for c in decoded_message):
                return decoded_message
        except UnicodeDecodeError:
            continue
    return None

def decrypt():
    ciphertext = 16397033758829274596113868636792378417270779111016278337049092851849768784178
    exponent = 3179008223760288311914866770887612256153603179393241588778642261701153272613
    public_exponent = 65537
    prime_candidates = get_prime_candidates(exponent * public_exponent)
    valid_primes = filter_valid_primes(prime_candidates)
    decrypted_message = decrypt_message(ciphertext, exponent, valid_primes)
    if decrypted_message:
        print(f"Decrypted String: {decrypted_message}")
    else:
        print("No valid decrypted string found.")

decrypt()
