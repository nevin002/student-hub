from django.urls import path
from . import views

app_name = 'resources'

urlpatterns = [
    path('', views.resource_list, name='resource_list'),
    path('new/', views.resource_create, name='resource_create'),
    path('<int:pk>/', views.resource_detail, name='resource_detail'),
    path('<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('<int:pk>/vote/', views.toggle_upvote, name='toggle_upvote'),
]
