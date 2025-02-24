from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Campaign(models.Model):
    CATEGORY_CHOICES = [
        ('Health', 'Health'),
        ('Education', 'Education'),
        ('Technology', 'Technology'),
        ('Other', 'Other'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Other')
    custom_category = models.CharField(max_length=100, blank=True, null=True)
    funding_needed = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    amount = models.IntegerField(max_length=100, default=0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

    @property
    def funding_percentage(self):
        """Calculate the percentage of funding achieved"""
        if self.funding_needed == 0:
            return 0
        return (float(self.amount) / float(self.funding_needed)) * 100

    @property
    def is_fully_funded(self):
        """Check if campaign is fully funded"""
        return float(self.amount) >= float(self.funding_needed)

    @property
    def funding_status(self):
        """Get the funding status as a string"""
        if self.is_fully_funded:
            return "100% Funded"
        return f"{self.funding_percentage:.1f}% Funded"

class Contribution(models.Model):

    """Model to track individual contributions to campaigns"""
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='contributions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} contributed ₹{self.amount} to {self.campaign.title}"

    class Meta:
        ordering = ['-created_at']
