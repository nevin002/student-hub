from django.urls import path
from . import views

app_name = 'requests'

urlpatterns = [
    # Main request views
    path('', views.request_list, name='request_list'),
    path('create/', views.request_create, name='request_create'),
    path('<int:pk>/', views.request_detail, name='request_detail'),
    path('<int:pk>/edit/', views.request_edit, name='request_edit'),
    path('<int:pk>/delete/', views.request_delete, name='request_delete'),
    
    # Offer management
    path('<int:pk>/offers/', views.offer_manage, name='offer_manage'),
    path('offers/<int:offer_pk>/accept/', views.offer_accept, name='offer_accept'),
    path('offers/<int:offer_pk>/reject/', views.offer_reject, name='offer_reject'),
    path('offers/<int:offer_pk>/withdraw/', views.offer_withdraw, name='offer_withdraw'),
    
    # User-specific views
    path('my-requests/', views.my_requests, name='my_requests'),
    path('my-offers/', views.my_offers, name='my_offers'),
    
    # Fulfillment
    path('fulfillment/<int:fulfillment_pk>/complete/', views.fulfillment_complete, name='fulfillment_complete'),
    
    # Statistics
    path('stats/', views.request_stats, name='request_stats'),
]
