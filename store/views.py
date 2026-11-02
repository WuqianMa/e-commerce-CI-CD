from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from .models import *
from django.http import JsonResponse
import json 
import datetime
from .utils import cookieCart,cartData,guestOrder



def frontpage(request):
    context={}
    return render(request,'store/frontpage.html',context)


def blog(request):
    posts=Post.objects.all()
    context={'posts':posts}
    return render(request,'store/blog.html',context)


def store(request):

    data=cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items'] 

    products = Product.objects.all()


    context={'products':products,'cartItems':cartItems}
    return render(request,'store/store.html',context)

def affiliate(request):
    data=cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items'] 

    links = amazonlink.objects.all()
    context={'links':links,'cartItems':cartItems}
    return render(request,'store/amazon.html',context)



def cart(request):

    data=cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items'] 

    context = {'items':items,'order':order,'cartItems':cartItems}
    return render(request,'store/cart.html', context)

def checkout(request):
    data=cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items'] 

    context = {'items':items,'order':order,'cartItems':cartItems}
    return render(request,'store/checkout.html', context)


@require_POST
def updateItem(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Login required"}, status=401)
    try:
        data = json.loads(request.body)
        product_id = int(data["productId"])
        action = data["action"]
    except (ValueError, TypeError, KeyError, json.JSONDecodeError):
        return JsonResponse({"error": "Invalid request payload"}, status=400)

    if action not in ("add", "remove"):
        return JsonResponse({"error": "Unsupported cart action"}, status=400)

    try:
        customer = request.user.customer
    except Customer.DoesNotExist:
        return JsonResponse({"error": "Customer profile missing"}, status=400)

    product = get_object_or_404(Product, pk=product_id)
    order, _ = Order.objects.get_or_create(customer=customer, complete=False)
    order_item, _ = OrderItem.objects.get_or_create(order=order, product=product)
    order_item.quantity += 1 if action == "add" else -1

    if order_item.quantity <= 0:
        order_item.delete()
    else:
        order_item.save(update_fields=["quantity"])
    return JsonResponse({"message": "Cart updated"})


@require_POST
def processOrder(request):
    # The original demo did not verify any payment with the provider.
    # Do not claim a paid order until server-side verification exists.
    return JsonResponse(
        {"error": "Demo checkout only; payment processing is disabled."},
        status=501,
    )
