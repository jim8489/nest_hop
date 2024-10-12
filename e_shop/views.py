from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
import requests
from django.conf import settings
from django.contrib import messages
from userauths.models import User
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

AUTH_USER_MODEL = "userauths.User"





# Create your views here.
from e_shop.models import *
from userauths.forms import UserUpdateForm
from userauths.models import *
from django.template.loader import render_to_string
from taggit.models import Tag
from django.db.models import Count, Avg
from e_shop.forms import ProductReviewform
from django.contrib.auth.decorators import login_required

def index(request):
    #Product = product.objects.all().order_by("-id")
    Product = product.objects.filter(product_status="published", featured=True).order_by("-id")

    
    context = {
        "products": Product
    }
    
    return render(request, 'e_shop/index.html',context)

def product_list_view(request):
    Product = product.objects.filter(product_status="published")
    
    
    context = {
        "products": Product,
    }
    
    return render(request, 'e_shop/product-list.html',context)


def category_list_view(request):
    categories = Category.objects.all()
    
    context = {
        "categories": categories
    }
    
    return render(request, 'e_shop/category-list.html',context)

def category_product_list_view(request,cid): #with cid get product
    category = Category.objects.get(cid=cid)
    products = product.objects.filter(product_status="published", category=category)
    
    
    context = {
        "category": category,
        "products":products,
    }
    
    return render(request, 'e_shop/category-product-list.html',context)

def vendor_list_view(request):
    vendors = Vendor.objects.all()
    
    context = {
        "vendors": vendors
    }
    
    return render(request, 'e_shop/vendor-list.html',context)

def vendor_detail_view(request,vid):
    vendor = Vendor.objects.get(vid=vid)
    products = product.objects.filter(product_status="published", vendor=vendor)

    
    context = {
        "vendor": vendor,
        "products":products,
    }
    
    return render(request, 'e_shop/vendor-detail.html',context)

def product_detail_view(request,pid):
    Products = product.objects.get(pid=pid)
    products = product.objects.filter(category = Products.category).exclude(pid=pid)
    
    #getting all reviws
    reviews = ProductReview.objects.filter(Product=Products)#.order_by("-date")
    
    #getting average reviw
    average_rating = ProductReview.objects.filter(Product=Products).aggregate(rating = Avg("rating"))

    p_image = Products.p_images.all()    
    
    review_form = ProductReviewform()
    
    context = {
        "p": Products,
        "product": products,
        "p_image":p_image,
        "reviews": reviews,
        "review_form": review_form,
        "average_rating": average_rating,
    }
    
    return render(request, 'e_shop/product-detail.html',context)

def tag_list(request, tag_slug=None):
    products = product.objects.filter(product_status="published").order_by("-id")
    
    tag=None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])
        
        context = {
            "products": products,
            "tag": tag,

        }
    
    return render(request, 'e_shop/tag.html',context)

def ajax_add_review(request,pid):
    Product = product.objects.get(pk=pid)
    user = request.user
    
    review = ProductReview.objects.create(
        user = user,
        Product = Product,
        review = request.POST["review"],
        rating = request.POST["rating"],
    )
    
    context = {
        'user': user.username,
        'review': request.POST["review"],
        'rating': request.POST["rating"],
    }
    
    average_review = ProductReview.objects.filter(Product=Product).aggregate(rating = Avg("rating"))
    
    return JsonResponse(
        {
            'bool': True,
            'context': context,
            "average_review": average_review
        }
    )

    
    

def search_view(request):
    query = request.GET.get("q")
    products = product.objects.filter(title__icontains=query).order_by("-date")
    
    context = {
        "products": products,
        "query":  query
    }
    
    return render(request, 'e_shop/search.html', context)

def filter_product(request):
    categories = request.GET.getlist("category[]")
    vendors = request.GET.getlist("vendor[]")
    
    products = product.objects.filter(product_status="published").order_by("-id").distinct()
    
    if len(categories)>0:
        products = products.filter(category__id__in = categories).distinct()
         
    if len(vendors)>0:
        products = products.filter(vendor__id__in = vendors).distinct()
         
    data = render_to_string("e_shop/async/product-list.html", {"products": products})
    return JsonResponse({"data": data})

