from myshop.forms import CustomerRegistrationForm
from django import forms
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Product, Category, Customer, Carousel, Cart, Order, Review, Product_Image
from django.views import View
from .forms import CustomerRegistrationForm, MyProfileForm, MyUserProfileForm, MyCheckoutForm, MyUserCheckoutForm, PaymentOptionForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def Home(request):
    carousel_slides = Carousel.objects.all()
    categories = Category.objects.all()
    all_product = Paginator(Product.objects.all().order_by('-id')[:40], 8)
    page = request.GET.get('page')
    try:
        product = all_product.page(page)
    except PageNotAnInteger:
        product = all_product.page(1)
    except EmptyPage:
        product = all_product.page(all_product.num_pages)

    cart_quantity = 0
    user = request.user
    if user.is_authenticated:
        cart_item = Cart.objects.filter(user=user)
        for i in cart_item:
            cart_quantity += i.quantity
    context = {
        'carousel_slides': carousel_slides,
        'product': product,
        'categories': categories,
        'cart_quantity': cart_quantity,
    }
    return render(request, 'home.html', context)


def Categories(request, id):
    categories = Category.objects.all()
    category = Category.objects.get(id=id)
    products = Paginator(Product.objects.filter(
        category=category).order_by('-id'), 2)
    page = request.GET.get('page')
    try:
        product = products.page(page)
    except PageNotAnInteger:
        product = products.page(1)
    except EmptyPage:
        product = products.page(products.num_pages)

    cart_quantity = 0
    user = request.user
    if user.is_authenticated:
        cart_item = Cart.objects.filter(user=user)
        for i in cart_item:
            cart_quantity += i.quantity
    context = {
        'product': product,
        'categories': categories,
        'cart_quantity': cart_quantity,
    }
    return render(request, 'categories.html', context)


def Allcategories(request):
    categories = Category.objects.all()
    products = Paginator(Product.objects.all().order_by('-id'), 2)
    page = request.GET.get('page')
    try:
        all_product = products.page(page)
    except PageNotAnInteger:
        all_product = products.page(1)
    except EmptyPage:
        all_product = products.page(products.num_pages)

    cart_quantity = 0
    user = request.user
    if user.is_authenticated:
        cart_item = Cart.objects.filter(user=user)
        for i in cart_item:
            cart_quantity += i.quantity
    context = {
        'all_product': all_product,
        'categories': categories,
        'cart_quantity': cart_quantity,
    }
    return render(request, 'allcategories.html', context)


def ProductDetail(request, id):
    product = Product.objects.filter(id=id)
    single_product = Product.objects.get(id=id)
    prod_img = Product_Image.objects.filter(product_id=id)
    off_percentage = 0
    if single_product.discounted_price:
        discount_cost = single_product.price - single_product.discounted_price
        off_percentage = (discount_cost * 100) / single_product.price
    product_discount_percentage = round(off_percentage)
    review = Review.objects.filter(product=single_product)
    p = product.first()
    cart_quantity = 0
    item_already_in_cart = False
    user = request.user
    if user.is_authenticated:
        item_already_in_cart = Cart.objects.filter(
            Q(product=p.id) & Q(user=request.user)).exists()
        cart_item = Cart.objects.filter(user=user)
        for i in cart_item:
            cart_quantity += i.quantity
    context = {
        'reviews': review,
        'cart_quantity': cart_quantity,
        'product': product,
        'single_product': single_product,
        'product_discount_percentage': product_discount_percentage,
        'prod_img': prod_img,
        'item_already_in_cart': item_already_in_cart
    }
    return render(request, 'product_detail.html', context)


