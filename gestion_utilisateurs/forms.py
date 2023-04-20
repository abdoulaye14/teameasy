from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField



User = get_user_model()


class LoginForm(forms.Form):
    email    = forms.EmailField(label='Adresse email',widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class RegisterForm(forms.ModelForm):
    """
    The default 

    """
    societe = forms.ModelChoiceField(required=False,queryset=None, widget=forms.Select(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_2 = forms.CharField(label='Confirmer votre mot de passe', widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))

    class Meta:
        model = User
        fields = ['email']

    def clean_email(self):
        '''
        Verify email is available.
        '''
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Cet email existe déjà")
        return email

    def clean_password2(self, societe):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")

        if societe is None:
            raise forms.ValidationError("Vous ne pouvez pas ajouter d'utilisateur")
        if password is not None and password != password_2:
            raise forms.ValidationError("Vos mots de passe ne correspondent pas !")
        return cleaned_data
    
    def save(self, request, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        
        user.societe = request.user.societe
        self.clean_email()
        self.clean_password2(user.societe)
        # user.active = False # send confirmation email
        if commit:
            user.save()
        return user

class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['societe', 'email']

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "Vos mots de passe ne correspondent pas !")
        return cleaned_data

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['societe', 'email', 'password', 'active', 'staff', 'admin']

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]