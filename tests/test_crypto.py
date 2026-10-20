
import pytest

from crypto_engine import encrypt_text, decrypt_text


def test_encrypt_and_decrypt():
    message = "Hello, QuantumVault!"
    password = "StrongPassword123!"

    encrypted = encrypt_text(message, password)

    assert encrypted != message
    assert decrypt_text(encrypted, password) == message


def test_encryption_uses_different_random_values():
    message = "Same message"
    password = "StrongPassword123!"

    encrypted_one = encrypt_text(message, password)
    encrypted_two = encrypt_text(message, password)

    assert encrypted_one != encrypted_two
    assert decrypt_text(encrypted_one, password) == message
    assert decrypt_text(encrypted_two, password) == message


def test_wrong_password_fails():
    encrypted = encrypt_text("Secret message", "CorrectPassword123!")

    with pytest.raises(ValueError, match="incorrect password or modified"):
        decrypt_text(encrypted, "WrongPassword123!")


def test_modified_ciphertext_fails():
    encrypted = encrypt_text("Secret message", "StrongPassword123!")

    import base64
    import json

    envelope = json.loads(base64.b64decode(encrypted))
    ciphertext = bytearray(base64.b64decode(envelope["ciphertext"]))
    ciphertext[0] ^= 1
    envelope["ciphertext"] = base64.b64encode(ciphertext).decode("ascii")

    modified = base64.b64encode(
        json.dumps(envelope, separators=(",", ":")).encode("utf-8")
    ).decode("ascii")

    with pytest.raises(ValueError, match="incorrect password or modified"):
        decrypt_text(modified, "StrongPassword123!")


def test_empty_inputs_are_rejected():
    with pytest.raises(ValueError):
        encrypt_text("", "StrongPassword123!")

    with pytest.raises(ValueError):
        decrypt_text("", "StrongPassword123!")
