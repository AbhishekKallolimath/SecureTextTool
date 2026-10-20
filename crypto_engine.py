
import os
import base64
import json

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt


# Security settings
SALT_LENGTH = 16
NONCE_LENGTH = 12
KEY_LENGTH = 32  # 32 bytes = 256 bits
SCRYPT_N = 2**14
SCRYPT_R = 8
SCRYPT_P = 1


def derive_key(password: str, salt: bytes) -> bytes:
    """Derive a secure encryption key from a password."""
    if not password:
        raise ValueError("Password cannot be empty.")

    kdf = Scrypt(
        salt=salt,
        length=KEY_LENGTH,
        n=SCRYPT_N,
        r=SCRYPT_R,
        p=SCRYPT_P,
    )
    return kdf.derive(password.encode("utf-8"))


def encrypt_text(text: str, password: str) -> str:
    """Encrypt text and return a Base64-encoded JSON envelope."""
    if not isinstance(text, str) or not text:
        raise ValueError("Text cannot be empty.")

    salt = os.urandom(SALT_LENGTH)
    nonce = os.urandom(NONCE_LENGTH)

    key = derive_key(password, salt)
    aesgcm = AESGCM(key)

    ciphertext = aesgcm.encrypt(
        nonce,
        text.encode("utf-8"),
        None,
    )

    envelope = {
        "version": 1,
        "algorithm": "AES-256-GCM",
        "kdf": "scrypt",
        "salt": base64.b64encode(salt).decode("ascii"),
        "nonce": base64.b64encode(nonce).decode("ascii"),
        "ciphertext": base64.b64encode(ciphertext).decode("ascii"),
    }

    json_data = json.dumps(envelope, separators=(",", ":")).encode("utf-8")
    return base64.b64encode(json_data).decode("ascii")


def decrypt_text(encrypted_text: str, password: str) -> str:
    """Decrypt an envelope produced by encrypt_text()."""
    if not isinstance(encrypted_text, str) or not encrypted_text.strip():
        raise ValueError("Encrypted text cannot be empty.")

    try:
        decoded = base64.b64decode(encrypted_text, validate=True)
        envelope = json.loads(decoded.decode("utf-8"))

        if not isinstance(envelope, dict):
            raise ValueError("Invalid encrypted data format.")

        if envelope.get("version") != 1:
            raise ValueError("Unsupported encrypted data version.")

        if envelope.get("algorithm") != "AES-256-GCM":
            raise ValueError("Unsupported encryption algorithm.")

        if envelope.get("kdf") != "scrypt":
            raise ValueError("Unsupported key derivation method.")

        salt = base64.b64decode(envelope["salt"], validate=True)
        nonce = base64.b64decode(envelope["nonce"], validate=True)
        ciphertext = base64.b64decode(
            envelope["ciphertext"], validate=True
        )

        if len(salt) != SALT_LENGTH:
            raise ValueError("Invalid salt length.")

        if len(nonce) != NONCE_LENGTH:
            raise ValueError("Invalid nonce length.")

        if len(ciphertext) < 16:
            raise ValueError("Encrypted data is incomplete.")

        key = derive_key(password, salt)
        aesgcm = AESGCM(key)

        plaintext = aesgcm.decrypt(nonce, ciphertext, None)
        return plaintext.decode("utf-8")

    except InvalidTag:
        raise ValueError(
            "Decryption failed: incorrect password or modified encrypted data."
        ) from None
    except (KeyError, TypeError, UnicodeDecodeError, json.JSONDecodeError):
        raise ValueError("Invalid or corrupted encrypted data.") from None
    except (base64.binascii.Error,):
        raise ValueError("Invalid Base64 encrypted data.") from None
