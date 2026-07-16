from django.db import models
from django.utils import timezone


# Create your models here.
class Task(models.Model):
    PRIORITY_CHOICES = [
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
        (4, 'Very High'),
        (5, 'Critical'),
    ]
    
    title = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)
    posted_at = models.DateTimeField(default=timezone.now)
    due_at = models.DateTimeField(null=True, blank=True)
    priority = models.IntegerField(default=3, choices=PRIORITY_CHOICES)
    order = models.IntegerField(default=0)

    def is_overdue(self, dt):
        if self.due_at is None:
            return False
        return self.due_at < dt
