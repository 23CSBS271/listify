from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    COLOR_CHOICES = [
        ('#0d6efd', 'Blue'),
        ('#198754', 'Green'),
        ('#ffc107', 'Yellow'),
        ('#dc3545', 'Red'),
    ]
    name = models.CharField(max_length=64)
    color = models.CharField(max_length=7, default='#0d6efd')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Task(models.Model):
    PRIORITY_CHOICES = (
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    )

    title = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    deadline = models.DateTimeField(blank=True, null=True)
    reminder = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')

    @property
    def is_overdue(self):
        return not self.completed and self.deadline and self.deadline < timezone.now()

    def __str__(self):
        return self.title


class ReminderLog(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    sent_at = models.DateTimeField(auto_now_add=True)
    reminder_type = models.CharField(max_length=20, default='deadline')  # 'deadline' or 'overdue'
    status = models.CharField(max_length=10, default='sent')  # 'sent' or 'failed'
    message = models.TextField(blank=True)

    def __str__(self):
        return f"{self.task.title} → {self.sent_at.strftime('%Y-%m-%d %H:%M')}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username
