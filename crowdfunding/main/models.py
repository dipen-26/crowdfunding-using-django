from django.db import models
from django.contrib.auth.models import User

class Campaign(models.Model):
    CATEGORY_CHOICES = [
        ('Health', 'Health'),
        ('Education', 'Education'),
        ('Technology', 'Technology'),
        ('Other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Other')
    custom_category = models.CharField(max_length=100, blank=True, null=True)
    funding_needed = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class CampaignImage(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='campaign_images/')
