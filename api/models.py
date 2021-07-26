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
    date = models.DateField()


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

    def AcceptInvite(self):
        self.trip.members.add(self.invitee)

    def save(self, *args, **kwargs):
        if self.pk is not None:
            if self.status == 'Accepted':
                self.AcceptInvite()
        super().save(*args, **kwargs)


class TripEvent(models.Model):
    trip = models.ForeignKey(
        Trip, on_delete=models.CASCADE, related_name="tripEvents")
    time = models.DateTimeField()
    name = models.CharField(max_length=255)
    details = models.TextField()
    address = models.TextField(max_length=255)
    placeID = models.TextField(max_length=255)
    lat = models.FloatField()
    long = models.FloatField()
    eventIdea = models.ForeignKey(
        'EventIdea', on_delete=models.CASCADE, related_name="tripEvent", null=True, blank=True)
    alternativeSource = models.ForeignKey(
        'Alternative', on_delete=models.CASCADE, related_name="alternativeResult", null=True, blank=True
    )


class EventIdea(models.Model):
    tripSuggestedTo = models.ForeignKey(
        Trip, on_delete=models.CASCADE, related_name="eventIdeas")
    suggestor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    createdAt = models.DateTimeField()
    time = models.DateTimeField()
    name = models.CharField(max_length=255)
    details = models.TextField()
    locationName = models.TextField(max_length=255)
    address = models.TextField(max_length=255)
    placeID = models.TextField(max_length=255)
    lat = models.FloatField()
    long = models.FloatField()
    upvotes = models.IntegerField()
    downvotes = models.IntegerField()
    status_choices = [
        ('Suggested', 'Suggested'),
        ('Added', 'Added'),
    ]
    status = models.CharField(
        max_length=100,
        choices=status_choices,
        default='Suggested'
    )

    def AddEventIdeaToTripEvents(self):
        TripEvent.objects.create(
            trip=self.tripSuggestedTo,
            time=self.time,
            name=self.name,
            details=self.details,
            address=self.address,
            placeID=self.placeID,
            lat=self.lat,
            long=self.long,
            eventIdea=self
        )

    def save(self, *args, **kwargs):
        if self.pk is not None:
            if self.status == 'Added':
                self.AddEventIdeaToTripEvents()
        super().save(*args, **kwargs)


class Alternative(models.Model):
    alternativeTo = models.ForeignKey(
        TripEvent, on_delete=models.CASCADE, related_name="alternatives")
    createdBy = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="alternatives")
    createdAt = models.DateTimeField()
    time = models.DateTimeField()
    name = models.CharField(max_length=255)
    details = models.TextField()
    locationName = models.TextField(max_length=255, null=True, blank=True)
    address = models.TextField(max_length=255, null=True, blank=True)
    placeID = models.TextField(max_length=255)
    lat = models.FloatField(null=True, blank=True)
    long = models.FloatField(null=True, blank=True)
    upvotes = models.IntegerField()
    downvotes = models.IntegerField()
    status_choices = [
        ('Suggested', 'Suggested'),
        ('Added', 'Added'),
    ]
    status = models.CharField(
        max_length=100,
        choices=status_choices,
        default='Suggested'
    )

    def OverwriteTripEventWithAlternative(self):
        targetTripEvent = self.alternativeTo
        targetTripEvent.name = self.name
        targetTripEvent.details = self.details
        targetTripEvent.address = self.address
        targetTripEvent.placeID = self.placeID
        targetTripEvent.lat = self.lat
        targetTripEvent.long = self.long
        targetTripEvent.alternativeSource = self
        targetTripEvent.save()

    def save(self, *args, **kwargs):
        if self.pk is not None:
            if self.status == 'Added':
                self.OverwriteTripEventWithAlternative()
        super().save(*args, **kwargs)
