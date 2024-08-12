import requests
from .models import Card

def load_cards_from_api():
    url = 'https://api.pokemontcg.io/v2/cards'
    response = requests.get(url)
    data = response.json()

    for card_data in data['data']:
        card, created = Card.objects.get_or_create(
            id=card_data['id'],
            defaults={
                'name': card_data.get('name', ''),
                'type': card_data.get('type', ''),
                'description': card_data.get('description', ''),
            }
        )
