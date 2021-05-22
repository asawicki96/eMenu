from django.db import models

# Create your models here.

class Card(models.Model):
    """ Card to be used in a menu """

    name = models.CharField(verbose_name="Nazwa", max_length=255, unique=True, null=False, blank=False)
    slug = models.SlugField(max_length=255)
    description = models.TextField(verbose_name="Opis", null=False, blank=False)

    created_at = models.DateTimeField(verbose_name="Data utworzenia", auto_now_add=True)
    modified_at = models.DateTimeField(verbose_name="Data ostatniej modyfikacji", auto_now=True)

    class Meta:
        verbose_name = "Karta"
        verbose_name_plural = "Karty"
        ordering = ("name",)

    def __str__(self):
        return self.name