from abc import ABC, abstractmethod


class Encryptor(ABC):
    """Abstract base class for encryption.

    This class defines the interface for encryption and decryption.

    Methods
    -------
    encrypt(data: str) -> str
        Encrypts the given data.
    decrypt(data: str) -> str
        Decrypts the given data.

    """

    @abstractmethod
    def encrypt(self, data: str) -> str:
        """Encrypts the given data.

        Parameters
        ----------
        data : str
            The data to be encrypted.

        Returns
        -------
        str
            The encrypted data.

        """
        pass

    @abstractmethod
    def decrypt(self, data: str) -> str:
        """Decrypts the given data.

        Parameters
        ----------
        data : str
            The data to be decrypted.

        Returns
        -------
        str
            The decrypted data.

        """
        pass