def add_to_cart(request):
    cart_product = {}
    
    cart_product[str(request.GET['id'])] = {
        'title': request.GET['title'],
        'qty': request.GET['qty'],
        'price': request.GET['price'],
        'image': request.GET['image'],
        'pid': request.GET['pid']
    }
    
    if 'cart_data_obj' in request.session:
        if str(request.GET['id'])in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
            
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
        
    else:
        request.session['cart_data_obj'] = cart_product
        
    return JsonResponse({"data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj'])})

def cart_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += float(item['qty']) * float(item['price'])
        return render(request, "e_shop/cart.html", {"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']),'cart_total_amount': cart_total_amount})
    else:
        return render(request, "e_shop/index.html")

def delete_product_from_cart(request):
    # Get the product ID to delete
    product_id = str(request.GET.get('id'))  # Use .get() to avoid KeyError if 'id' isn't present

    # Check if 'cart_data_obj' exists in session
    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']

        # Check if the product exists in the cart and delete it
        if product_id in cart_data:
            del cart_data[product_id]
            request.session['cart_data_obj'] = cart_data  # Save the updated cart back to the session

    # Recalculate the total cart amount
    cart_total_amount = 0
    totalcartitems = 0
    if 'cart_data_obj' in request.session:
        for item in request.session['cart_data_obj'].values():
            cart_total_amount += float(item['qty']) * float(item['price'])
        totalcartitems = len(request.session['cart_data_obj'])

    # Render the updated cart template
    context = render_to_string("e_shop/async/cart-list.html", {
        "cart_data": request.session.get('cart_data_obj', {}),
        'totalcartitems': totalcartitems,
        'cart_total_amount': cart_total_amount
    })

    # Return the updated cart data and total items in a JSON response
    return JsonResponse({"data": context, 'totalcartitems': totalcartitems})

def update_cart(request):
    # Get the product ID to delete
    product_qty = str(request.GET['qty'])
    product_id = str(request.GET.get('id'))  # Use .get() to avoid KeyError if 'id' isn't present

    # Check if 'cart_data_obj' exists in session
    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']
        cart_data[str(request.GET['id'])]['qty'] = product_qty

        # Check if the product exists in the cart and delete it
        if product_id in cart_data:
            request.session['cart_data_obj'] = cart_data  # Save the updated cart back to the session

    # Recalculate the total cart amount
    cart_total_amount = 0
    totalcartitems = 0
    if 'cart_data_obj' in request.session:
        for item in request.session['cart_data_obj'].values():
            cart_total_amount += float(item['qty']) * float(item['price'])
        totalcartitems = len(request.session['cart_data_obj'])

    # Render the updated cart template
    context = render_to_string("e_shop/async/cart-list.html", {
        "cart_data": request.session.get('cart_data_obj', {}),
        'totalcartitems': totalcartitems,
        'cart_total_amount': cart_total_amount
    })

    # Return the updated cart data and total items in a JSON response
    return JsonResponse({"data": context, 'totalcartitems': totalcartitems})

@login_required
def checkout_view(request):
    cart_total_amount = 0
    totalcartitems = 0
    if 'cart_data_obj' in request.session:
        for item in request.session['cart_data_obj'].values():
            cart_total_amount += float(item['qty']) * float(item['price'])
        totalcartitems = len(request.session['cart_data_obj'])
        
    return render(request, "e_shop/checkout.html",{
        "cart_data": request.session.get('cart_data_obj', {}),
        'totalcartitems': totalcartitems,
        'cart_total_amount': cart_total_amount
    })
    
def payment_completed_view(request):
    cart_total_amount = 0
    totalcartitems = 0
    if 'cart_data_obj' in request.session:
        for item in request.session['cart_data_obj'].values():
            cart_total_amount += float(item['qty']) * float(item['price'])
        totalcartitems = len(request.session['cart_data_obj'])
        
    return render(request, "e_shop/payment-completed.html",{
        "cart_data": request.session.get('cart_data_obj', {}),
        'totalcartitems': totalcartitems,
        'cart_total_amount': cart_total_amount
    })
def payment_failed_view(request):
    return render(request, "e_shop/payment-failed.html")
 

@login_required
def user_account_view(request):
    vendor = Vendor.objects.all()
    user = request.user

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('user-account')  # Redirect to the same page after saving
    else:
        form = UserUpdateForm(instance=user)  # Pre-fill form with current user data

    context = {
        'vendor': vendor,
        'user': user,
        'form': form,
    }

    return render(request, 'e_shop/user-account.html', context)

def contact(request):
    return render(request, 'e_shop/contact.html')

def deals(request):
    products = product.objects.filter(product_status="published")
    
    context = {
        "products":products
    }
    return render(request, 'e_shop/deals.html', context)




# views.py
def generate_bkash_token():
    url = f"{settings.BKASH_BASE_URL}/token/grant"
    headers = {
        'Content-Type': 'application/json',
        'password': settings.BKASH_PASSWORD,
        'username': settings.BKASH_USERNAME
    }
    payload = {
        'app_key': settings.BKASH_APP_KEY,
        'app_secret': settings.BKASH_APP_SECRET
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    # Log the response status and body for debugging
    print(f"bKash Token API Response Status Code: {response.status_code}")
    print(f"bKash Token API Response Body: {response.text}")

    if response.status_code == 200:
        return response.json().get('id_token', None)  # Use .get() to avoid KeyError
    else:
        error_message = response.json().get('statusMessage', 'Unknown error')
        print(f"Error generating token: {error_message}")
        return None

# views.py

def create_payment(request):
    #amount = request.POST.get('amount', '100')
    token = generate_bkash_token()
    
    if not token:
        return JsonResponse({'error': 'Failed to generate bKash token'})

    url = f"{settings.BKASH_BASE_URL}/payment/create"
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    payload = {
        "amount": '200',
        "currency": "BDT",
        "intent": "sale",
        "merchantInvoiceNumber": "INV1234"  # Invoice number can be dynamic
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        payment_data = response.json()
        return JsonResponse(payment_data)
    else:
        return JsonResponse({'error': 'Payment creation failed'})

# views.py

def execute_payment(request):
    payment_id = request.GET.get('paymentID', None)
    token = generate_bkash_token()
    
    if not payment_id or not token:
        return JsonResponse({'error': 'Missing paymentID or token'})

    url = f"{settings.BKASH_BASE_URL}/payment/execute/{payment_id}"
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    
    response = requests.post(url, headers=headers)
    
    if response.status_code == 200:
        payment_result = response.json()
        # Save the payment result in the database if necessary
        return JsonResponse(payment_result)
    else:
        return JsonResponse({'error': 'Payment execution failed'})

# views.py

def query_payment(request):
    payment_id = request.GET.get('paymentID', None)
    token = generate_bkash_token()
    
    if not payment_id or not token:
        return JsonResponse({'error': 'Missing paymentID or token'})

    url = f"{settings.BKASH_BASE_URL}/payment/query/{payment_id}"
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        payment_status = response.json()
        return JsonResponse(payment_status)
    else:
        return JsonResponse({'error': 'Failed to retrieve payment status'})
