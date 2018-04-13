from .models import Author, Language, Genre
from django.core.exceptions import ValidationError
from django import forms
from django.utils.translation import ugettext_lazy as _
import datetime


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        # Check data is in range librarian allowed to change(+4 week)
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        return data


class AddBookForm(forms.Form):
    title = forms.CharField(max_length=200)
    author = forms.ModelChoiceField(queryset=Author.objects.all())
    summary = forms.CharField(max_length=1000, required=False)
    isbn = forms.CharField(min_length=13, max_length=13)
    language = forms.ModelChoiceField(queryset=Language.objects.all())
    genre = forms.ModelMultipleChoiceField(queryset=Genre.objects.all(), required=False)
