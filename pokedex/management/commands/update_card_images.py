import requests
import time
from django.core.management.base import BaseCommand
from pokedex.models import Card

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        api_url = 'https://api.pokemontcg.io/v2/cards'
        headers = {'X-Api-Key': 'free ez '}

        page_size = 100
        page = 1

        while True:
            url = f"{api_url}?pageSize={page_size}&page={page}"
            self.stdout.write(self.style.SUCCESS(f'Fetching card data from API: {url}'))

            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                data = response.json()

                cards_data = data.get('data', [])
                if not cards_data:
                    self.stdout.write(self.style.SUCCESS('No more data found.'))
                    break

                for card_data in cards_data:
                    card_id = card_data.get('id')
                    card, created = Card.objects.update_or_create(
                        id=card_id,
                        defaults={
                            'name': card_data.get('name', ''),
                            'type': ', '.join(card_data.get('types', [])),
                            'hp': card_data.get('hp', ''),
                            'rarity': card_data.get('rarity', ''),
                            'description': card_data.get('text', ''),
                            'image_url': card_data.get('images', {}).get('large', '')
                        }
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'created new card: {card.name}'))
                    else:
                        self.stdout.write(self.style.SUCCESS(f'updated data for card: {card.name}'))

            except requests.RequestException as e:
                self.stdout.write(self.style.ERROR(f'error: {e}'))

            time.sleep(1)

            page += 1
