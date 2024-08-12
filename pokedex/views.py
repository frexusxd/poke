from django.shortcuts import render, redirect, get_object_or_404
from .forms import DeckForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login, logout
from .models import Deck, Card
import requests
from django.core.paginator import Paginator
from django.contrib import messages

@login_required
def create_deck(request):
    search_query = request.GET.get('search', '')
    cards = Card.objects.all().order_by('name')

    if search_query:
        cards = cards.filter(name__icontains=search_query)

    paginator = Paginator(cards, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST':
        deck_name = request.POST.get('deck_name')
        selected_cards_ids = request.POST.getlist('cards')

        if deck_name and selected_cards_ids:
            deck = Deck.objects.create(name=deck_name, user=request.user)
            selected_cards = Card.objects.filter(id__in=selected_cards_ids)
            deck.cards.set(selected_cards)
            deck.save()

            messages.success(request, 'wow goodjob')
            return redirect('profile')
        else:
            messages.error(request, 'error')

    return render(request, 'pokedex/create_deck.html', {
        'page_obj': page_obj,
        'search_query': search_query,
    })

def home(request):
    return render(request, 'pokedex/home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def view_deck(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id)
    return render(request, 'view_deck.html', {'deck': deck})

@login_required
def delete_deck(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id)

    if request.method == 'POST':
        deck.delete()
        return redirect('profile')

    return render(request, 'delete_deck.html', {'deck': deck})

def fetch_cards_from_api():
    response = requests.get('https://api.pokemontcg.io/v2/cards/xy1-1')
    if response.status_code == 200:
        return response.json()
    return []

def update_cards():
    cards_data = fetch_cards_from_api()
    for card_data in cards_data:
        Card.objects.update_or_create(
            id=card_data['id'],
            defaults={
                'name': card_data['name'],
            }
        )

def card_list(request):
    cards = Card.objects.all()
    return render(request, 'card_list.html', {'cards': cards})

@login_required
def profile_view(request):
    user = request.user
    decks = Deck.objects.filter(user=user)
    return render(request, 'registration/profile.html', {
        'decks': decks,
    })

@login_required
def profile(request):
    decks = Deck.objects.filter(user=request.user)
    return render(request, 'registration/profile.html', {'decks': decks})

@login_required
def edit_deck(request, pk):
    cards = Card.objects.all().order_by('name')
    paginator = Paginator(cards, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST':
        form = DeckForm(request.POST)
        if form.is_valid():
            deck = form.save(commit=False)
            deck.user = request.user
            deck.save()

            selected_cards = request.POST.getlist('cards')
            deck.cards.set(selected_cards)
            deck.save()
            return redirect('success')
    else:
        form = DeckForm()

    return render(request, 'pokedex/create_deck.html', {
        'form': form,
        'page_obj': page_obj,
    })

def deck_list(request):
    decks = Deck.objects.all()
    return render(request, 'pokedex/deck_list.html', {'decks': decks})

def custom_logout(request):
    logout(request)
    return redirect('/')
