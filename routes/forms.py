from django import forms
from .models import Airport, Route

class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['parent_airport', 'child_airport', 'position', 'duration']
        widgets = {
            'parent_airport': forms.Select(attrs={'class': 'form-select'}),
            'child_airport': forms.Select(attrs={'class': 'form-select'}),
            'position': forms.Select(attrs={'class': 'form-select'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }

class SearchLastForm(forms.Form):
    DIRECTION_CHOICES = [
        ('LEFT', 'Left'),
        ('RIGHT', 'Right'),
    ]
    start_airport = forms.ModelChoiceField(
        queryset=Airport.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    direction = forms.ChoiceField(
        choices=DIRECTION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
