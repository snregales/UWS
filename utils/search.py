from django import forms
from django.views.generic import FormView


class SearchForm(forms.Form):
    search = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Search'})
    )


class SearchMixin(FormView):
    form_class = SearchForm
