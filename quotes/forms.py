from django import forms

class AuthorForm(forms.Form):
    fullname = forms.CharField(max_length=50)
    born_date = forms.CharField(max_length=50)
    born_location = forms.CharField(max_length=150)
    description = forms.CharField(widget=forms.Textarea)

class QuoteForm(forms.Form):
    quote = forms.CharField(min_length=10, widget=forms.Textarea(attrs={'rows': 3}))

class TagForm(forms.Form):
    name = forms.CharField(min_length=3, max_length=25, required=True, widget=forms.TextInput())