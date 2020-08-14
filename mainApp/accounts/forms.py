from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model
)

User = get_user_model()

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Username or password is wrong')
            if not user.check_password(password):
                raise forms.ValidationError('Username or password is wrong')
            if not user.is_active:
                raise forms.ValidationError('Username or password is wrong')
        return super(UserLoginForm, self).clean(*args, **kwargs)

ROLES= [
    ('admin', 'Admin'),
    ('consultant', 'Consultant'),
    ('client', 'Client'),
    ]
class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.CharField(label='Role', widget=forms.Select(choices=ROLES))

    class Meta:
        model = User
        fields = [
            'username',
            'password'
        ]
