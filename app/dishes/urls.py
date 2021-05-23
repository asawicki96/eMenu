from django.urls import path, include
from rest_framework.routers import DefaultRouter

from dishes import views

app_name = 'dishes'

router = DefaultRouter()

router.register('dishes', views.DishViewSet, basename='dishes')


urlpatterns = [
    path('', include(router.urls)),
]
