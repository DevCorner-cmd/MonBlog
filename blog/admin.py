from django.contrib import admin
from .models import Article, Commentaire, ArticleView


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        'titre',
        'auteur',
        'publie',
        'date_creation',
        'views',
    )

    list_filter = (
        'publie',
        'date_creation',
        'auteur',
    )

    search_fields = (
        'titre',
        'description',
        'resume_desc',
    )

    prepopulated_fields = {
        'slug': ('titre',)
    }

    ordering = ('-date_creation',)

    fieldsets = (
        ('Contenu', {
            'fields': ('titre', 'slug', 'description', 'resume_desc', 'image', 'views')
        }),
        ('Publication', {
            'fields': ('auteur', 'publie')
        }),
        ('Dates', {
            'fields': ('date_creation', 'date_modif')
        }),
    )

    readonly_fields = ('date_creation', 'date_modif')


admin.site.site_header = "Administration MonBlog"
admin.site.site_title = "MonBlog Admin"
admin.site.index_title = "Gestion du contenu"


@admin.register(Commentaire)
class CommentaireAdmin(admin.ModelAdmin):
    list_display = (
        'article',
        'auteur',
        'contenu',
        'date_creation',
        'parent'
    )

    list_filter = (
        'parent',
        'date_creation',
        'auteur',
    )

    search_fields = (
        'article',
        'contenu',
    )


    ordering = ('-date_creation',)

    fieldsets = (
        ('Contenu', {
            'fields': ('article', 'contenu')
        }),
        ('Publication', {
            'fields': ('auteur',)
        }),
        ('Dates', {
            'fields': ('date_creation',)
        }),
    )

    readonly_fields = ('date_creation', 'parent')



@admin.register(ArticleView)
class ArticleViewAdmin(admin.ModelAdmin):
    list_display = (
        'article',
        'ip_address',
        'viewed_at',
    )

    list_filter = (
        'viewed_at',
    )

    search_fields = (
        'ip_address',
        'article__titre',
    )

    ordering = ('-viewed_at',)