from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

# Create your models here.

class Customized_User(AbstractUser):
    pass

class Dorm(models.Model):
    name = models.CharField(max_length=20)
    year_built = models.IntegerField()
    singles = models.IntegerField()
    doubles = models.IntegerField()
    triples = hermodels.IntegerField()
    quadruples = models.IntegerField()
    style = models.CharField(max_length=100)
    number_rooms = models.IntegerField()
    Features = models.TextField()

    def __str__(self):
        return self.name

class Room(models.Model):
    room_number = models.CharField(max_length=10)
    dorm = models.ForeignKey(Dorm, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=20)
    floor = models.IntegerField()
    available = models.BooleanField(default=False)

    def __str__(self):
        return str(self.dorm) + " " + self.room_number

class Review(models.Model):
    reviewer = models.ForeignKey(Customized_User, related_name='reviews', on_delete=models.CASCADE, null=True, blank=True)
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    review_date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField()

    def __str__(self):
        return "review left by " + str(self.reviewer)