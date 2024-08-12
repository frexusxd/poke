from django.db import models

class Card(models.Model):
    name = models.CharField(max_length=100)
    image_url = models.URLField(blank=True, null=True)
    type = models.CharField(max_length=50)
    hp = models.IntegerField()
    rarity = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name
