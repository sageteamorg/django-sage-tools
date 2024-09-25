from django.contrib.admin.widgets import AdminFileWidget


class SVGWidget(AdminFileWidget):
    def __init__(self, url=None, attrs=None):
        self.svg_field_url = url
        super().__init__(attrs)

    def format_value(self, value):
        """Return the file URL if available."""
        if self.svg_field_url:
            return self.svg_field_url
        return super().format_value(value)
