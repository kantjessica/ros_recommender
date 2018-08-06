from django import forms

class SearchForm(forms.Form):
    keywords = forms.CharField(label='Please give the keywords here:', max_length=100)