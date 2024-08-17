import pytest
from cryptography.fernet import InvalidToken


class TestEncryptors:
    """Test suite for the `FernetEncryptor` and `DummyEncryptor` classes."""

    def test_fernet_encryptor_encrypt(self, fernet_encryptor):
        """Test that `FernetEncryptor` correctly encrypts data.

        Parameters
        ----------
        fernet_encryptor : FernetEncryptor
            The FernetEncryptor instance used for testing.

        """
        data = "Hello, World!"
        encrypted_data = fernet_encryptor.encrypt(data)
        assert isinstance(encrypted_data, str)
        assert encrypted_data != data  # Ensure the data is actually encrypted

    def test_fernet_encryptor_decrypt(self, fernet_encryptor):
        """Test that `FernetEncryptor` correctly decrypts data.

        Parameters
        ----------
        fernet_encryptor : FernetEncryptor
            The FernetEncryptor instance used for testing.

        """
        data = "Hello, World!"
        encrypted_data = fernet_encryptor.encrypt(data)
        decrypted_data = fernet_encryptor.decrypt(encrypted_data)
        assert decrypted_data == data

    def test_fernet_encryptor_invalid_decrypt(self, fernet_encryptor):
        """Test that `FernetEncryptor` raises an `InvalidToken` exception when
        decrypting invalid data.

        Parameters
        ----------
        fernet_encryptor : FernetEncryptor
            The FernetEncryptor instance used for testing.

        """
        with pytest.raises(InvalidToken):
            fernet_encryptor.decrypt("invalid_encrypted_data")

    def test_dummy_encryptor_encrypt(self, dummy_encryptor):
        """Test that `DummyEncryptor` returns the data unchanged when
        "encrypting".

        Parameters
        ----------
        dummy_encryptor : DummyEncryptor
            The DummyEncryptor instance used for testing.

        """
        data = "Hello, World!"
        encrypted_data = dummy_encryptor.encrypt(data)
        assert encrypted_data == data

    def test_dummy_encryptor_decrypt(self, dummy_encryptor):
        """Test that `DummyEncryptor` returns the data unchanged when
        "decrypting".

        Parameters
        ----------
        dummy_encryptor : DummyEncryptor
            The DummyEncryptor instance used for testing.

        """
        data = "Hello, World!"
        decrypted_data = dummy_encryptor.decrypt(data)
        assert decrypted_data == data

    def test_fernet_encryptor_invalid_data_type(self, fernet_encryptor):
        """Test that `FernetEncryptor` raises a `TypeError` when given invalid
        data types.

        Parameters
        ----------
        fernet_encryptor : FernetEncryptor
            The FernetEncryptor instance used for testing.

        """
        with pytest.raises(TypeError):
            fernet_encryptor.encrypt(12345)  # Pass an invalid data type
