from django.urls import path
from . import views

urlpatterns = [
    path('create_room/', views.create),
    path('join_room/', views.join),
    path('room/', views.room),
    path('get_token/', views.getToken),
    path('fetch_room/', views.fetchRoom),

    path('create_member/', views.createMember),
    path('get_member/', views.getMember),
    path('delete_member/', views.deleteMember),
]