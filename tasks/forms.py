from django.forms import ModelForm
from .models import Task
from django import forms

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title of the task'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'write a description...'}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }