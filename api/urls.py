from django.urls import path, include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api-auth', include('rest_framework.urls')),
    path('signup', views.api_registration_view),
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('user_details/<int:pk>', views.user_details.as_view()),
    path('create_member_invite', views.create_member_invite.as_view()),
    path('user_invites', views.user_invites_list.as_view()),
    path('single_invite/<int:pk>', views.single_invite.as_view()),
    path('trips', views.user_trips_list.as_view()),
    path('trip/<int:pk>', views.user_single_trip.as_view()),
    path('remove_from_trip/<int:pk>', views.remove_member_from_trip.as_view()),
    path('trip_events/<int:tripID>', views.trip_events_list.as_view()),
    path('trip_event/<int:pk>', views.trip_single_event.as_view()),
    path('event_ideas/<int:tripID>', views.event_idea_list.as_view()),
    path('event_idea/<int:pk>', views.single_event_idea.as_view()),
    path('event_alternatives/<int:eventID>',
         views.event_alternatives_list.as_view()),
    path('event_alternative/<int:pk>', views.single_alternative.as_view())
]
