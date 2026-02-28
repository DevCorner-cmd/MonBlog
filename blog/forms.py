
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Article

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
            'class': 'input input-bordered w-full',
            'placeholder': 'Nom d’utilisateur'
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
    email = forms.EmailField(
        label="Votre adresse email",
        widget=forms.EmailInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Entrez votre adresse'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']

