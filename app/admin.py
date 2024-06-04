from django.contrib import admin
from app.models import*

admin.site.register(Customer)
class customermodelAdmin(admin.ModelAdmin):
    list_display = ['id','user','name','locality','city','zipcode','state']

admin.site.register(product)
class productModelAdmin(admin.ModelAdmin):
    list_display=['id','title','selling_price','discounted_price','brand','category','product_image']

admin.site.register(cart)
class cartModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']

admin.site.register(orderplaced)