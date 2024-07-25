from .base import Encryptor


class DummyEncryptor(Encryptor):
    """
    Dummy encryption class for testing.

    This class implements the Encryptor interface but performs no actual encryption or decryption.

    Methods
    -------
    encrypt(data: str) -> str
        Returns the data unchanged.
    decrypt(data: str) -> str
        Returns the data unchanged.

    Examples
    --------
    >>> encryptor = DummyEncryptor()
    >>> encrypted_data = encryptor.encrypt("Hello, World!")
    >>> encrypted_data
    'Hello, World!'
    >>> decryptor = encryptor.decrypt(encrypted_data)
    >>> decryptor
    'Hello, World!'
    """

    def encrypt(self, data: str) -> str:
        return data

    def decrypt(self, data: str) -> str:
        return data
