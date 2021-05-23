from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.utils.text import slugify
import logging

logger = logging.getLogger(__name__)

# Create your models here.

class Dish(models.Model):
    """ Dish to be used in menu card """ 

    name = models.CharField(verbose_name="Nazwa", max_length=255, unique=True)
    slug = models.SlugField(max_length=255, editable=False)

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

    def save(self, *args, **kwargs):
        """ Custom save method to populate slug from name """
        
        self.slug = slugify(self.name)
        
        super().save(*args, **kwargs)

    @classmethod
    def get_recent_objs(cls) -> list:
        """ Returns list of recent created or updated Dish objects."""
        
        recent_timedelta = settings.RECENT_DISH_TIMEDELTA
        recent_objs_queryset = cls.objects.filter(modified_at__date=(timezone.now() - recent_timedelta).date())

        try:
            return [obj for obj in recent_objs_queryset]

        except Exception as e:
            logger.error(e)
            return None
