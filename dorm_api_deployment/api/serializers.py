from rest_framework import serializers
from .models import Dorm, Room, Review, Customized_User

class UserSerializer(serializers.ModelSerializer):
    reviews = serializers.PrimaryKeyRelatedField(many = True, queryset = Review.objects.all())
    class Meta:
        model = Customized_User
        fields = '__all__'

class DormSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Dorm

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Room

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Review