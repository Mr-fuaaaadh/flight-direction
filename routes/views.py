from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, TemplateView, ListView
from django.db.models import Max, Min
from .models import Airport, Route
from .forms import RouteForm, SearchLastForm

class HomeView(ListView):
    model = Airport
    template_name = 'routes/base.html'
    context_object_name = 'airports'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['routes'] = Route.objects.all().select_related('parent_airport', 'child_airport')
        return context

class RouteCreateView(CreateView):
    model = Route
    form_class = RouteForm
    template_name = 'routes/route_form.html'
    success_url = reverse_lazy('home')

class LastReachableSearchView(FormView):
    form_class = SearchLastForm
    template_name = 'routes/search_last.html'

    def form_valid(self, form):
        start_airport = form.cleaned_data['start_airport']
        direction = form.cleaned_data['direction']
        
        # Traverse logic
        current_node = start_airport
        while True:
            next_route = Route.objects.filter(
                parent_airport=current_node, 
                position=direction
            ).select_related('child_airport').first()
            
            if not next_route:
                break
            current_node = next_route.child_airport
            
        return render(self.request, 'routes/last_result.html', {
            'start_airport': start_airport,
            'direction': direction,
            'last_airport': current_node
        })

class DurationStatsView(TemplateView):
    template_name = 'routes/duration_result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Longest duration
        max_duration = Route.objects.aggregate(Max('duration'))['duration__max']
        context['longest_route'] = Route.objects.filter(duration=max_duration).select_related('parent_airport', 'child_airport').first()
        
        # Shortest duration
        min_duration = Route.objects.aggregate(Min('duration'))['duration__min']
        context['shortest_route'] = Route.objects.filter(duration=min_duration).select_related('parent_airport', 'child_airport').first()
        
        return context
