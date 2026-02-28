from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'blog'  # obligatoire pour utiliser le namespace

urlpatterns = [
    path('', views.article_list, name='home'),
    path('detail/<slug:slug>/', views.detail_article, name='detail_article'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/add/', views.add_article, name='add'),
    path('dashboard/edit/<int:id>/', views.edit_article, name='edit'),
    path('dashboard/delete/<int:id>/', views.delete_article, name='delete'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('repondre/<int:comment_id>/', views.repondre_commentaire, name='repondre_commentaire'),

    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('signup/', views.signup, name='signup'),
    
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]

