from django.urls import path, include
from rest_framework.routers import DefaultRouter

from dishes import views

router = DefaultRouter()

router.register('dishes', views.DishViewSet, basename='dishes')


urlpatterns = [
    path('', include(router.urls))
]
