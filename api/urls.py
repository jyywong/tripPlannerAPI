from django.urls import path, include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api-auth', include('rest_framework.urls')),
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('trips', views.user_trips_list.as_view()),
    path('trip_events/<int:tripID>', views.trip_events_list.as_view()),
    path('event_ideas/<int:tripID>', views.event_idea_list.as_view()),
    path('event_alternatives/<int:eventID>',
         views.event_alternatives_list.as_view())
]
