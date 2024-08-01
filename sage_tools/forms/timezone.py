from django import forms

try:
    import pytz
except ImportError:
    raise ImportError(  # noqa: B904
        "Install `pytz` package. Run `pip install pytz`."
    )

class TimezoneForm(forms.Form):
    timezone = forms.ChoiceField(choices=[(tz, tz) for tz in pytz.all_timezones])
    next = forms.CharField(widget=forms.HiddenInput())
