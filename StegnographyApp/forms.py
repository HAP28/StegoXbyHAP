from django import forms

class HideDataForm(forms.Form):
    image = forms.ImageField()
    message = forms.CharField(widget=forms.Textarea)

class RevealDataForm(forms.Form):
    image = forms.ImageField()