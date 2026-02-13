from django.contrib import admin
from .models import Airport, Route

@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('parent_airport', 'child_airport', 'position', 'duration')
    list_filter = ('position',)
    search_fields = ('parent_airport__name', 'child_airport__name')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('parent_airport', 'child_airport')
