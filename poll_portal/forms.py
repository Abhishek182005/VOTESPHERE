from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Poll


class CreatePollForm(ModelForm):
    class Meta:
        model = Poll
        fields = ['question', 'option_one', 'option_two', 'option_three']
        widgets = {
            'question': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Enter your poll question...'}),
            'option_one': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Option A'}),
            'option_two': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Option B'}),
            'option_three': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Option C'}),
        }


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['username', 'password1', 'password2']:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})
