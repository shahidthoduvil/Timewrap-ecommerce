from django.shortcuts import render,redirect
from .models import Product,Category,Color,Cart,CartItem,Banner,Brand,Material,MultipleImg,Wishlist,WishlistItem,Variation,Coupon
from user.models import Address
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import MultiValueDictKeyError
import razorpay
from django.conf import settings
from order.models import ReviewRating

from django.contrib import messages

# Create your views here.

# ...............................................user side........................................................
@login_required(login_url='login')
def cart_summary(request):
   
    cart=None
    cart_items=None
    coupon_view=Coupon.objects.all()
    try:
        cart,_=Cart.objects.get_or_create(user=request.user,is_paid=False)
        

        cart_items=CartItem.objects.filter(cart=cart, is_active=True).order_by('id')
     
    except Exception as e:
       print(e)

    if request.method=='POST':
        coupon=request.POST.get('coupon')
        coupon_obj=Coupon.objects.filter(coupon_code__icontains=coupon)
        print(coupon_obj)
        if not coupon_obj.exists():
            messages.error(request,'invalid Coupon')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        if cart.coupon:
            messages.warning(request, 'Coupon Already applied')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        if cart.get_cart_total() < coupon_obj[0].min_amount:
            messages.warning(
                request, f'Total amount should be greater than ₹{coupon_obj[0].min_amount} excluding tax')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        if coupon_obj[0].is_expired:
             messages.warning(request, 'This coupon has expired')
             return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        cart.coupon = coupon_obj[0]
        cart.save()
    
        messages.success(request, 'Coupon Applied')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
    print('before')
    context = {'cart_items': cart_items, 'cart': cart,'coupon_view':coupon_view}
    print('after')

    return render(request,"user_side/cart.html",context)



@login_required(login_url='login')
def add_cart(request,product_id):
    product_variant = None
    try:
        variation = request.GET.get('variant')
        color = Color.objects.get(color_name=variation)
        product = Product.objects.get(id=product_id)

   
        user=request.user

      
        if color:
                product_variant = Variation.objects.get(product=product, color=color)
                cart, _ = Cart.objects.get_or_create(user=user, is_paid=False)
       

                is_cart_item = CartItem.objects.filter(
                cart=cart, product=product, variant=product_variant).exists()

      
       

        if is_cart_item:
                cart_item = CartItem.objects.get(
                cart=cart, product=product, variant=product_variant)
                if cart_item.quantity >= product.stock:

                    messages.warning(request, "Sorry, the product is out of stock.")
                    
                    return redirect(cart_summary)
                cart_item.quantity += 1
                cart_item.save()
                return redirect(cart_summary)

    
        else:
                cart_item = CartItem.objects.create(
                    product=product, quantity=1, cart=cart, variant=product_variant)
                cart_item.save()
                return redirect(cart_summary)

    except:
        pass

    return redirect(cart_summary)

    



# descrease the cart_item

def remove_cart(request,product_id, cart_item_id):
    
    try:
        product = Product.objects.get(id=product_id)
        cart = Cart.objects.get(user=request.user, is_paid=False)
        cart_item = CartItem.objects.get(
            product=product, id=cart_item_id, cart=cart)

        if cart_item.quantity > 1:
            
            cart_item.quantity -= 1
            cart_item.save()
        else:
          pass
    except:
        pass


    return redirect(cart_summary)

def remove_cart_item(request, product_id, cart_item_id):
    product = Product.objects.get(id=product_id)
    cart = Cart.objects.get(user=request.user, is_paid=False)
    cart_item = CartItem.objects.filter(
        product=product, id=cart_item_id, cart=cart)
    cart_item.delete()

    return redirect(cart_summary)



@login_required(login_url='login')
def add_wishlist(request,product_id):
    product = Product.objects.get(id=product_id)
    user=request.user
    wishlist,_ = Wishlist.objects.get_or_create(user=user)
    try:
         WishlistItem.objects.get(wishlist=wishlist, product=product)
    except:
        wishlist_item = WishlistItem.objects.create(
                product=product,
                wishlist=wishlist,
                quantity=1
            )
        
        
    return redirect('wishlist')

def remove_wishlistitem(request,product_id):
    product=Product.objects.get(id=product_id)
    user=request.user
    wishlist = Wishlist.objects.get(user=user)
    wishlist_item = WishlistItem.objects.get(product=product,wishlist=wishlist)
    wishlist_item.delete()
    return redirect('wishlist')


@login_required(login_url='login')
def wishlist(request,wishlist_items=None):
    try:
        wishlist = Wishlist.objects.get(user=request.user)
        wishlist_items = WishlistItem.objects.filter(wishlist=wishlist,is_active=True)
        print(wishlist_items)
        
    except ObjectDoesNotExist:
        pass

    context = {        
        'wishlist_items':wishlist_items,
    }
    
    return render(request, 'user_side/wishlist.html',context)


