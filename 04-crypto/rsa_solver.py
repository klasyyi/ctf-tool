#!/usr/bin/env python3
"""
RSA CTF solver script.
Automates three common attack vectors:
1. Small public exponent attack (integer root).
2. FactorDB prime factorization lookup.
3. Fermat factorization for close prime numbers.
"""

import math
import sys
import json
import urllib.request

try:
    from Crypto.Util.number import long_to_bytes, inverse
except ImportError:
    print("Dependencies missing. Install with: pip install pycryptodome gmpy2")
    sys.exit(1)

# Input challenge parameters
n = 0
e = 65537
c = 0

def solve_small_e(c, e):
    """Calculates direct integer root when e is small and c < n."""
    print("[*] Testing small exponent root...")
    try:
        import gmpy2
        m, is_exact = gmpy2.iroot(c, e)
        if is_exact:
            pt = long_to_bytes(int(m))
            print(f"[+] Decrypted text: {pt}")
            return pt
    except ImportError:
        pass
    print("[-] Small exponent attack failed.")
    return None

def solve_factordb(n, e, c):
    """Queries FactorDB API to retrieve known prime factors for modulus n."""
    print(f"[*] Querying FactorDB for n={n}...")
    url = f"http://factordb.com/api?query={n}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            factors = data.get('factors')
            if factors and len(factors) >= 2:
                p = int(factors[0][0])
                q = int(factors[1][0])
                if p * q == n:
                    print(f"[+] Factors found: p={p}, q={q}")
                    phi = (p - 1) * (q - 1)
                    d = inverse(e, phi)
                    m = pow(c, d, n)
                    pt = long_to_bytes(m)
                    print(f"[+] Decrypted text: {pt}")
                    return pt
    except Exception as err:
        print(f"[-] FactorDB request failed: {err}")
    return None

def fermat_factor(n, max_iter=10000000):
    """Factors n when prime factors p and q are close to each other."""
    print("[*] Testing Fermat factorization...")
    a = math.isqrt(n)
    if a * a < n:
        a += 1
    b2 = a * a - n
    count = 0
    while not math.isqrt(b2) ** 2 == b2 and count < max_iter:
        a += 1
        b2 = a * a - n
        count += 1
    if count >= max_iter:
        print("[-] Fermat reached maximum iterations.")
        return None
    b = math.isqrt(b2)
    p = a - b
    q = a + b
    if p * q == n and p > 1:
        print(f"[+] Factors found: p={p}, q={q}")
        return p, q
    return None

if __name__ == '__main__':
    if n == 0 or c == 0:
        print("Set values for n, e, and c at the top of the script.")
        sys.exit(0)

    if e <= 5:
        if solve_small_e(c, e):
            sys.exit(0)

    if solve_factordb(n, e, c):
        sys.exit(0)

    primes = fermat_factor(n)
    if primes:
        p, q = primes
        phi = (p - 1) * (q - 1)
        d = inverse(e, phi)
        m = pow(c, d, n)
        print(f"[+] Decrypted text: {long_to_bytes(m)}")
