from django.db import router
from django.urls import include, path
from rest_framework import routers

from .views import CategoryViewSet


router = routers.SimpleRouter()

router.register('categories', CategoryViewSet)
#router.register('products', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]