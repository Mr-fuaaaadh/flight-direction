from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .models import Airport, Route

class FlightRoutesTest(TestCase):
    def setUp(self):
        self.a1 = Airport.objects.create(name="JFK")
        self.a2 = Airport.objects.create(name="LAX")
        self.a3 = Airport.objects.create(name="SFO")
        self.a4 = Airport.objects.create(name="SEA")

    def test_unique_parent_side_constraint(self):
        # Create first route
        Route.objects.create(parent_airport=self.a1, child_airport=self.a2, position='LEFT', duration=100)
        
        # Try to create another LEFT child for same parent
        with self.assertRaises(IntegrityError):
            Route.objects.create(parent_airport=self.a1, child_airport=self.a3, position='LEFT', duration=200)

    def test_parent_cannot_be_child(self):
        route = Route(parent_airport=self.a1, child_airport=self.a1, position='LEFT', duration=100)
        with self.assertRaises(ValidationError):
            route.clean()

    def test_traversal_logic(self):
        # Create a path: JFK (L) -> LAX (L) -> SFO
        Route.objects.create(parent_airport=self.a1, child_airport=self.a2, position='LEFT', duration=100)
        Route.objects.create(parent_airport=self.a2, child_airport=self.a3, position='LEFT', duration=150)
        
        # Traversal logic from JFK - Left
        current = self.a1
        while True:
            nxt = Route.objects.filter(parent_airport=current, position='LEFT').first()
            if not nxt: break
            current = nxt.child_airport
        
        self.assertEqual(current.name, "SFO")

    def test_duration_stats(self):
        Route.objects.create(parent_airport=self.a1, child_airport=self.a2, position='LEFT', duration=500)
        Route.objects.create(parent_airport=self.a1, child_airport=self.a3, position='RIGHT', duration=50)
        
        from django.db.models import Max, Min
        max_d = Route.objects.aggregate(Max('duration'))['duration__max']
        min_d = Route.objects.aggregate(Min('duration'))['duration__min']
        
        self.assertEqual(max_d, 500)
        self.assertEqual(min_d, 50)
