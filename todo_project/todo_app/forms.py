from django import forms
from .models import todos

class listform(forms.ModelForm):
    class Meta:
        model=todos
        fields=["title","description","finished","date"]
