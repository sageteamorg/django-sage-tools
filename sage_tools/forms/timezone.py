from django import forms

try:
    import pytz
except ImportError:
    raise ImportError("Install `pytz` package. Run `pip install pytz`.")  # noqa: B904


class TimezoneForm(forms.Form):
    timezone = forms.ChoiceField(choices=[(tz, tz) for tz in pytz.all_timezones])
    next = forms.CharField(widget=forms.HiddenInput())
