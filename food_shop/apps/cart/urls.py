from rest_framework.routers import SimpleRouter

from .views import ShopingCartViewSet

router = SimpleRouter()
router.register(r'cart', ShopingCartViewSet, basename='cart')

urlpatterns = router.urls
