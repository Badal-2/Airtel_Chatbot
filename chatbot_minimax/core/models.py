from django.db import models
from django.utils import timezone

class Conversation(models.Model):
    """Store conversation history for memory tracking"""
    
    user_id = models.CharField(max_length=100, default="user_1")
    user_message = models.TextField()
    bot_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=100, null=True, blank=True)
    
    class Meta:
        ordering = ['-timestamp']  # Latest first
    
    def __str__(self):
        return f"{self.user_id} - {self.timestamp}"