from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, permissions, serializers
from .models import Trip, MemberInvite, TripEvent, EventIdea, Alternative
from .serializers import RegisterUserSerializer, TripSerializer, TripEventSerializer, MemberInviteSerializer, EventIdeaSerializer, AlternativeSerializer
# Create your views here.


@api_view(['POST'])
def api_registration_view(request):
    serializer = RegisterUserSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        new_user = serializer.save()
        data['response'] = 'Successfully created new user'
        data['username'] = new_user.username
        data['email'] = new_user.email
    else:
        data = serializer.errors
    return Response(data)


class user_invites_list(generics.ListAPIView):
    serializer_class = MemberInvite

    def get_queryset(self):
        userInvites = MemberInvite.objects.filter(invitee=self.request.user)
        return userInvites


class create_member_invite(generics.CreateAPIView):
    serializer_class = MemberInvite


class user_trips_list(generics.ListCreateAPIView):
    serializer_class = TripSerializer
    queryset = Trip.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        userTrips = Trip.objects.filter(members=self.request.user)
        return userTrips


class trip_events_list(generics.ListCreateAPIView):
    serializer_class = TripEventSerializer

    def get_queryset(self):
        tripEvents = TripEvent.objects.filter(trip=self.kwargs['tripID'])
        return tripEvents


class event_idea_list(generics.ListCreateAPIView):
    serializer_class = EventIdeaSerializer

    def get_queryset(self):
        tripEventIdeas = EventIdea.objects.filter(
            tripSuggestedTo=self.kwargs['tripID'])
        return tripEventIdeas


class event_alternatives_list(generics.ListCreateAPIView):
    serializer_class = AlternativeSerializer

    def get_queryset(self):
        eventAlternatives = Alternative.objects.filter(
            alternativeTo=self.kwargs['eventID'])
        return eventAlternatives
