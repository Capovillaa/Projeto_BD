import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class Security:
    
    SALT_SIZE = 16

    @classmethod
    def kdf(cls,senha: bytes, salt: bytes ) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=1_200_000,
        )

        key = base64.urlsafe_b64encode(kdf.derive(senha))
        return key
    
    @classmethod
    def encrypt(cls,senha: bytes, mensagem: bytes) -> bytes:

        salt = os.urandom(cls.SALT_SIZE)

        key = cls.kdf(senha,salt)
        f = Fernet(key)

        token = f.encrypt(mensagem)

        return salt + token
    
    @classmethod
    def decrypt(cls,senha: bytes, mensagem_criptografada: bytes) -> bytes:

        salt = mensagem_criptografada[:cls.SALT_SIZE]
        token = mensagem_criptografada[cls.SALT_SIZE:]

        key = cls.kdf(senha,salt)
        f = Fernet(key)

        mensagem_descriptografada = f.decrypt(token)
        return mensagem_descriptografada
