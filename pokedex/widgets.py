from django import forms
from django.utils.html import format_html
from .models import Card

class CardCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create_option(self, *args, **kwargs):
        option = super().create_option(*args, **kwargs)
        card = option['value']
        card_instance = Card.objects.get(pk=card)
        option['label'] = format_html(
            '<label for="{}" class="card-checkbox"><img src="{}" alt="{}" /> {}</label>',
            option['id'],
            card_instance.image_url,
            card_instance.name,
            card_instance.name
        )
        return option
