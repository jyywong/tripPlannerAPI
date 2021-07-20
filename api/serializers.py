from rest_framework import serializers
from .models import Trip, MemberInvite, TripEvent, EventIdea, Alternative
from django.contrib.auth.models import User


class RegisterUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self, *args, **kwargs):
        new_user = User(
            username=self.validated_data['username'],
            email=self.validated_data['email']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError(
                {'password2': 'Passwords must match'})

        new_user.set_password(password)
        new_user.save()
        return new_user


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ['id', 'name', 'members', 'admin']


class MemberInviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberInvite
        fields = ['trip', 'invitee', 'createdAt', 'status']


class TripEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripEvent
        fields = ['time', 'name', 'details', 'locationName',
                  'address', 'placeID', 'lat', 'long']


class EventIdeaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventIdea
        fields = ['suggestor', 'createdAt', 'time', 'name', 'details',
                  'locationName', 'address', 'placeID', 'lat', 'long', 'upvotes', 'downvotes']


class AlternativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alternative
        fields = ['alternativeTo', 'createdAt', 'time', 'name', 'details',
                  'locationName', 'address', 'placeID', 'lat', 'long', 'upvotes', 'downvotes']
