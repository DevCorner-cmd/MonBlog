from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Article, Commentaire, ArticleView
from .forms import ArticleForm
from django.db.models import Sum, Count
from django.db.models.functions import TruncDate



# Vérifie si l'utilisateur est admin
def is_owner(user):
    return user.is_superuser



def article_list(request):
    articles = Article.objects.filter(publie=True)

    # Si un utilisateur envoie un commentaire
    if request.method == "POST":
        if request.user.is_authenticated and not request.user.is_superuser:
            contenu = request.POST.get("contenu")
            article_id = request.POST.get("article_id")

            if contenu and article_id:
                article = get_object_or_404(Article, id=article_id)

                Commentaire.objects.create(
                    article=article,
                    auteur=request.user,
                    contenu=contenu
                )

        return redirect('blog:home')

    return render(request, 'blog/home.html', {
        'articles': articles
    })


def get_client_ip(request):
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded:
        return x_forwarded.split(',')[0]
    return request.META.get('REMOTE_ADDR')


from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Prefetch
from .models import Article, Commentaire, ArticleView

def detail_article(request, slug):
    article = get_object_or_404(
        Article.objects.prefetch_related(
            "commentaires__reponses",
            "commentaires__auteur",
            "commentaires__reponses__auteur"
        ),
        slug=slug,
        publie=True
    )

    # ----------- COMPTEUR DE VUES -----------
    ip = get_client_ip(request)
    session_key = f"viewed_{article.id}"

    if request.user != article.auteur:

        already_viewed_session = request.session.get(session_key)
        already_viewed_ip = ArticleView.objects.filter(
            article=article,
            ip_address=ip
        ).exists()

        if not already_viewed_session and not already_viewed_ip:
            ArticleView.objects.create(
                article=article,
                ip_address=ip
            )

            article.views += 1
            article.save(update_fields=['views'])

            request.session[session_key] = True

    # ----------- COMMENTAIRES / RÉPONSES -----------
    if request.method == "POST" and request.user.is_authenticated:
        contenu = request.POST.get("contenu")
        parent_id = request.POST.get("parent_id")

        if contenu:
            parent = None
            if parent_id:
                try:
                    parent = Commentaire.objects.get(id=parent_id)
                except Commentaire.DoesNotExist:
                    parent = None

            Commentaire.objects.create(
                article=article,
                auteur=request.user,
                contenu=contenu,
                parent=parent
            )

            return redirect("blog:detail_article", slug=article.slug)

    date1 = article.date_creation.strftime("%d/%m/%Y")
    date2 = article.date_modif.strftime("%d/%m/%Y")

    return render(request, 'blog/detail.html', {
        'article': article,
        'date1': date1,
        'date2': date2
    })



@login_required
def dashboard(request):
    articles = Article.objects.filter(auteur=request.user)

    total_views = articles.aggregate(
        total= Sum('views')
    )['total'] or 0

    top_articles = articles.order_by('-views')[:5]

    views_per_day = (
        ArticleView.objects
        .filter(article__auteur=request.user)
        .annotate(date=TruncDate('viewed_at'))
        .values('date')
        .annotate(count=Count('id'))
        .order_by('-date')
    )

    return render(request, 'blog/dashboard.html', {
        'articles': articles,
        'total_views': total_views,
        'top_articles': top_articles,
        'views_per_day': views_per_day
    })



# ajout

@login_required
def add_article(request):
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)  # on ne sauvegarde pas encore
            article.auteur = request.user      # on assigne l’utilisateur connecté
            article.save()                     # maintenant on sauvegarde
            return redirect('blog:dashboard')
    else:
        form = ArticleForm()

    return render(request, 'blog/add_article.html', {'form': form})




# modifier
@login_required
def edit_article(request, id):
    article = get_object_or_404(Article, id = id)
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('blog:dashboard')
    else:
        form = ArticleForm(instance=article)

    return render(request, 'blog/article_form.html', {'form': form, 'article': article})


# suppression
@login_required
def delete_article(request, id):
    article = get_object_or_404(Article, id=id, auteur=request.user)
    if request.method == 'POST':
        article.delete()
        return redirect('blog:dashboard')
    return render(request, 'blog/confirm_delete.html', {'article': article})


# Home : affiche articles et commentaires, formulaire de commentaire inclus
def home(request):
    articles = Article.objects.all().order_by('-date_creation')
    top_articles = Article.objects.filter(publie=True).order_by('-views')[:3]

    if request.method == "POST" and request.user.is_authenticated and not request.user.is_superuser:
        contenu = request.POST.get("contenu")
        article_id = request.POST.get("article_id")
        article = Article.objects.get(id=article_id)
        if contenu:
            Commentaire.objects.create(
                article=article,
                auteur=request.user,
                contenu=contenu
            )
        return redirect('blog:home')

    context = {
        "articles": articles,
        'top_articles': top_articles,
    }
    return render(request, 'blog/home.html', context)

# Admin répond à un commentaire
@login_required
@user_passes_test(is_owner)
def repondre_commentaire(request, comment_id):
    commentaire = Commentaire.objects.get(id=comment_id)
    if request.method == "POST":
        contenu = request.POST.get("contenu")
        if contenu:
            Commentaire.objects.create(
                article=commentaire.article,
                auteur=request.user,
                contenu=contenu,
                parent=commentaire
            )
    return redirect('blog:home')

from .forms import CustomUserCreationForm

def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog:login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})


# track d'ip

def get_client_ip(request):
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded:
        return x_forwarded.split(',')[0]
    return request.META.get('REMOTE_ADDR')



