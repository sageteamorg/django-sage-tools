from django.conf import settings
from sage_tools.decorators import AdminBypassDecorator

settings.configure(DJANGO_ADMIN_URL_PREFIX="admin")


def example_view(request, *args, **kwargs):
    return {"key": "value"}


decorated_view = AdminBypassDecorator(example_view)


class TestAdminBypassDecorator:
    """Test suite for the `AdminBypassDecorator` class."""

    def test_admin_request_bypasses_function_call(self, mock_request2):
        """Test that the function call is bypassed for admin requests.

        Parameters
        ----------
        mock_request2 : HttpRequest
            The mock request object used for testing.

        """
        mock_request2.path = "/admin/some_admin_page/"

        result = decorated_view(mock_request2)

        assert result == AdminBypassDecorator.EMPTY_CONTEXT

    def test_non_admin_request_calls_original_function(self, mock_request2):
        """Test that the original function is called for non-admin requests.

        Parameters
        ----------
        mock_request2 : HttpRequest
            The mock request object used for testing.

        """
        mock_request2.path = "/some_other_page/"

        result = decorated_view(mock_request2)

        assert result == {"key": "value"}

    def test_is_admin_request_true_for_admin_path(self, mock_request2):
        """Test that `is_admin_request` returns True for admin paths.

        Parameters
        ----------
        mock_request2 : HttpRequest
            The mock request object used for testing.

        """
        mock_request2.path = "/admin/some_admin_page/"
        assert AdminBypassDecorator.is_admin_request(mock_request2) is True

    def test_is_admin_request_false_for_non_admin_path(self, mock_request2):
        """Test that `is_admin_request` returns False for non-admin paths.

        Parameters
        ----------
        mock_request2 : HttpRequest
            The mock request object used for testing.

        """
        mock_request2.path = "/some_other_page/"
        assert AdminBypassDecorator.is_admin_request(mock_request2) is False
