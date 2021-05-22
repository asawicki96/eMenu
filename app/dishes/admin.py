from django.contrib import admin
from dishes import models

# Register your models here.

@admin.register(models.Dish)
class DishAdmin(admin.ModelAdmin):
    model = models.Dish
    prepopulated_fields = {"slug": ("name",)}