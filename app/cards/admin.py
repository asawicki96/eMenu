from django.contrib import admin
from cards import models


@admin.register(models.Card)
class CardAdmin(admin.ModelAdmin):
    model = models.Card
    prepopulated_fields = {"slug": ("name",)}
