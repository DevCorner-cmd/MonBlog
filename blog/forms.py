from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Article
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ['titre', 'resume_desc', 'description', 'image', 'publie']

        widgets = {
            'titre': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Entrez le titre'
            }),

            'resume_desc': forms.Textarea(attrs={
                'class': 'textarea textarea-bordered w-full',
                'rows': 3,
                'placeholder': 'Petit résumé...'
            }),

            'description': forms.Textarea(attrs={
                'class': 'textarea textarea-bordered w-full h-40',
                'placeholder': 'Contenu complet de l’article'
            }),

            'image': forms.ClearableFileInput(attrs={
                'class': 'file-input file-input-bordered w-full'
            }),

            'publie': forms.CheckboxInput(attrs={
                'class': 'toggle toggle-primary'
            }),
        }


class CustomUserCreationForm(UserCreationForm):

    username = forms.CharField(
        label="Nom d'utilisateur",
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Exemple : JeanPaul'
        })
    )

    email = forms.EmailField(
        label="Adresse email",
        widget=forms.EmailInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'example@gmail.com'
        })
    )

    password1 = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Mot de passe'
        })
    )

    password2 = forms.CharField(
        label="Confirmer le mot de passe",
        widget=forms.PasswordInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Confirmer le mot de passe'
        })
    )

    def clean(self):
        cleaned_data = super().clean()

        pwd1 = cleaned_data.get("password1")
        pwd2 = cleaned_data.get("password2")
        email = cleaned_data.get("email")

        if email:
            try:
                validate_email(email)
            except ValidationError:
                self.add_error("email", "Entrez une adresse email valide.")

        if pwd1 and pwd2 and pwd1 != pwd2:
            self.add_error("password2", "Les mots de passe ne correspondent pas.")

        return cleaned_data


    def clean_password1(self):
        password = self.cleaned_data.get('password1')

        if len(password) < 8:
            raise ValidationError("Le mot de passe doit contenir au moins 8 caractères.")

        if not re.search(r"\d", password):
            raise ValidationError("Le mot de passe doit contenir au moins un chiffre.")

        if not re.search(r"[a-z]", password):
            raise ValidationError("Le mot de passe doit contenir au moins une lettre minuscule.")

        if not re.search(r"[A-Z]", password):
            raise ValidationError("Le mot de passe doit contenir au moins une lettre majuscule.")

        return password


    def clean_username(self):
        username = self.cleaned_data.get('username')

        if len(username) < 3:
            raise ValidationError("Le nom d'utilisateur doit contenir au moins 3 caractères.")

        return username


    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']