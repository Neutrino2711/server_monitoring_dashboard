from django.urls import path 
from rest_framework.routers import DefaultRouter
from . import views 
from .views import dashboard_view

router = DefaultRouter()
router.register(r'servers', views.ServerViewSet, basename = 'server')

urlpatterns = [
    path('servers/<uuid:server_id>/metrics/',views.ServerMetricsView.as_view(),name='server-metrics'),
    path('dashboard/',dashboard_view,name = 'dashboard')

] + router.urls