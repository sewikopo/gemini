
from decimal import Decimal

from .models import Category,Product, OrderItem,Order,ServiceItem, Service,Staff
from rest_framework import serializers
from django.db import transaction
from drf_writable_nested.serializers import WritableNestedModelSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'products_count']

    products_count = serializers.IntegerField(read_only=True)
    
    
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'inventory', 'unit_price', 'price_with_tax', 'Category']

    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)
    
class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']    

class OrderItemSerializer(WritableNestedModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, order_item: OrderItem):
        return order_item.quantity * order_item.product.unit_price
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity','total_price']


class ServiceItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, service_item: ServiceItem):
        return service_item.quantity * service_item.product.unit_price
    class Meta:
        model = ServiceItem
        fields = ['id', 'product', 'quantity','total_price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, order):
        return sum([item.quantity * item.product.unit_price for item in order.items.all()])

    class Meta:
        model = Order
        fields = ['id', 'placed_at','payment_status', 'items','total_price']
        
    # def to_representation(self, instance):
    #     representation = super(OrderSerializer, self).to_representation(instance)
    #     representation['items'] = OrderItemSerializer(instance.items.all(), many=True).data
    #     return representation
    # def create(instance,self, validated_data):
    #     items = validated_data.pop('items')
    #     instance.items.clear() 
    #     instance.items.add(*items) 
    #     return super(OrderSerializer,self).create(validated_data)
        
class ServiceSerializer(serializers.ModelSerializer):
    items = ServiceItemSerializer(many=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, service):
        return sum([item.quantity * item.product.unit_price for item in service.items.all()])

    class Meta:
        model = Service
        fields = ['id','staff','license_plates','placed_at','payment_status', 'items','total_price']

class AddOrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError(
                'No product with the given ID was found.')
        return value

    def save(self, **kwargs):
        order_id = self.context['order_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        # unit_price = self.validated_data['unit_price']
        try:
            order_item = OrderItem.objects.get(
                order_id=order_id, product_id=product_id)
            order_item.quantity += quantity
            order_item.save()
            self.instance = order_item
        except OrderItem.DoesNotExist:
            self.instance = OrderItem.objects.create(
                order_id=order_id, **self.validated_data)

        return self.instance

    class Meta:
        model = OrderItem
        fields = ['id', 'product_id', 'quantity']

class AddServiceItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError(
                'No product with the given ID was found.')
        return value

    def save(self, **kwargs):
        service_id = self.context['service_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        
        try:
            service_item = ServiceItem.objects.get(
                service_id=service_id, product_id=product_id)
            service_item.quantity += quantity
            service_item.save()
            self.instance = service_item
        except ServiceItem.DoesNotExist:
            self.instance = ServiceItem.objects.create(
                service_id=service_id, **self.validated_data)

        return self.instance

    class Meta:
        model = ServiceItem
        fields = ['id', 'product_id', 'quantity']

class UpdateOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['quantity']

class UpdateServiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceItem
        fields = ['quantity']
        
class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id']
        
class CreateServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['staff', 'license_plates']
        
class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['name']