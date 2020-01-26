from django import forms
from .models import MyUser
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def forbidden_names_validator(value):
    forbidden_names = {'admin', 'user', 'login', 'logout', 'superuser',
                       'authentication', 'form', 'model', 'tests', 'urls',
                       }
    if value.lower() in forbidden_names:
        message = _('This is an in forbidden username')
        raise ValidationError(message)


def invalid_names_validator(value):
    if '@' in value or '&' in value or '$' in value:
        message = _('You input an invalid username')
        raise ValidationError(message)


def unique_names_validator(value):
    if MyUser.objects.filter(username__iexact=value):
        message = _('The username already exists!')
        raise ValidationError(message)


def unique_emails_validator(value):
    if MyUser.objects.filter(email__iexact=value):
        message = _('The email already exists!')
        raise ValidationError(message)


class UserCreationForm(forms.ModelForm):
    username = forms.CharField(label=_('Username'), widget=forms.TextInput(attrs={'class': 'form-control'}),
                               max_length=30, required=True,
                               help_text=_("Username may contain numbers, uppercase or lowercase"))
    email = forms.EmailField(label=_('Email'), widget=forms.EmailInput(attrs={'class': 'form-control'}),
                             required=True, max_length=30)
    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                required=True, max_length=16,
                                help_text=_("Password should be at least 8 bits and no more than 16 bits"))
    password2 = forms.CharField(label=_('Confirm Password'),
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True,
                                max_length=16, help_text=_("Please input your password again"))

    class Meta:
        model = MyUser
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].validators += [forbidden_names_validator, invalid_names_validator,
                                               unique_names_validator, ]
        self.fields['email'].validators += [unique_emails_validator, ]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 == password2:
            return password2
        else:
            raise forms.ValidationError(_('The two passwords do not match!'))

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data.get("password1"))
        if commit:
            user.save()
        return user
