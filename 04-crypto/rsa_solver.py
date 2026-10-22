#!/usr/bin/env python3
"""
Standalone RSA CTF Solver Script
Supports:
1. Small e attack (Direct cube root / gmpy2)
2. FactorDB auto-lookup for N (finds p and q)
3. Fermat's factorization (when p and q are close)
"""

import math
import sys
import json
import urllib.request

try:
    from Crypto.Util.number import long_to_bytes, inverse
except ImportError:
    print("Run: pip install pycryptodome gmpy2")
    sys.exit(1)

# ==============================================================================
# INPUT VALUES (Fill in challenge parameters)
# ==============================================================================
n = 0
e = 65537
c = 0

# ==============================================================================
# ATTACK 1: SMALL E (e = 3, e = 5, when c < n)
# ==============================================================================
def solve_small_e(c, e):
    print("[*] Testing Small e attack (Integer root)...")
    try:
        import gmpy2
        m, is_exact = gmpy2.iroot(c, e)
        if is_exact:
            pt = long_to_bytes(int(m))
            print(f"[+] Small e SUCCESS! Flag: {pt}")
            return pt
    except ImportError:
        # Fallback without gmpy2 (Python 3.8+ integer root approximation)
        pass
    print("[-] Small e failed or requires higher k*N iterations.")
    return None

# ==============================================================================
# ATTACK 2: FACTORDB (Lookup known p and q from factordb.com)
# ==============================================================================
def solve_factordb(n, e, c):
    print(f"[*] Querying FactorDB for n={n}...")
    url = f"http://factordb.com/api?query={n}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            status = data.get('status')
            factors = data.get('factors')
            
            # Status "FF" means fully factored
            if factors and len(factors) >= 2:
                p = int(factors[0][0])
                q = int(factors[1][0])
                if p * q == n:
                    print(f"[+] Found factors on FactorDB!\np = {p}\nq = {q}")
                    phi = (p - 1) * (q - 1)
                    d = inverse(e, phi)
                    m = pow(c, d, n)
                    pt = long_to_bytes(m)
                    print(f"[+] Flag: {pt}")
                    return pt
    except Exception as err:
        print(f"[-] FactorDB error: {err}")
    print("[-] FactorDB did not have factors.")
    return None

# ==============================================================================
# ATTACK 3: FERMAT FACTORIZATION (p and q are very close)
# ==============================================================================
def fermat_factor(n, max_iter=10000000):
    print("[*] Running Fermat's Factorization (close primes)...")
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
        print("[-] Fermat reached max iterations.")
        return None
    b = math.isqrt(b2)
    p = a - b
    q = a + b
    if p * q == n and p > 1:
        print(f"[+] Fermat SUCCESS!\np = {p}\nq = {q}")
        return p, q
    return None

# ==============================================================================
# MAIN RUNNER
# ==============================================================================
if __name__ == '__main__':
    if n == 0 or c == 0:
        print("Usage: Edit script and input n, e, and c values at the top.")
        sys.exit(0)
    
    # 1. Try small e
    if e <= 5:
        res = solve_small_e(c, e)
        if res: sys.exit(0)
        
    # 2. Try FactorDB
    res = solve_factordb(n, e, c)
    if res: sys.exit(0)

    # 3. Try Fermat
    primes = fermat_factor(n)
    if primes:
        p, q = primes
        phi = (p - 1) * (q - 1)
        d = inverse(e, phi)
        m = pow(c, d, n)
        print(f"[+] Flag: {long_to_bytes(m)}")
