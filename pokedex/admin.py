from django.contrib import admin
from .models import Deck, DeckCard, Card

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'hp', 'rarity')
    search_fields = ('name', 'type')

@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    search_fields = ('name',)

    def save_model(self, request, obj, form, change):
        obj.clean()
        super().save_model(request, obj, form, change)

@admin.register(DeckCard)
class DeckCardAdmin(admin.ModelAdmin):
    list_display = ('deck', 'card')
    search_fields = ('deck__name', 'card__name')
