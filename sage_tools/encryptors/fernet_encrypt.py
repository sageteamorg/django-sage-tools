from .base import Encryptor

try:
    from cryptography.fernet import Fernet
except ImportError:
    raise ImportError("Install `cryptography` package. Run `pip install cryptography`.")


class FernetEncryptor(Encryptor):
    """Fernet encryption class.

    This class uses the Fernet symmetric encryption method provided by the `cryptography` package to encrypt and decrypt data.

    Parameters
    ----------
    secret_key : str
        The secret key used for encryption and decryption. Must be a URL-safe base64-encoded 32-byte key.

    Methods
    -------
    encrypt(data: str) -> str
        Encrypts the given data using Fernet encryption.
    decrypt(data: str) -> str
        Decrypts the given data using Fernet encryption.

    Examples
    --------
    >>> secret_key = Fernet.generate_key()
    >>> encryptor = FernetEncryptor(secret_key)
    >>> encrypted_data = encryptor.encrypt("Hello, World!")
    >>> decrypted_data = encryptor.decrypt(encrypted_data)
    >>> decrypted_data
    'Hello, World!'

    """

    def __init__(self, secret_key: str):
        self.fernet = Fernet(secret_key)

    def encrypt(self, data: str) -> str:
        """Encrypts the given data using Fernet encryption.

        Parameters
        ----------
        data : str
            The data to be encrypted.

        Returns
        -------
        str
            The encrypted data.

        """
        self._validate_data(data)
        data = self._encode_data(data)
        encrypted_value = self.fernet.encrypt(data)
        return encrypted_value.decode("utf-8")

    def decrypt(self, data: str) -> str:
        """Decrypts the given data using Fernet encryption.

        Parameters
        ----------
        data : str
            The data to be decrypted.

        Returns
        -------
        str
            The decrypted data.

        """
        self._validate_data(data)
        data = self._encode_data(data)
        return self.fernet.decrypt(data).decode("utf-8")

    def _validate_data(self, data):
        """Validates the data to ensure it is either a string or bytes.

        Parameters
        ----------
        data : str or bytes
            The data to be validated.

        Raises
        ------
        TypeError
            If the data is not a string or bytes.

        """
        if not isinstance(data, (str, bytes)):
            raise TypeError(
                "FernetEncryptor only supports string or bytes data types for encryption."
            )

    def _encode_data(self, data):
        """Encodes the data to bytes if it is a string.

        Parameters
        ----------
        data : str or bytes
            The data to be encoded.

        Returns
        -------
        bytes
            The encoded data.

        """
        if isinstance(data, str):
            data = data.encode("utf-8")
        return data
