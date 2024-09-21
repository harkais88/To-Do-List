from django.db import models

class Task(models.Model):
    name = models.CharField(max_length=255)

    STATUS_CHOICES = [
        ("Completed","Completed"),
        ("Pending","Pending"),
    ]
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default="Pending")

    def __str__(self):
        return f"Task: {self.name} Status: {self.status}"