import logging
from datetime import timedelta
from typing import Any, Optional

from django.conf import settings
from django.http import HttpRequest
from django.utils import timezone

try:
    from cryptography.fernet import InvalidToken
except ImportError:
    raise ImportError("Install `cryptography` package. Run `pip install cryptography`.")

from sage_tools.encryptors import FernetEncryptor

logger = logging.getLogger(__name__)


class SessionHandler:
    """
    Manages session variables with encryption and a custom expiry time for enhanced security and privacy.

    This class provides methods to set, get, and delete session variables securely. It uses
    Fernet symmetric encryption to ensure that session data is encrypted before being stored,
    offering an additional layer of security. Each session variable can have its own lifespan,
    after which it is considered expired and automatically removed.
    """

    def __init__(self, request: HttpRequest) -> None:
        """
        Initializes the SessionHandler with the current request and uses the secret key from Django settings for encryption.
        """
        self.request = request
        self.fernet = FernetEncryptor(settings.FERNET_SECRET_KEY)

    def set(
        self, key: str, value: str, lifespan=timedelta(minutes=10), encrypt=True
    ) -> None:
        """
        Encrypts and sets a session variable with a specified lifespan.
        """
        if not isinstance(key, str) or not key:
            raise ValueError("Key must be a non-empty string")
        if not isinstance(lifespan, timedelta) or lifespan.total_seconds() <= 0:
            raise ValueError("Lifespan must be a positive timedelta object")

        try:
            encrypted_value = (
                self.fernet.encrypt(value.encode("utf-8")) if encrypt else value
            )
            self.request.session[key] = {
                "value": encrypted_value,
                "created_at": timezone.now().timestamp(),
                "lifespan": lifespan.total_seconds(),
            }
        except Exception as e:
            logger.error(f"Error encrypting session data for key {key}: {str(e)}")

    def get(self, key: str, decrypt=True) -> Optional[str]:
        """
        Retrieves, decrypts, and returns the value of a session variable if it has not expired.
        """
        session_info = self.request.session.get(key)
        if session_info and self._is_valid_session_data(session_info):
            created_at = session_info.get("created_at")
            expiry = session_info.get("lifespan", 0)
            if timezone.now().timestamp() - created_at < expiry:
                encrypted_value = session_info.get("value")
                try:
                    return (
                        self.fernet.decrypt(encrypted_value)
                        if decrypt
                        else encrypted_value
                    )
                except InvalidToken:
                    logger.error(
                        f"Invalid token for session key {key}. Possible data tampering."
                    )
            else:
                self.delete(key)
        return None

    def delete(self, key: str) -> Optional[Any]:
        """
        Deletes a session variable, if it exists.
        """
        return self.request.session.pop(key, None)

    def is_expired(self, key: str) -> bool:
        """
        Checks if a session variable has expired.
        """
        session_info = self.request.session.get(key)
        if session_info and self._is_valid_session_data(session_info):
            created_at = session_info.get("created_at")
            lifespan = session_info.get("lifespan", 0)
            return timezone.now().timestamp() - created_at >= lifespan
        return True

    def refresh(self, key: str, lifespan=timedelta(minutes=10)) -> bool:
        """
        Refreshes the lifespan of an existing session variable, if it exists and has not expired.
        """
        if not self.is_expired(key):
            session_info = self.request.session.get(key)
            if session_info:
                session_info["created_at"] = timezone.now().timestamp()
                session_info["lifespan"] = lifespan.total_seconds()
                self.request.session[key] = session_info
                return True
        return False

    def exists(self, key: str) -> bool:
        """
        Checks if a session variable exists and has not expired.
        """
        return key in self.request.session and not self.is_expired(key)

    def _is_valid_session_data(self, session_data: dict[str, Any]) -> bool:
        """
        Validates the structure of the session data.
        """
        return all(k in session_data for k in ["value", "created_at", "lifespan"])

    def flush(self) -> None:
        """
        Clears the session data and regenerates a new session key.
        """
        self.request.session.flush()

    def cycle_key(self) -> None:
        """
        Preserves the session data but changes the session key to prevent session fixation.
        """
        self.request.session.cycle_key()
