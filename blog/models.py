from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.urls import reverse

"""
Article
- Titre
- Auteur
- Slug
- Description
- Resume description
- Image
- Date de creation
- Date de modification
- Publie -> Bool
- Ajout de vidéo
"""

class Article(models.Model):
    titre = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    views = models.PositiveIntegerField(default=0)
    description = models.TextField()
    resume_desc = models.TextField(blank=True)

    image = models.ImageField(upload_to='articles', blank=True, null=True)
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)

    publie = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modif = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.titre)
            slug = base_slug
            n = 1
            while Article.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:detail_article', kwargs={'slug': self.slug})




    def __str__(self):
        return self.titre
    

    """
    Compare uniquement la date (jour/mois/année)
    Donc les microsecondes ne posent plus problème.
    """
# Commentaires
class Commentaire(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="commentaires")
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)  # utilisateur connecté
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(
    "self",
    null=True,
    blank=True,
    related_name="reponses",
    on_delete=models.CASCADE
)  # réponses admin

    def __str__(self):
        return f"{self.auteur.username} sur {self.article.titre}"



# pour traccker les ip pour les vues

class ArticleView(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('article', 'ip_address')

    def __str__(self):
        return self.ip_address