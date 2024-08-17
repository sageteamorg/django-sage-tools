from django.test import override_settings
from sage_tools.context_processors.maintenance import get_maintenance_variables


class TestMaintenanceVariables:
    """Test suite for the `get_maintenance_variables` context processor."""

    @override_settings(UNDER_CONSTRUCTION_MODE=True, COMING_SOON_MODE=True)
    def test_get_maintenance_variables_enabled(self, mock_request):
        """Test `get_maintenance_variables` when both maintenance modes are
        enabled.

        Parameters
        ----------
        mock_request : HttpRequest
            The mock request object used for testing.

        """
        context = get_maintenance_variables(mock_request)
        assert context["is_maintenance_enabled"] is True
        assert context["is_coming_soon_enabled"] is True

    @override_settings(UNDER_CONSTRUCTION_MODE=False, COMING_SOON_MODE=False)
    def test_get_maintenance_variables_disabled(self, mock_request):
        """Test `get_maintenance_variables` when both maintenance modes are
        disabled.

        Parameters
        ----------
        mock_request : HttpRequest
            The mock request object used for testing.

        """
        context = get_maintenance_variables(mock_request)
        assert context["is_maintenance_enabled"] is False
        assert context["is_coming_soon_enabled"] is False

    @override_settings(UNDER_CONSTRUCTION_MODE=True, COMING_SOON_MODE=False)
    def test_get_maintenance_variables_partial(self, mock_request):
        """Test `get_maintenance_variables` when only `UNDER_CONSTRUCTION_MODE`
        is enabled.

        Parameters
        ----------
        mock_request : HttpRequest
            The mock request object used for testing.

        """
        context = get_maintenance_variables(mock_request)
        assert context["is_maintenance_enabled"] is True
        assert context["is_coming_soon_enabled"] is False
