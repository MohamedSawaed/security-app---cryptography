from mymodule import pyidea
from mymodule import pydsa
from mymodule import pyEC
import hashlib


def idea_ofb(key, IV, bytesarr):
    o = IV
    for i in range(0, len(bytesarr), 8):
        my_IDEA = pyidea.IDEA(key)
        o = my_IDEA.encrypt(o)
        r = min(len(bytesarr) - i, 8)
        t = o >> (64 - 8*r)
        txt = int.from_bytes(bytesarr[i:i + r], 'big')
        txt = txt^t
        bytesarr[i:i + r] = bytearray(txt.to_bytes(r, 'big'))
    
    return bytesarr

# The symmetric IDEA key definition:
key = 0x006400c8012c019001f4025802bc0320


# El Gamal key delivery:
print("\nAlice encrypts her symmetric IDEA key using Bob's public key...\n")
elgamal = pyEC.ElGamal()
elgamal.curve = pyEC.P256
C1, C2 = elgamal.encrypt(key.to_bytes(16, 'big'), pyEC.publickey)
print("Key before and after encryption:", hex(key), "--->\n", "\nC1 =", "(",hex(C1.x), ",", hex(C1.y), ")", "\n\nC2 =", "(", hex(C2.x), ",", hex(C2.y), ")")


IV = 0xEEA37DEE36032EB1


print("\n\nReading Alice's sound file...")
plainbytes = bytearray()
file = open("sound.bin", "rb")

byte = file.read(1)
while byte:
    plainbytes += byte
    byte = file.read(1)
file.close()

dsa_key = pydsa.dsa_key

m = hashlib.sha1()
m.update(str(plainbytes).encode('utf-8'))
message = int("0x" + m.hexdigest(), 0)

print("Alice signs her file using DSA signature with her private key...")
r, s = pydsa.dsa_sign(dsa_key["Q"], dsa_key["P"], dsa_key["G"], dsa_key["priv"], message)
print("Signature output = (r,s) = (",hex(r),",",hex(s), ")")
plainbytes = plainbytes + r.to_bytes(20, 'big') + s.to_bytes(20, 'big')
print("Sound file with signature concatenated by the end =", hex(int.from_bytes(plainbytes, 'big')))

# IDEA - OFB encryption
print("\n\nAlice encrypts the entire plaintext sequence...")
cipherbytes = idea_ofb(key, IV, plainbytes)
print("Ciphertext =", hex(int.from_bytes(cipherbytes, 'big')))

# IDEA - OFB decryption Bob
print("\n\n\nBob decrypts the encrypted symmetric key Alice sent him, using his private El-Gamal key...")
M = elgamal.decrypt(pyEC.privatekey, C1, C2)
assert key == int.from_bytes(M, 'big')

print("\nBob decrypts the ciphertext file Alice sent him, using the symmetric key")
plainbytes = idea_ofb(key, IV, cipherbytes)
R = int.from_bytes(plainbytes[len(plainbytes) - 40:len(plainbytes) - 20], 'big')
S = int.from_bytes(plainbytes[len(plainbytes) - 20:len(plainbytes)], 'big')
m = hashlib.sha1()
m.update(str(plainbytes[0:len(plainbytes) - 40]).encode('utf-8'))
message = int("0x" + m.hexdigest(), 0)
print("Bob verifies the file was sent from Alice using her public DSA key")
assert pydsa.dsa_verify(R, S, dsa_key["G"], dsa_key["P"], dsa_key["Q"], dsa_key["pub"], message)
print("File was valid")
print("\nFile after decryption:", hex(int.from_bytes(plainbytes[0:len(plainbytes) - 40], 'big')))


