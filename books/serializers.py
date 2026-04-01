from rest_framework import serializers
from .models import Book
import re

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    def validate_isbn(self, value):
        value = value.replace('-', '')
        if not re.match(r'^(\d{10}|\d{13})$', value):
            raise serializers.ValidationError("ISBN must exactly contain 10 or 13 digits (hyphens allowed).")
        return value
