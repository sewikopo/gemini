from django.db import models
from django.core.validators import MinValueValidator

class Category(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']

class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    unit_price = models.DecimalField(
    max_digits=8,
    decimal_places=2,
    validators=[MinValueValidator(1)])
    inventory = models.IntegerField(validators=[MinValueValidator(0)])
    last_update = models.DateTimeField(auto_now=True)
    Category = models.ForeignKey(
        Category, on_delete=models.PROTECT,null=True, related_name='products')
   
    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']
        
        
        
class Order(models.Model):
    PAYMENT_STATUS_CASH = 'C'
    PAYMENT_STATUS_BCA = 'B'
    PAYMENT_STATUS_MANDIRI = 'M'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_CASH, 'CASH'),
        (PAYMENT_STATUS_BCA, 'BCA'),
        (PAYMENT_STATUS_MANDIRI, 'MANDIRI')
    ]

    placed_at = models.DateTimeField(auto_now_add=True) 
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_CASH)
    

class Staff(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self) -> str:
         return self.name

    class Meta:
        ordering = ['name']
 

class Service(models.Model):
    PAYMENT_STATUS_CASH = 'C'
    PAYMENT_STATUS_BCA = 'B'
    PAYMENT_STATUS_MANDIRI = 'M'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_CASH, 'CASH'),
        (PAYMENT_STATUS_BCA, 'BCA'),
        (PAYMENT_STATUS_MANDIRI, 'MANDIRI')
    ]

    placed_at = models.DateTimeField(auto_now_add=True) 
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_CASH)

    staff = models.ForeignKey(Staff, on_delete=models.PROTECT)
    license_plates = models.CharField(max_length=255)
    
      
class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey(Product,on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    
    class Meta:
        unique_together = [['order', 'product']]

class ServiceItem(models.Model):
    service = models.ForeignKey(Service,on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey(Product,on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    
    class Meta:
        unique_together = [['service', 'product']]

    
