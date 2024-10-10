from rest_framework import routers

from .views import ProductViewSet

router = routers.SimpleRouter()

router.register('products', ProductViewSet, basename='products')

urlpatterns = router.urls
