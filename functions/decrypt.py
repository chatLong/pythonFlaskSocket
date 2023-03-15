import os
from Crypto.Cipher import AES

class decrypt:
    def decrypt_directory(dir, key):
        for dirpath, dirnames, filenames in os.walk(dir):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                with open(filepath, 'rb') as f:
                    nonce = f.read(16)
                    tag = f.read(16)
                    ciphertext = f.read()

                cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
                plaintext = cipher.decrypt_and_verify(ciphertext, tag)

                with open(filepath, 'wb') as f:
                    f.write(plaintext)

#key = get_random_bytes(16)
#decrypt_directory("../testEncryptionDir", key)
