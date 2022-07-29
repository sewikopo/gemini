from itertools import product
from urllib import request, response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.pagination import PageNumberPagination
from rest_framework_swagger.views import get_swagger_view
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.db.models.aggregates import Count
from django.template import Template, Context, loader
from .models import Category, Service, Product, Order,OrderItem,ServiceItem
from .serializers import  AddOrderItemSerializer, CategorySerializer, OrderItemSerializer, CreateOrderSerializer
from .serializers import ProductSerializer, OrderSerializer, UpdateOrderItemSerializer
from .serializers import ServiceSerializer, CreateServiceSerializer, AddServiceItemSerializer, UpdateServiceItemSerializer
from .serializers import ServiceItemSerializer
from store import serializers 


# schema_view = get_swagger_view(title='Store API')
# url(r'^$', schema_view)

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_field = ['category_id']
    #pagination_class = DefaultPagination
    search_fields = ['title']
    #ordering_fields = ['unit_price', 'last_update']
    def get_serializer_context(self):
        return {'request': self.request}

    
    # def get(self, request):
    #     #self.object = self.get_object()
    #     #return Response({'Product': self.object})
    #     products = Product.objects.all()
    #     serializer = ProductSerializer(products, many=True)
    #     return Response({'products': serializer.data}, template_name='product.html')
    
    
    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.orderitems.count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with an order item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(
        products_count=Count('products')).all()
    serializer_class = CategorySerializer

    def delete(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        if category.products.count() > 0:
            return Response({'error': 'Category cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class OrderViewSet(ModelViewSet):
    queryset=Order.objects.all()
    serializer_class=OrderSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(
            data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(data = serializer.data)
    
    
class ServiceViewSet(ModelViewSet):
    queryset=Service.objects.all()
    serializer_class=ServiceSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}

    def create(self, request, *args, **kwargs):
        serializer = CreateServiceSerializer(
            data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = ServiceSerializer(order)
        return Response(serializer.data)
    

class OrderItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete','head', 'options']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddOrderItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderItemSerializer
        return OrderItemSerializer

    def get_queryset(self):
        return OrderItem.objects.filter(order_id=self.kwargs['order_pk']).select_related('product')

    def get_serializer_context(self):
        return {'order_id': self.kwargs['order_pk']}

class ServiceItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete','head', 'options']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddServiceItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateServiceItemSerializer
        return ServiceItemSerializer

    def get_queryset(self):
        return ServiceItem.objects.filter(service_id=self.kwargs['service_pk']).select_related('product')

    def get_serializer_context(self):
        return {'service_id': self.kwargs['service_pk']}
            
