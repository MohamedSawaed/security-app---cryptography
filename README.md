# security-app---cryptography
security app - cryptography

The study of this project:

I started by learning about the relevant topics through the lectures
and exercises in the course, then I approached external sources of
information (like IDEA), blogs and articles by cryptology experts. I
delved into the course’s materials and tried to reach a good
understanding of the project topics, to understand how to implement
the various algorithms.

Project Flow:


After delving into the relevant material, I actually started
working on the IDEA algorithm and took a small sound file, and tested it
with IDEA to see that the encryption is legal. I implemented the DSA
and El Gamal EC algorithms and tested them to see that the symmetric
key is encrypted and also that the signature is valid for various sound
files. After I implemented the algorithms above, I did a whole
system simulation that combines all these algorithms together when El
Gamal EC was used to pass the symmetric key, DSA was used to sign
the sound file, and IDEA was used to encrypt the file with the signature,
and decrypt it on the receiving end.

Obtained results:

![image](https://user-images.githubusercontent.com/98653093/158760698-f36c4e11-7a1b-4308-974e-5f5c4cc7c734.png)



The project results can be described by the chart above. The user has to
enter his desired sound file into the app, the app signs his file using DSA
and encrypts the file + signature using IDEA + OFB, the app also sends
the symmetric key (IDEA key) to the receiver's end through a secured
channel (El Gammal EC), The receiver decrypts the entire message and
verifies that the signature is valid using DSA public key.


