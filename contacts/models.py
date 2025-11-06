from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Contact(models.Model):
    """
    Contact model for storing user contact information.
    Each contact belongs to a specific user (owner).
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['owner', 'email']  # Prevent duplicate emails per user

    def __str__(self):
        return f"{self.name} ({self.email})"
