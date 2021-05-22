from django.db import models

# Create your models here.

class Dish(models.Model):
    """ Dish to be used in menu card """ 

    name = models.CharField(verbose_name="Nazwa", max_length=255, unique=True)
    slug = models.SlugField(max_length=255)

    card = models.ForeignKey(verbose_name="Karta", to="cards.Card", 
                             related_name="dishes", on_delete=models.SET_NULL, 
                             null=True, blank=True)

    description = models.TextField(verbose_name="Opis")
    price = models.DecimalField(verbose_name="Cena", max_digits=6, decimal_places=2)
    preparation_time = models.DurationField(verbose_name="Czas przygotowania")
    is_vege = models.BooleanField(verbose_name="Wegetariańskie", default=False)

    created_at = models.DateTimeField(verbose_name="Data utworzenia", auto_now_add=True)
    modified_at = models.DateTimeField(verbose_name="Data ostatniej modyfikacji", auto_now=True)

    class Meta:
        verbose_name = "Danie"
        verbose_name_plural = "Dania"
        ordering = ("name",)

    def __str__(self):
        return self.name
