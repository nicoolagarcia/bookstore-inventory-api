from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.conf import settings
import requests
import datetime

from .models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request):
        category = request.query_params.get('category')
        if not category:
            return Response({"error": "Parámetro 'category' requerido"}, status=status.HTTP_400_BAD_REQUEST)
        
        queryset = self.get_queryset().filter(category__icontains=category)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='low-stock')
    def low_stock(self, request):
        threshold = request.query_params.get('threshold')
        if not threshold:
            return Response({"error": "Parámetro 'threshold' requerido"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            threshold = int(threshold)
        except ValueError:
            return Response({"error": "'threshold' debe ser entero"}, status=status.HTTP_400_BAD_REQUEST)
        
        queryset = self.get_queryset().filter(stock_quantity__lt=threshold)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    @action(detail=True, methods=['post'], url_path='calculate-price')
    def calculate_price(self, request, pk=None):
        book = self.get_object()
        
        try:
            api_url = getattr(settings, 'EXCHANGE_RATE_API_URL', 'https://api.exchangerate-api.com/v4/latest/USD')
            # Se asume formato EUR
            response = requests.get(api_url, timeout=5)
            response.raise_for_status()
            data = response.json()
            exchange_rate = data.get('rates', {}).get('EUR', 0.85)
        except requests.RequestException:
            # Si la API falla, se usa la tasa por defecto
            exchange_rate = 0.85

        cost_usd = float(book.cost_usd)
        cost_local = cost_usd * exchange_rate
        margin_percentage = 1.40
        selling_price_local = cost_local * margin_percentage
        
        # actualizamos el precio de venta en la base de datos
        book.selling_price_local = round(selling_price_local, 2)
        book.save()

        result = {
            "id": book.id,
            "cost_usd": cost_usd,
            "exchange_rate": float(exchange_rate),
            "cost_local": round(cost_local, 2),
            "margin_percentage": int(round((margin_percentage - 1) * 100)),
            "selling_price_local": float(book.selling_price_local),
            "currency": "EUR",
            "calculation_timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
        
        return Response(result, status=status.HTTP_200_OK)
