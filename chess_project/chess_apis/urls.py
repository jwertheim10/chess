from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ml/<str:username>/', views_ml.chess_ml_insights, name='chess_ml_insights'),

]