def product_info(request,product_slug):
 
    try:
       
        single_product=Product.objects.get(slug=product_slug)
        variants = Variation.objects.filter(product=single_product)
        review=ReviewRating.objects.filter(product=single_product)

        mult=MultipleImg.objects.filter(product = single_product)
        products=Product.objects.filter(is_available=True).order_by('id')
    except Exception as e:
        raise e
   

    context={'single_product':single_product,
             'mult':mult,
             'products':products,
             'variants': variants,
             'review':review,
    }
    if request.GET.get('variant'):
            color = request.GET.get('variant')
            variation = Color.objects.get(color_name=color)
            variant=Variation.objects.get(color=variation,product=single_product)
            print(variant)
            variant_price = single_product.get_product_price()
            context.update({
                'selected_variant': variant,
                'variant_price': variant_price,
                'color' : color,
                
              
                })

    return render(request,'user_side/product_info.html',context)




def store(request,category_slug=None,brand_slug=None,color_slug=None,material_slug=None):
    categories=None
    products=None

    if category_slug !=None:
        categories=get_object_or_404(Category,slug=category_slug)
        products=Product.objects.filter(category=categories,is_available=True)
        paginator=Paginator(products,2)
        page=request.GET.get('page')
        paged_products=paginator.get_page(page)
        product_count=products.count()


    elif brand_slug !=None:
        brand=get_object_or_404(Brand,slug=brand_slug)
        products=Product.objects.filter(brand=brand,is_available=True)
        paginator=Paginator(products,3)
        page=request.GET.get('page')
        paged_products=paginator.get_page(page)
        product_count=products.count()

    elif color_slug !=None:
        color=get_object_or_404(Color,slug=color_slug)
        products=Product.objects.filter(color=color,is_available=True)
        paginator=Paginator(products,3)
        page=request.GET.get('page')
        paged_products=paginator.get_page(page)
        product_count=products.count()

    elif material_slug !=None:
        material=get_object_or_404(Material,slug=material_slug)
        products=Product.objects.filter(material=material,is_available=True)
        paginator=Paginator(products,3)
        page=request.GET.get('page')
        paged_products=paginator.get_page(page)
        product_count=products.count()

    elif request.GET.get('min'):
            min = request.GET.get('min')
            max = request.GET.get('max')
            products = Product.objects.filter(price__range=(min, max))
            paginator=Paginator(products,3)
            page=request.GET.get('page')
            paged_products=paginator.get_page(page)
            product_count=products.count()

    elif request.GET.get('sortby'):
            sort = request.GET.get('sortby')
            if sort == 'newest':
                products = Product.objects.all().order_by('-created_date')
            elif sort == 'low-to-high':
                products = Product.objects.all().order_by('price')
            elif sort == 'high-to-low':
                products = Product.objects.all().order_by('-price')

            paginator=Paginator(products,3)
            page=request.GET.get('page')
            paged_products=paginator.get_page(page)
            product_count=products.count()
    
    
    else:
        products=Product.objects.filter(is_available=True).order_by('id')
        paginator=Paginator(products,3)
        page=request.GET.get('page')
        paged_products=paginator.get_page(page)
        product_count=products.count()


    context={

        'products':paged_products,
        'category':categories,
        # 'products':products,
        'product_count':product_count,
      
    }

    return render(request,'user_side/store.html',context)



def material(request):
     all_mat=Material.objects.all()
     return{'all_mat':all_mat}

def color(request):
     all_colr=Color.objects.all()
     return{'all_colr':all_colr}


def brand(request):
     all_band=Brand.objects.all()
     return{'all_band':all_band}












def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        products = Product.objects.none()  # define an empty queryset
        if keyword:
            products = Product.objects.order_by('-created_date').filter(
                Q(title__icontains=keyword) | Q(description__icontains=keyword)
            )
        product_count = products.count()
    else:
        products = Product.objects.none()
        product_count = 0

    context = {
        'products': products,
        'product_count': product_count,
    }

    return render(request, "user_side/store.html", context)



def banner_view(request):
    
    banner=Banner.objects.all()



    context={'banner':banner}
       
        

    return render(request,'user_side/home.html',context)

@login_required(login_url='login')
def checkout(request):
    current_user = request.user
    addresses = Address.objects.filter(user=current_user).order_by('id')
    coupon = Coupon.objects.all()

    payment = None
    cart=None
    cart_items=None
    # coupon  # define payment before the try block

    try:
        cart = Cart.objects.get(user=current_user, is_paid=False)
        cart_items = CartItem.objects.filter(cart=cart)
        client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
        payment = client.order.create({'amount': int(cart.get_grand_total()) * 100, 'currency': 'INR', 'payment_capture': 1})
    except:
        pass

    if payment is not None:  # check if payment is not None before using it
        cart.razor_pay_order_id = payment['id']
        cart.save()

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'address': addresses,
        'payment': payment,
        'coupon': coupon,
    }

    return render(request, "user_side/checkout.html", context)

    


def remove_coupon(request):
    try:
        cart = Cart.objects.get(user=request.user, is_paid=False)
        cart.coupon = None
        cart.save()
        messages.success(request, 'Coupon removed successfully')
    except:
        pass
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


    
   


def default_address(request,id):
    Address.objects.filter(user=request.user,default=True).update(default=False)
    Address.objects.filter(id=id,user=request.user).update(default=True)

    return redirect(checkout)









