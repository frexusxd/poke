from django.db import models
from django.contrib.auth.models import User

class Card(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    image_url = models.URLField(blank=True, null=True)
    type = models.CharField(max_length=50, blank=True)
    hp = models.CharField(max_length=10, blank=True)
    rarity = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Deck(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cards = models.ManyToManyField(Card, related_name='decks')

    def __str__(self):
        return self.name

class DeckCard(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('deck', 'card')

    def __str__(self):
        return f'{self.card.name} (x{self.quantity}) in {self.deck.name}'
