from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
from decimal import Decimal

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(
        max_length=17,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^(?=(?:\D*\d){10}$|(?:\D*\d){13}$)[-\d]+$',
                message="ISBN must be 10 or 13 digits (hyphens are allowed)."
            )
        ]
    )
    cost_usd = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    selling_price_local = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    stock_quantity = models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=100)
    supplier_country = models.CharField(max_length=100)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.author}"
