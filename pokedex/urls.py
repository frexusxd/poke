from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import delete_deck, deck_list


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('create_deck/', views.create_deck, name='create_deck'),
    path('deck/<int:deck_id>/', views.view_deck, name='view_deck'),
    path('deck/<int:deck_id>/delete/', views.delete_deck, name='delete_deck'),
    path('cards/', views.card_list, name='card_list'),
    path('accounts/profile/', views.profile_view, name='profile'),
    path('logout/', views.custom_logout, name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
    path('deck/<int:pk>/edit/', views.edit_deck, name='edit_deck'),
    path('deck/<int:deck_id>/delete/', views.delete_deck, name='delete_deck'),
    path('decks/', deck_list, name='deck_list'),
    path('profile/', views.profile, name='profile'),
]
