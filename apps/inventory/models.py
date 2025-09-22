from django.db import models


class InventoryItem(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()

    def __str__(self) -> str:
        return self.name
