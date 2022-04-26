from django.urls import path
from .views import Dorm_APIVIEW, Dorm_APIDetail, Room_APIVIEW, Room_APIDetail, Review_APIVIEW, Review_APIDetail

urlpatterns = [
    path('dorm/', Dorm_APIVIEW.as_view(), name ='home-api'),
    path('dorm/<int:pk>/', Dorm_APIDetail.as_view()),
    path('room/', Room_APIVIEW.as_view(), name='room-api'),
    path('room/<int:pk>/', Room_APIDetail.as_view()),
    path('review/', Review_APIVIEW.as_view()),
    path('review/<int:pk>/', Review_APIDetail.as_view()),
]