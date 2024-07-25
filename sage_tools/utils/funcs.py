"""
Useful Functions
"""

import base64
import os
import secrets


def create_directories(base_dir: str, directories: list[tuple[str]]):
    """
    Creates a series of directories based on the input parameters.

    Args:
    - base_dir (str): The base directory in which the subdirectories will be created.
    - directories (list of tuples): A list of tuples where each tuple represents a
        subdirectory to create. The first element of each tuple is the name of the
        subdirectory, and the rest of the elements (if any) represent subdirectories
        within the previous directory.

    Example:
    base_dir = '/path/to/base'
    directories = [('logs',), ('logs', 'auth'), ('logs', 'core')]
    create_directories(base_dir, directories)

    This will create the following directories:
    - /path/to/base/logs
    - /path/to/base/logs/auth
    - /path/to/base/logs/core
    """
    for directory in directories:
        path = os.path.join(base_dir, *directory)
        if not os.path.exists(path):
            os.makedirs(path)


def generate_base32_secret(length: int = 20) -> str:
    """
    Generate a secure random Base32-encoded secret.

    Args:
        length (int): Length of the random bytes. Default is 20 bytes.

    Returns:
        str: A Base32-encoded string.
    """
    # Generate secure random bytes
    random_bytes = secrets.token_bytes(length)

    # Encode the bytes to Base32 and decode to a string for ease of use
    base32_secret = base64.b32encode(random_bytes).decode("utf-8")

    # Remove any Base32 padding characters ('=')
    return base32_secret.rstrip("=")


def hide_phone_number(phone_number):
    """
    Mask the phone number to only show the last four digits.

    Args:
        phone_number (str): The phone number to be masked.

    Returns:
        str: The masked phone number with only the last four digits visible.
    """
    if not phone_number:
        return "Phone number not available"

    # Ensure the phone number is in string format
    phone_number = str(phone_number)

    # Check if the phone number length is less than 4
    if len(phone_number) < 4:
        return "Invalid phone number"

    hidden_part = "*" * (
        len(phone_number) - 4
    )  # Replace all but the last 4 digits with asterisks
    visible_part = phone_number[-4:]  # Last 4 digits of the phone number

    return f"{hidden_part}{visible_part}"
