from django import forms
from .models import Deck, Card

class DeckForm(forms.ModelForm):
    class Meta:
        model = Deck
        fields = ['name', 'cards']
        widgets = {
            'cards': forms.CheckboxSelectMultiple(),
        }

class CardChoiceForm(forms.Form):
    cards = forms.ModelMultipleChoiceField(
        queryset=Card.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
