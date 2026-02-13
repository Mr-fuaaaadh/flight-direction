from django.urls import path
from .views import HomeView, RouteCreateView, LastReachableSearchView, DurationStatsView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('route/add/', RouteCreateView.as_view(), name='add_route'),
    path('search/', LastReachableSearchView.as_view(), name='search_last'),
    path('stats/', DurationStatsView.as_view(), name='stats'),
]
