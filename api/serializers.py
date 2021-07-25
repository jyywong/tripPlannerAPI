from collections import UserDict
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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class TripSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True)

    class Meta:
        model = Trip
        fields = ['id', 'name', 'members']


class TripNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ['id', 'name']


class MemberInviteSerializer(serializers.ModelSerializer):
    admin = serializers.ReadOnlyField(source='trip.admin.username')
    adminEmail = serializers.ReadOnlyField(source='trip.admin.email')
    inviteeEmail = serializers.EmailField(write_only=True)
    invitee = serializers.ReadOnlyField(source='invitee.id')
    trip = TripNameSerializer(read_only=True)
    tripID = serializers.IntegerField(source='trip.id')

    class Meta:
        model = MemberInvite
        fields = ['id', 'admin', 'adminEmail', 'trip', 'tripID', 'inviteeEmail',
                  'invitee',  'createdAt', 'status']

    # TODO: Error handling for nonexistant email
    def create(self, validated_data):
        if User.objects.filter(email=validated_data['inviteeEmail']).exists():
            invitee = User.objects.get(email=validated_data['inviteeEmail'])
            newMemberInvite = MemberInvite.objects.create(
                invitee=invitee, trip=validated_data['trip']
            )
            newMemberInvite.save()
            return newMemberInvite
        else:
            raise serializers.ValidationError(
                'This email does not belong to any user'
            )


class TripEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripEvent
        fields = ['id', 'trip', 'time', 'name', 'details',
                  'address', 'placeID', 'lat', 'long', 'eventIdea', 'alternativeSource']


class EventIdeaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventIdea
        fields = ['id', 'suggestor', 'createdAt', 'time', 'name', 'details',
                  'locationName', 'address', 'placeID', 'lat', 'long', 'upvotes', 'downvotes', 'status']


class AlternativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alternative
        fields = ['id', 'alternativeTo', 'createdBy', 'createdAt', 'time', 'name', 'details',
                  'locationName', 'address', 'placeID', 'lat', 'long', 'upvotes', 'downvotes', 'status']
