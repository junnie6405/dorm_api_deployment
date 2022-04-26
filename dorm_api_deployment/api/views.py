from .models import Dorm, Room, Review
from rest_framework import generics, permissions
from .serializers import DormSerializer, RoomSerializer, ReviewSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAdminUser

class Dorm_APIVIEW(generics.ListCreateAPIView):
    queryset = Dorm.objects.all()
    serializer_class = DormSerializer

class Dorm_APIDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dorm.objects.all()
    serializer_class = DormSerializer
    permissions_classes = [IsAdminUser]

class Review_APIVIEW(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsOwnerOrReadOnly,)

class Review_APIDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsOwnerOrReadOnly,)

class Room_APIVIEW(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class Room_APIDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

