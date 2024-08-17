import pytest
from django.http import HttpRequest
from unittest.mock import Mock
from cryptography.fernet import Fernet

from sage_tools.repository.generator import BaseDataGenerator
from sage_tools.encryptors import FernetEncryptor, DummyEncryptor
from sage_tools.services.slug import SlugService


@pytest.fixture
def mock_request():
    return HttpRequest()


@pytest.fixture
def mock_request2():
    return Mock(spec=HttpRequest)


@pytest.fixture
def secret_key():
    return Fernet.generate_key()


@pytest.fixture
def fernet_encryptor(secret_key):
    return FernetEncryptor(secret_key)


@pytest.fixture
def dummy_encryptor():
    return DummyEncryptor()


@pytest.fixture
def generator():
    return BaseDataGenerator(locale="en")


@pytest.fixture
def mock_instance():
    instance = Mock()
    instance.title = "Test Title"
    instance.slug = "existing-slug"
    instance.pk = 1
    return instance


@pytest.fixture
def slug_service(mock_instance):
    return SlugService(mock_instance)
