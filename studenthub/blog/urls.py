from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('new/', views.post_create, name='post_create'),
    path('<int:pk>/', views.post_detail, name='post_detail'),
    path('<int:pk>/comment/', views.add_post_comment, name='add_post_comment'),
]
