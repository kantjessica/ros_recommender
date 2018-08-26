from django import forms

class SearchForm(forms.Form):
    keywords = forms.CharField(label='Please give the keywords here:', max_length=100)
    types = forms.ChoiceField(choices=[('Package','Package'),('Repository','Repository'),('Both','Both')], label="Select a type", required=True)
    distribution = forms.ChoiceField(choices=[('All','All'),('groovy','groovy'),('hydro','hydro'),('indigo','indigo'),('jade','jade'),('kinetic','kinetic'),('lunar','lunar'),('melodic','melodic')], label="Select a distribution", required=True)
