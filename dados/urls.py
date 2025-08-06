# urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegistroFinanceiroViewSet

router = DefaultRouter()
router.register(r'registros', RegistroFinanceiroViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
