from django.urls import path
from .views import BridgeGateway

urlpatterns = [
    path('', BridgeGateway.as_view(), name='index'),
]
