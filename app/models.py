
from django.db import models
from django.contrib.auth.models import User
from django.core .validators import MaxValueValidator
MaxValueValidator


STATE_CHOICES = (
    ('KERALA', 'KERALA'),
    ('KARNATAKA', 'KARNATAKA'),
    ('ANDRA PRADESH', 'ANDRA PRADESH'),
    ('MAHARASHTA', 'MAHARASTRA'))

CITY_CHOICES = (
    ('banglore', 'banglore'),
    ('kochi', 'kochi'),
    ('hydrabad', 'hydrabad'),
    ('pune', 'pune')
)


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    locality = models.CharField(max_length=200, null=True)
    city = models.CharField( max_length=50, null=True)
    zipcode = models.IntegerField(null=True)
    state = models.CharField( max_length=50, null=True)


    def __str__(self):
        return str(self.id)


CATEGORY_CHOICES = (
    ('M', 'MOBILES'),
    ('L', 'LAPTOP'),
    ('TW', 'TOP WEAR'),
    ('BW', 'BUTTOM WEAR'),

)


class product(models.Model):
    title = models.CharField(max_length=50)
    selling_price = models.FloatField()
    discount_price = models.FloatField()
    discription = models.TextField(max_length=100, null=True)
    brand = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to='producting')


    def __str__(self):
        return str(self.id)


class cart(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


    def __str__(self):
        return str(self.id)
    @property
    def total_Cost(self):
        return self.quantity * self.product.discount_price


STATUS_CHOICE = (

    ('ACCEPTED', 'ACCEPTED'),
    ('PACKED', 'PACKED'),
    ('DELIVERED', 'DELIVERED'),
    ('CANCEL', 'CANCEL'),
)


class orderplaced(models.Model):

    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    orderes_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICE, default='pending')
    feedback = models.TextField(null=True)


class OrderDetails(models.Model):
    order = models.ForeignKey(orderplaced,on_delete=models.CASCADE)
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICE, default='pending')
    created_date = models.DateTimeField(auto_now_add=True)
