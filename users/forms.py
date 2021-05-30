from django import forms
from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.models import User
from .models import User

class SignUpForm(UserCreationForm):
    #project = forms.CharField(max_length=30, required=False, help_text='Optional.')
    #last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    # project = forms.fields.ChoiceField(
    #     choices = (
    #         ('0', 'none'),
    #         ('1', 'pj_1'),
    #         ('2', 'pj_2'),
    #         ('3', 'pj_3'),
    #         ('4', 'pj_4')
    #     ),
    #     required=True,
    #     widget=forms.widgets.Select
    # )
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', )