

from django.db import models
from base.models import BaseModel
from user.models import Account, Address
from product.models import Product, Variation


class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100)
    cart_total = models.PositiveIntegerField()
    tax = models.PositiveIntegerField()
    grand_total = models.PositiveIntegerField()
    payment_method = models.CharField(max_length=30, default='RazorPay')
    is_paid = models.BooleanField(default=True)
    paid_date = models.DateTimeField(auto_now_add=True)
    discount=models.PositiveIntegerField(default=0)


    def __str__(self) -> str:
        return self.transaction_id


class Order(BaseModel):
    order_id = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    delivery_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)
    ordered_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.id} of {self.user}'


class OrderItem(models.Model):
    STATUS = (
        ('Ordered', 'Ordered'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
        ('Refunded', 'Refunded')
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.CharField(max_length=100, null=True,blank=True)
    order_status = models.CharField(max_length=20, choices=STATUS, default='Ordered')
    item_price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    item_total = models.PositiveIntegerField()

    def __str__(self):
        return self.product.title
    



class   ReviewRating(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review = models.TextField(blank=True, null=True)
    rating = models.FloatField()
    status = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)

    def str(self):
        return self.review
