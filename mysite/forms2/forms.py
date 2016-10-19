from django import forms 

class NameForm(forms.Form):
	input_form = forms.CharField(label="Enter Query")