from django.db import models
from django.db.models.fields import related
from tripPlanner import settings
# Create your models here.


class Trip(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="trips")
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              related_name="admin_trips")


class MemberInvite(models.Model):
    trip = models.ForeignKey(
        Trip, on_delete=models.CASCADE, related_name="invites")
    invitee = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="invites")
    createdAt = models.DateField(auto_now=True)
    status_choices = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
    ]
    status = models.CharField(
        max_length=100,
        choices=status_choices,
        default='Pending'
    )


class TripEvent(models.Model):
    time = models.TimeField()
    name = models.CharField(max_length=255)
    details = models.TextField()
    locationName = models.TextField(max_length=255)
    address = models.TextField(max_length=255)
    placeID = models.TextField(max_length=255)
    lat = models.FloatField()
    long = models.FloatField()


class EventIdea(models.Model):
    tripSuggestedTo = models.ForeignKey(
        Trip, on_delete=models.CASCADE, related_name="eventIdeas")
    suggestor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    createdAt = models.DateTimeField()
    time = models.TimeField()
    name = models.CharField(max_length=255)
    details = models.TextField()
    locationName = models.TextField(max_length=255)
    address = models.TextField(max_length=255)
    placeID = models.TextField(max_length=255)
    lat = models.FloatField()
    long = models.FloatField()
    upvotes = models.IntegerField()
    downvotes = models.IntegerField()


class Alternative(models.Model):
    alternativeTo = models.ForeignKey(
        TripEvent, on_delete=models.CASCADE, related_name="alternatives")
    createdAt = models.DateTimeField()
    time = models.TimeField()
    name = models.CharField(max_length=255)
    details = models.TextField()
    locationName = models.TextField(max_length=255)
    address = models.TextField(max_length=255)
    placeID = models.TextField(max_length=255)
    lat = models.FloatField()
    long = models.FloatField()
    upvotes = models.IntegerField()
    downvotes = models.IntegerField()
