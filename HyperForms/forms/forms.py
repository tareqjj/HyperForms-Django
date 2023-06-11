from django import forms


class RegistrationForm(forms.Form):
    name = forms.CharField(label="your name")
    age = forms.IntegerField(label="your age")
    favorite_book = forms.CharField(label="your favorite book")
