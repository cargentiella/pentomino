from . import views
from django.urls import path

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('image/', views.ImageView.as_view(), name='image'),
]
