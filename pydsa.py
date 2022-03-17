import os
import random



dsa_key = {
    "Q": 1218442816993522937915646204915776994404649089503,
    "P": 11220611807188583130302963536190351192186270126479330588604287699892081267588448305835704397593153801135202051719876685351614175538253684346816652027037363,
    "G": 11189361631195852088154673407566885728548496486362662112597687161142104619469702160215294558351391466982303919803857229515093575816938371433954759500448775,
    "pub": 4572510396595314270786423212039255215498677297795049756997099191729339616558419010431226927123876238239229467750410441342637393785565872285607741290303779,
    "priv": 148102768779017960166999813987055538077373228390
    }



def _random_s(min, max):
    """
    Helper function to select a random number.
    :param min: smallest random number
    :param max: largest random number
    :return: random number
    """
    
    return random.randrange(min, max)

def modexp(g, u, p):
   """Computes s = (g ^ u) mod p
   Args are base, exponent, modulus
   (see Bruce Schneier's book, _Applied Cryptography_ p. 244)
   """
   s = 1
   while u != 0:
      if u & 1:
         s = (s * g) % p
      u >>= 1
      g = (g * g) % p
   return s


def _digits_of_n(n, b):
    """
    Return the list of the digits in the base 'b'
    representation of n, from LSB to MSB
    :param n: integer
    :param b: base
    :return: number of digits in the base b
    """
    digits = []
    while n:
        digits.append(int(n % b))
        n /= b
    return digits

def dsa_sign(q, p, g, x, message):
    """
    Create a DSA signature of a message
    using the private part of a DSA keypair.
    The message is integer and usually a SHA-1 hash.
    public key: q,p,g, y
    public key: q,p,g, x
    :param q: selected prime divisor
    :param p: computed prime modulus: (p-1) mod q = 0
    :param g: computed:
              1 < g < p, g**q mod p = 1
              and
              g = h**((p-1)/q) mod p
    :param x: selected: 0 < x < q
    :param message: message to sign
    :return: DSA signature (s1,s2) sometimes called (r,s)
    """
    while True:
        k = _random_s(2, q-1)
        r = 0
        s = 0
        m = modexp(g, k, p)
        r = m % q
        if r == 0:
            continue
        temp_s = modexp(k, q-2, q) * (message + x * r)
        s = temp_s % q
        if s == 0:
            continue
        return (int(r), int(s))


def dsa_verify(r, s, g, p, q, y, message):
    """
    Verify the DSA signature of a message
    using the public part of a DSA keypair.
    The message is integer SHA-1 HASH
    """
    if not r > 0:
        return False
    if not r < q:
        return False
    if not s > 0:
        return False
    if not s < q:
        return False
    w = modexp(s, q-2, q)
    u1 = (message * w) % q
    u2 = (r * w) % q
    # v = (((g**u1)*(y**u2)) % p ) % q # correct formula but slooooow!
    # because of that, we use modulo arithmetic to calculate intermediate values:
    u1 = pow(g, u1, p)
    u2 = pow(y, u2, p)
    v = u1 * u2 % p % q
    if v == r:
        return True
    return False