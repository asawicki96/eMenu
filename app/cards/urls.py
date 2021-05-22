from django.urls import path, include
from rest_framework.routers import DefaultRouter

from cards import views

router = DefaultRouter()

router.register('cards', views.CardViewSet, basename='cards')


urlpatterns = [
    path('', include(router.urls))
]
