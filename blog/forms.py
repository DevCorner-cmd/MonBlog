
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
                'class': 'textarea textarea-bordered w-full',
                'rows': 6,
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
            
            'placeholder': 'Example : Jean Paul'
        })
    )
    password1 = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Mot de passe'
        })
    )
    password2 = forms.CharField(
        label="Confirmer le mot de passe",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirmer le mot de passe'
        })
    )
    email = forms.EmailField(
        label="Votre adresse email",
        widget=forms.EmailInput(attrs={
            'placeholder': 'example@gmail.com'
        })
    )

     # Validation globale du formulaire
    def clean(self):
        cleaned_data = super().clean()
        pwd1 = cleaned_data.get("password1")
        pwd_confirm = cleaned_data.get("password2")

        email = cleaned_data.get('email')

        if email:
            try:
                # Vérifie le format de l'email
                validate_email(email)
            except ValidationError:
                # Ajoute une erreur au champ email
                self.add_error("Entrez une adresse mail correcte")

        if pwd1 and pwd_confirm and pwd1 != pwd_confirm:
            # Ajoute une erreur spécifique au champ pwd_confirm
            self.add_error("pwd_confirm", "Les mots de passe ne correspondent pas.")

        return cleaned_data
    

    def clean_pwd1(self):
        password = self.cleaned_data.get('password1')

        # Vérifie la longueur
        if len(password) < 8:
            raise ValidationError("Le mot de passe doit contenir au moins 8 caractères.")

        # Vérifie au moins un chiffre
        if not re.search(r"\d", password):
            raise ValidationError("Le mot de passe doit contenir au moins un chiffre.")

        # Vérifie au moins une lettre minuscule
        if not re.search(r"[a-z]", password):
            raise ValidationError("Le mot de passe doit contenir au moins une lettre minuscule.")

        # Vérifie au moins une lettre majuscule
        if not re.search(r"[A-Z]", password):
            raise ValidationError("Le mot de passe doit contenir au moins une lettre majuscule.")
        
        # verifie si le mdp existe
        if not User.objects.filter(password=password).exists():
            raise ValidationError("Mot de passe incorrect.")
        
        if User.objects.filter(password=password).exists():
            raise ValidationError("Ce mot de passe est déjà utilisé par un autre utilisateur. Veuillez en choisir un autre.")

        return password
    
    def clean_username(self):
        username = self.cleaned_data.get('username')

        if len(username) < 3:
            raise ValidationError("Le nom d'utilisateur doit contenir au moins 3 caractères.")

        return username

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']

