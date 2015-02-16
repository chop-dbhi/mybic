from django import forms
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

class FixtureForm(forms.Form):
    fixture = forms.CharField(max_length=300)

    def clean(self):
        validate = URLValidator()
        try:
            validate(self.cleaned_data.get('fixture'))
        except ValidationError, e:
            print e
        return self.cleaned_data