class CustomerRegistration(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        context = {
            'form': form,
        }
        return render(request, 'registration.html', context)

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Congratulations!! Registered Successfully.')
            return redirect('login')
        context = {
            'form': form,
        }
        return render(request, 'registration.html', context)


class MyProfile(View):
    def get(self, request):
        u_form = MyUserProfileForm(instance=request.user)
        p_form = MyProfileForm(instance=request.user.customer)

        cart_quantity = 0
        user = request.user
        if user.is_authenticated:
            cart_item = Cart.objects.filter(user=user)
            for i in cart_item:
                cart_quantity += i.quantity
        context = {
            'u_form': u_form,
            'p_form': p_form,
            'cart_quantity': cart_quantity,
        }
        return render(request, 'profile.html', context)

    def post(self, request):
        u_form = MyUserProfileForm(request.POST, instance=request.user)
        p_form = MyProfileForm(request.POST, request.FILES,
                               instance=request.user.customer)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(
                request, 'Congratulations!! Profile Updated Successfully.')
            return redirect('profile')

        cart_quantity = 0
        user = request.user
        if user.is_authenticated:
            cart_item = Cart.objects.filter(user=user)
            for i in cart_item:
                cart_quantity += i.quantity
        context = {
            'u_form': u_form,
            'p_form': p_form,
            'cart_quantity': cart_quantity,
        }
        return render(request, 'profile.html', context)


def Add_to_cart(request):
    if request.method == "GET":
        prod_size = request.GET.get('size')
        prod_id = request.GET.get('prod_id')
        product = Product.objects.get(id=prod_id)
        qty = request.GET.get('qty')
        if qty == '0':
            qty = 1
        quantity = qty
        Cart(user=request.user, product=product,
             quantity=quantity, prod_size=prod_size).save()
        return redirect('product_detail', id=prod_id)


@login_required(login_url='/accounts/login/')
def BuyNow(request):

    prod_id = request.GET.get('prod_id')
    product = Product.objects.get(id=prod_id)
    size = request.GET.get('size')
    user = request.user
    qty = 1
    cart_item = Cart.objects.filter(user=user)

    if request.method == "GET":

        # Handle checkout forms......
        u_form = MyUserProfileForm(instance=request.user)
        p_form = MyProfileForm(instance=request.user.customer)
        form = PaymentOptionForm()

        # Handle cart total quantity......
        cart_quantity = 0
        if user.is_authenticated:
            for i in cart_item:
                cart_quantity += i.quantity

        # handle item price......
        amount = 0
        shipping_amount = 70
        total_amount = 0
        if product:
            if product.discounted_price:
                item_price = product.discounted_price
            else:
                item_price = product.price
            tempamount = qty * item_price
            amount += tempamount

        context = {
            'form': form,
            'u_form': u_form,
            'p_form': p_form,
            'product': product,
            'qty': qty,
            'cart_quantity': cart_quantity,
            'amount': amount,
            'total_amount': amount + shipping_amount,
            'shipping_amount': shipping_amount,
        }
        return render(request, 'checkout.html', context)

    if request.method == "POST":

        # Handle checkout forms......
        u_form = MyUserCheckoutForm(
            request.POST, instance=request.user)
        p_form = MyCheckoutForm(
            request.POST, instance=request.user.customer)
        form = PaymentOptionForm(request.POST)

        # Handle cash on delivery payment option......
        if u_form.is_valid() and p_form.is_valid():
            payment_option = request.POST.get('payment_option')
            if payment_option == 'Cash on delivery':
                product_order = Order.objects.filter(
                    product=product, size=size).first()
                if product_order:
                    if product_order.size == size:
                        product_order.quantity += qty
                        product_order.save()
                        return render(request, 'success.html')
                    else:
                        order = Order(user=user, customer=user.customer, product=product,
                                      quantity=qty, payment_option=payment_option, size=size)
                        order.save()
                        u_form.save()
                        p_form.save()
                        return render(request, 'success.html')
                else:
                    order = Order(user=user, customer=user.customer, product=product,
                                  quantity=qty, payment_option=payment_option, size=size)
                    order.save()
                    u_form.save()
                    p_form.save()
                    return render(request, 'success.html')

            # Handle paypal payment option......
            elif payment_option == 'Paypal':
                messages.warning(
                    request, 'Selected payment option not available now, Please select another payment option. !!')
                return redirect('buyNow', id=prod_id)

            # Handle stripe payment option......
            elif payment_option == 'Stripe':
                messages.warning(
                    request, 'Selected payment option not available now, Please select another payment option. !!')
                return redirect('buyNow', id=prod_id)

            # Handle no payment option selected......
            else:
                messages.warning(
                    request, 'No payment option selected, Please select a payment option. !!')
                return redirect('buyNow', id=prod_id)

        # Handle cart total quantity......
        cart_quantity = 0
        if user.is_authenticated:
            for i in cart_item:
                cart_quantity += i.quantity

        context = {
            'form': form,
            'u_form': u_form,
            'p_form': p_form,
        }
        return render(request, 'checkout.html', context)


@login_required(login_url='/accounts/login/')
def CartItem(request):

    # Handle delete a cart product item......
    if request.user.is_authenticated:
        if request.method == "GET":
            item_remove_id = request.GET.get('remove_id')
            try:
                c = Cart.objects.get(
                    Q(product=item_remove_id) & Q(user=request.user))
                c.delete()
            except Cart.DoesNotExist:
                pass

        # Handle total quantity of cart......
        cart_quantity = 0
        c_len = 0
        user = request.user
        cart_item = Cart.objects.filter(user=user).order_by('-id')
        for i in cart_item:
            cart_quantity += i.quantity

        # Handle all products length of cart......
        ci_len = len(cart_item)

        # Handle amount of cart products......
        amount = 0
        shipping_amount = 70
        total_amount = 0
        for p in cart_item:
            if p.product.discounted_price:
                item_price = p.product.discounted_price
            else:
                item_price = p.product.price
            tempamount = p.quantity * item_price
            amount += tempamount
        context = {
            'c_len': c_len,
            'ci_len': ci_len,
            'cart_item': cart_item,
            'cart_quantity': cart_quantity,
            'amount': amount,
            'total_amount': amount + shipping_amount,
            'shipping_amount': shipping_amount,
        }
        return render(request, 'cart_item.html', context)


def Plus_Minus_Item(request):
    if request.method == "GET":
        if request.GET.get('plus_id'):
            plus_id = request.GET.get('plus_id')
            c = Cart.objects.get(
                Q(product=plus_id) & Q(user=request.user))
            c.quantity += 1
            c.save()
            cart_item = Cart.objects.filter(user=request.user)
            amount = 0
            shipping_amount = 70
            total_amount = 0
            if cart_item:
                for p in cart_item:
                    if p.product.discounted_price:
                        item_price = p.product.discounted_price
                    else:
                        item_price = p.product.price
                    tempamount = p.quantity * item_price
                    amount += tempamount

                data = {
                    'quantity': c.quantity,
                    'amount': amount,
                    'total_amount': amount + shipping_amount
                }
                return JsonResponse(data)

        elif request.GET.get('minus_id'):
            minus_id = request.GET.get('minus_id')
            c = Cart.objects.get(
                Q(product=minus_id) & Q(user=request.user))
            c.quantity -= 1
            c.save()
            cart_item = Cart.objects.filter(user=request.user)
            amount = 0
            shipping_amount = 70
            total_amount = 0
            if cart_item:
                for p in cart_item:
                    if p.product.discounted_price:
                        item_price = p.product.discounted_price
                    else:
                        item_price = p.product.price
                    tempamount = p.quantity * item_price
                    amount += tempamount

                data = {
                    'quantity': c.quantity,
                    'amount': amount,
                    'total_amount': amount + shipping_amount
                }
                return JsonResponse(data)


class Checkout(View):
    def get(self, request):
        user = request.user
        cart_item = 0
        item = 0
        cart_item = Cart.objects.filter(user=user).order_by('-id')
        item = len(cart_item)
        if item >= 1:

            # Handle checkout forms......
            u_form = MyUserProfileForm(instance=request.user)
            p_form = MyProfileForm(instance=request.user.customer)
            form = PaymentOptionForm()

            # Handle cart total quantity......
            cart_quantity = 0
            if user.is_authenticated:
                for i in cart_item:
                    cart_quantity += i.quantity

            # handle item price......
            amount = 0
            shipping_amount = 70
            total_amount = 0
            for p in cart_item:
                if p.product.discounted_price:
                    item_price = p.product.discounted_price
                else:
                    item_price = p.product.price
                tempamount = p.quantity * item_price
                amount += tempamount

            context = {
                'form': form,
                'u_form': u_form,
                'p_form': p_form,
                'cart_item': cart_item,
                'cart_quantity': cart_quantity,
                'amount': amount,
                'total_amount': amount + shipping_amount,
                'shipping_amount': shipping_amount,
            }
            return render(request, 'checkout.html', context)
        else:
            redirect('home')
        return redirect('home')

    def post(self, request):
        user = request.user
        cart_item = Cart.objects.filter(user=user)

        # Handle checkout forms......
        u_form = MyUserCheckoutForm(request.POST, instance=request.user)
        p_form = MyCheckoutForm(
            request.POST, instance=request.user.customer)
        form = PaymentOptionForm(request.POST)

        # Handle cash on delivery payment option......
        if u_form.is_valid() and p_form.is_valid():
            payment_option = request.POST.get('payment_option')
            if payment_option == 'Cash on delivery':
                for ci in cart_item:
                    product_order = Order.objects.filter(
                        product=ci.product).first()
                    if product_order:
                        product_order.quantity += ci.quantity
                        product_order.save()
                        ci.delete()
                    else:
                        order = Order(user=user, customer=ci.user.customer, product=ci.product,
                                      quantity=ci.quantity, size=ci.prod_size, payment_option=payment_option)
                        order.save()
                        ci.delete()
                u_form.save()
                p_form.save()
                return render(request, 'success.html')

            # Handle paypal payment option......
            elif payment_option == 'Paypal':
                messages.warning(
                    request, 'Selected payment option not available now, Please select another payment option. !!')
                return redirect('checkout')

            # Handle stripe payment option......
            elif payment_option == 'Stripe':
                messages.warning(
                    request, 'Selected payment option not available now, Please select another payment option. !!')
                return redirect('checkout')

            # Handle no payment option selected......
            else:
                messages.warning(
                    request, 'No payment option selected, Please select a payment option. !!')
                return redirect('checkout')

        # Handle cart total quantity......
        cart_quantity = 0
        if user.is_authenticated:
            for i in cart_item:
                cart_quantity += i.quantity

        context = {
            'form': form,
            'u_form': u_form,
            'p_form': p_form,
        }
        return render(request, 'checkout.html', context)


@login_required(login_url='/accounts/login/')
def Orders(request):
    user = request.user
    cart_item = Cart.objects.filter(user=user)
    orders = Order.objects.filter(user=user).order_by('-id')

    # Handle cart total quantity......
    cart_quantity = 0
    if user.is_authenticated:
        for i in cart_item:
            cart_quantity += i.quantity

    # Handle delete order from orders......
    if request.method == "GET":
        delete_id = request.GET.get('delete_id')
        try:
            delete_order = Order.objects.filter(
                Q(user=user) & Q(product=delete_id))
            delete_order.delete()
        except Order.DoesNotExist:
            pass

    # Handle cancel order from orders......
    if request.method == "GET":
        cancel_id = request.GET.get('cancel_id')
        try:
            cancel_order = Order.objects.get(
                Q(user=user) & Q(product=cancel_id))
            cancel_order.status = 'Cancelled'
            cancel_order.save()
        except Order.DoesNotExist:
            pass

    context = {
        'orders': orders,
        'cart_quantity': cart_quantity,
    }
    return render(request, 'orders.html', context)


def Search(request):

    # Handle search......
    query = request.GET.get('query', '').lower()
    if len(query) > 78:
        search_products = Product.objects.none()

    title_Search = Product.objects.filter(title__icontains=query)
    description_search = Product.objects.filter(
        description__icontains=query)
    brand_search = Product.objects.filter(brand__icontains=query)
    search_products = title_Search.union(
        description_search, brand_search)

    # Handle pagination......
    all_product = Paginator(search_products, 2)
    page = request.GET.get('page')
    try:
        product = all_product.page(page)
    except PageNotAnInteger:
        product = all_product.page(1)
    except EmptyPage:
        product = all_product.page(all_product.num_pages)

    if search_products.count() == 0:
        messages.warning(
            request, 'No search results found, Please refine your query. !!')

    # Handle cart total quantity......
    user = request.user
    cart_item = Cart.objects.filter(user=user)
    cart_quantity = 0
    if user.is_authenticated:
        for i in cart_item:
            cart_quantity += i.quantity

    context = {
        'product': product,
        'query': query,
        'cart_quantity': cart_quantity
    }
    return render(request, 'search.html', context)


def Review_rate(request):
    if request.method == "GET":
        prod_id = request.GET.get('prod_id')
        product = Product.objects.get(id=prod_id)
        comment = request.GET.get('comment')
        rate = request.GET.get('rate')
        user = request.user
        Review(user=user, product=product, comment=comment, rate=rate).save()
        return redirect('product_detail', id=prod_id)
