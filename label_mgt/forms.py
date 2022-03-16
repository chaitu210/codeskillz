from django import forms
from django.contrib.auth import authenticate


class AuthenticationForm(forms.Form):
    username = forms.CharField(max_length=254)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password)

            if self.user_cache is None:
                raise forms.ValidationError(
                    "Invalid Details. Please check the EmailID-Password combination.")
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):

        if not user.is_active:
            raise forms.ValidationError("This account is inactive.")

    def get_user(self):
        return self.user_cache
