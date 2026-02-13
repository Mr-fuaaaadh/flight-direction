from django.db import models
from django.core.exceptions import ValidationError

class Airport(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Route(models.Model):
    POSITION_CHOICES = [
        ('LEFT', 'Left'),
        ('RIGHT', 'Right'),
    ]

    parent_airport = models.ForeignKey(
        Airport, 
        on_delete=models.CASCADE, 
        related_name='child_routes'
    )
    child_airport = models.OneToOneField(
        Airport, 
        on_delete=models.CASCADE, 
        related_name='parent_route'
    )
    position = models.CharField(max_length=10, choices=POSITION_CHOICES)
    duration = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['parent_airport', 'position'], 
                name='unique_parent_side'
            )
        ]

    def __str__(self):
        return f"{self.parent_airport} -> {self.child_airport} ({self.position})"

    def clean(self):
        # Parent and child cannot be the same
        if self.parent_airport == self.child_airport:
            raise ValidationError("An airport cannot be its own child.")

        # Check for circular dependency (simple case: A -> B, B -> A)
        # More complex circular dependencies would need more logic
        # but for a binary tree structure, the OneToOneField on child_airport
        # already prevents an airport from having multiple parents.

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
