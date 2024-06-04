from ast import Pass
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from .models import Customer, OrderDetails, product, cart, orderplaced
from .forms import CustomerProfileForm, CustomerRegistrationForm
from django.db.models import Q
from django.contrib.auth.models import User,auth
from django.contrib.auth import login, logout



# def home(request):

# return render(request, 'app/home.html')

def logins(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:

            user = auth.authenticate(username=username, password=password)
            if user is not None:
                if user.is_superuser:
                    login(request, user)
                    return redirect("admin_home")
                else:
                    login(request, user)
                    return redirect("profile")
            else:
                messages.error(request, 'Invalid Login Details')
                return redirect("login")
        except Exception as e:
            print(e)
            messages.error(request, 'Invalid Login Details')
            return redirect("login")
     
    else:
        return render(request,'app/login.html')




class ProductView(View):
    def get(self, request):
        print('topwears')
        topwears = product.objects.filter(category='TW')
        bottomwears = product.objects.filter(category='BW')
        mobile = product.objects.filter(category='M')
        print(mobile)
        return render(request, 'app/home.html', {'topwears': topwears, 'bottomwears': bottomwears, 'mobile': mobile})


class ProductDetailView(View):
    def get(self, request, pk):
        print(pk)
        products = product.objects.get(pk=pk)
        return render(request, 'app/productdetail.html',
                      {'product': products})


def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    products = product.objects.get(id=product_id)
    cart(User=user, product=products).save()
    return redirect('/cart')


def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        carts = cart.objects.filter(User=user)
        print(carts)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in cart.objects.all() if p.User == user]
        print(cart_product)
        totalamount = 0
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discount_price)
                amount += tempamount
                totalamount = amount + shipping_amount
            return render(request, 'app/addtocart.html', {'carts': carts, 'totalamount': totalamount, 'amount': amount})
        else:
            return render(request, 'app/emptycart.html')

    else:
        return render(request, 'app/emptycart.html')


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = cart.objects.get(Q(product=prod_id) & Q(User=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in cart.objects.all() if p.User ==
                        request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discount_price)
    amount += tempamount

    data = {
        'quantity': c.quantity,
        'amount': amount,
        'totalamount': amount + shipping_amount
    }
    return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = cart.objects.get(Q(product=prod_id) & Q(User=request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in cart.objects.all() if p.User ==
                        request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discount_price)
        amount += tempamount
        totalamount = amount

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount + shipping_amount
        }
        return JsonResponse(data)


def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = cart.objects.filter(Q(product=prod_id) & Q(User=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in cart.objects.all() if p.User ==
                        request.user]
        tempamount = 0
        for p in cart_product:
            tempamount = (p.quantity * p.product.discount_price)
        amount += tempamount

        data = {

            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)


def buy_now(request):
    return render(request, 'app/addtocart.html')


def profile(request):
    return render(request, 'app/profile.html')


def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add': add})


def orders(request):
    orders = orderplaced.objects.filter(User=request.user).order_by('-id')
    print(orders)
    return render(request, 'app/orders.html', {'orders': orders})


def mobile(request, data=None):
    print(data)
    if data == None:
        mobiles = product.objects.filter(category='M')
    elif data == 'Redmi' or data == 'Samsung':
        mobiles = product.objects.filter(category="M", brand__icontains=data)
        print(mobiles)
    elif data == 'below':
        mobiles = product.objects.filter(
            category="M").filter(discount_price__lt=10000)
        #mobiles = product.objects.filter(category="M").filter(brand=data)
    elif data == 'above':
        mobiles = product.objects.filter(
            category="M").filter(discount_price__gt=10000)
    return render(request, 'app/mobile.html', {'mobiles': mobiles})


def customerregistration(request):
    if request.method == "POST":
        #form = CustomerRegistrationForm(request.POST)
        # if form.is_valid():
        if request.POST.get('password1') == request.POST.get('password2'):
            user = User.objects.create_user(username=request.POST.get(
                'username'), password=request.POST.get('password1'))
            messages.success(
                request, 'congratulations!! Registered Successfully')
        else:
            messages.success(request, 'password is not match')

        return redirect("customerregistration")
    else:
        return render(request, 'app/customerregistration.html')


def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = cart.objects.filter(User=user)
    amount = 0.0
    shipping_amount = 70.0
    cart_product = [p for p in cart.objects.all() if p.User == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discount_price)
    amount += tempamount
    totalamount = amount + shipping_amount
    return render(request, 'app/checkout.html', {'add': add, 'totalamount': totalamount, 'cart_items': cart_items})


def getcartcount(request):
    cart_count = cart.objects.filter(User=request.user).count()
    return JsonResponse({"status": "success", "count": cart_count})


def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    carts = cart.objects.filter(User=user)
    for c in carts:
        order = orderplaced.objects.create(User=user, Customer=customer, product=c.
                    product, quantity=c.quantity)
        print(order)
        order_details = OrderDetails(order = order).save()
        c.delete()
        return redirect("orders")


class ProfileView(View):
    def get(self, request):
        user = request.user
        customer = Customer.objects.filter(user=user)
        if not customer:
            form = CustomerProfileForm()
            return render(request, 'app/profile.html', {'form': form,
                                                        'active': 'btn-primary'})
        else:
            return redirect('home')

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form. cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            State = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name, locality=locality,
                           city=city, state=State, zipcode=zipcode)
            reg.save()
            messages.success(
                request, 'congratulations!! profile updated succesfully')
            return redirect("home")
        else:
            print(form.errors)
            messages.success(request, str(form.errors))
            return render(request, 'app/profile.html')


def submit_order_feedback(request, id):
    print(id)
    feedback = request.POST.get('feedback')
    order = orderplaced.objects.get(id=id)
    order.feedback = feedback
    order.save()
    return redirect('orders')


def order_details(request,id):
    order_details = OrderDetails.objects.filter(order = id).order_by('id')
    order = orderplaced.objects.get(id=id)
    context = {
        'order_details':order_details,
        'order':order
    }
    return render(request,'app/order_details.html',context)

def  all_orders(request):
    orders = orderplaced.objects.filter(User=request.user).order_by('-id')
    print(orders)
    return render(request, 'app/my_order.html', {'orders': orders})

