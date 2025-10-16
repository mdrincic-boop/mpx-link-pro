from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
import hashlib


class AudioEncryption:
    def __init__(self, password: str = None):
        self.enabled = False
        self.key = None
        self.cipher = None

        if password:
            self.set_password(password)

    def set_password(self, password: str):
        salt = b'mpx_audio_salt_v1'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        self.key = kdf.derive(password.encode())
        self.enabled = True

    def encrypt(self, data: bytes) -> bytes:
        if not self.enabled:
            return data

        iv = os.urandom(16)
        cipher = Cipher(
            algorithms.AES(self.key),
            modes.CFB(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        encrypted = encryptor.update(data) + encryptor.finalize()

        return iv + encrypted

    def decrypt(self, data: bytes) -> bytes:
        if not self.enabled:
            return data

        iv = data[:16]
        encrypted = data[16:]

        cipher = Cipher(
            algorithms.AES(self.key),
            modes.CFB(iv),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        decrypted = decryptor.update(encrypted) + decryptor.finalize()

        return decrypted


class AuthenticationManager:
    def __init__(self, shared_secret: str = None):
        self.shared_secret = shared_secret
        self.enabled = shared_secret is not None

    def generate_token(self, timestamp: float) -> str:
        if not self.enabled:
            return ""

        message = f"{timestamp}:{self.shared_secret}"
        return hashlib.sha256(message.encode()).hexdigest()

    def verify_token(self, token: str, timestamp: float, tolerance: float = 5.0) -> bool:
        if not self.enabled:
            return True

        import time
        current_time = time.time()

        if abs(current_time - timestamp) > tolerance:
            return False

        expected_token = self.generate_token(timestamp)
        return token == expected_token


class FECEncoder:
    def __init__(self, redundancy: int = 2):
        self.redundancy = redundancy
        self.enabled = redundancy > 0

    def encode(self, data: bytes) -> bytes:
        if not self.enabled:
            return data

        checksum = hashlib.md5(data).digest()
        return data + checksum

    def decode(self, data: bytes) -> tuple[bytes, bool]:
        if not self.enabled:
            return data, True

        if len(data) < 16:
            return data, False

        payload = data[:-16]
        received_checksum = data[-16:]
        calculated_checksum = hashlib.md5(payload).digest()

        valid = received_checksum == calculated_checksum
        return payload, valid
