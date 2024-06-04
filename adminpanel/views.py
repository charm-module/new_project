from app.models import Customer, OrderDetails, orderplaced, product
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.core.files.base import ContentFile
import base64
from django.db.models import Q


# Create your views here.

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                if user.is_superuser:
                    login(request, user)
                    return redirect("admin_home")
                else:
                    messages.error(request, 'Only Admin can acces')
                    return redirect("login")
            else:
                messages.error(request, 'Invalid Login Details')
                return redirect("login")
        except:
            messages.error(request, 'Invalid Login Details')
            return redirect("login")

    else:
        return render(request, 'adminpanel/admin_login.html')


def admin_home(request):
    if request.user.is_superuser:
        return render(request, 'adminpanel/home.html')

    else:
        return redirect('login')


def admin_product(request):
    if request.user.is_superuser:
        products = product.objects.all()
        context = {
            'products': products
        }
        return render(request, 'adminpanel/admin_view_product.html', context)

    else:
        return redirect('login')


def add_product(request):
    if request.user.is_superuser:
        return render(request, 'adminpanel/add_product.html')
    else:
        return redirect('login')


def save_add_product(request):
    if request.user.is_superuser:
        title = request.POST.get('product_name')
        selling_price = request.POST.get('selling_price')
        discount_price = request.POST.get('discount_price')
        brand = request.POST.get('brand')
        category = request.POST.get('category')
        description = request.POST.get('description')

        image_data = request.POST.get('image64data')
        data = None
        if image_data:
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        item = product()
        item.title = title
        item.selling_price = selling_price
        item.discount_price = discount_price
        item.discription = description
        item.brand = brand
        item.category = category
        if data:
            item.product_image = data
        item.save()

        return redirect('admin_product')
    else:
        return redirect('login')


def edit_product(request, id):
    product_obj = product.objects.get(id=id)
    return render(request, 'adminpanel/edit_product.html', {'product': product_obj})


def save_edit_product(request):
    if request.user.is_superuser:
        product_id = request.POST.get('product_id')
        title = request.POST.get('product_name')
        selling_price = request.POST.get('selling_price')
        discount_price = request.POST.get('discount_price')
        brand = request.POST.get('brand')
        category = request.POST.get('category')
        description = request.POST.get('description')

        image_data = request.POST.get('image64data')
        data = None
        if image_data:
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        item = product.objects.get(id=product_id)
        item.title = title
        item.selling_price = selling_price
        item.discount_price = discount_price
        item.discription = description
        item.brand = brand
        item.category = category
        if data:
            item.product_image = data
        item.save()

        return redirect('admin_product')
    else:
        return redirect('login')


def delete_product(request, id):
    if request.user.is_superuser:
        product_obj = product.objects.get(id=id).delete()
        return redirect('admin_product')
    else:
        return redirect('login')


def customers(request):
    if request.user.is_superuser:
        customers = User.objects.filter(~Q(is_superuser=True)).values(
            'id', 'first_name', 'last_name', 'email', 'customer__city')
        print(customers)

        return render(request, 'adminpanel/customers.html', {'customer': customers})

    else:
        return redirect('login')


def edit_customers(request, id):
    if request.user.is_superuser:
        user = User.objects.get(id=id)
        custom = Customer.objects.get(user=user)
        context = {
            'user': user,
            'customer': custom
        }
        return render(request, 'adminpanel/edit_customers.html', context)
    else:
        return redirect('login')


def save_edit_customer(request):
    if request.user.is_superuser:
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        locality = request.POST.get('locality')
        customer_id = request.POST.get('customer_id')

        user = User.objects.get(id=customer_id)
        cust = Customer.objects.get(user=user)
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        cust.locality = locality
        cust.save()
        user.save()
        return redirect('customers')

    else:
        return redirect('login')


def delete_customer(request, id):
    if request.user.is_superuser:
        User.objects.get(id=id).delete()
        return redirect('customers')
    else:
        return redirect('login')


def admin_orders(request):
    
    if request.user.is_superuser:
        try:
            filter=request.GET['filter']
        except:
            filter=None
        print(filter)
        if filter:
            orders=orderplaced.objects.filter(status=filter)
        else:
                
    
            orders = orderplaced.objects.all()
        return render(request, 'adminpanel/admin_view_order.html', {'orders': orders})
    else:
        return redirect('login')


def order_status_change(request):
    id = request.GET.get('id')
    value = request.GET.get('val')
    order = orderplaced.objects.get(id=id)
    order.status = value
    order_details = OrderDetails.objects.create(order=order, status=value)
    order.save()
    return JsonResponse({'sucess': True})


def delete_order(request, id):
    orderplaced.objects.get(id=id).delete()
    return redirect('admin_orders')


def admin_logout(request):
    logout(request)
    return redirect('login')


def get_order_details(request):
    id = request.GET.get('id')
    order_details = list(OrderDetails.objects.filter(
        order=id).values_list('status', 'created_date').order_by('id'))

    return JsonResponse({'success': True, 'data': order_details})
