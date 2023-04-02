from django.shortcuts import render,redirect
from.models import Order,OrderItem
from product.models import Coupon
from django.contrib import messages
from django.contrib import messages
from django.http import HttpResponseRedirect
from order.models import ReviewRating
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.




def orderlist(request):
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    


    orders = Order.objects.all().order_by('-id')
    

    # Filter orders based on minimum and maximum price
    if min_price and max_price:
        orders = orders.filter(payment__grand_total__gte=min_price, payment__grand_total__lte=max_price)
    elif min_price:
        orders = orders.filter(payment__grand_total__gte=min_price)
    elif max_price:
        orders = orders.filter(payment__grand_total__lte=max_price)

    context = {
        'orders': orders,
        'items': OrderItem.objects.all()
    }
    
    return render(request,'admin/orderlist.html', context)


def coupon_list(request):
    context={
        'coupon':Coupon.objects.all()
    }

    return render(request,"admin/coupon.html",context)


def add_coupon(request):
    if request.method=='POST':
        coupon_name=request.POST.get('coupon_code')
        discount_price=request.POST.get('discount_price')
        min_amount=request.POST.get('min_amount')
        
        Coupon.objects.create(
            coupon_code=coupon_name,
            min_amount=min_amount, 
           discount_price=discount_price, 
        
            )
        messages.success(request,f'{coupon_name} created successfully')
        return redirect(coupon_list)
    else:
        return redirect(coupon_list)







def delete_coupon(request):
    if request.method=='POST':
        coupon_id=request.POST.get('coupon_id')
        
        try:
            coupon=Coupon.objects.get(id=coupon_id)
            coupon.delete()
            messages.success(request,f'deleted{coupon}successfully')
            return redirect(coupon_list)
        except: 
            messages.error(request, f'Invalid coupon ID: {coupon_id}')
            return redirect(coupon_list)
    else:
        messages.error(request,f'something went wrong')
        return redirect(coupon_list)
    
   


def order_items(request, id):

    try:

        order = Order.objects.get(id=id)

        order_items = OrderItem.objects.filter(order=order).order_by('id')
        

        print(order_items)


        return render(request,'admin/order_items.html', {'order_items' : order_items})
    
    
    except:

        messages.error(request, 'Oops!Something gone wrong')

        return redirect(orderlist)
    


def status_update(request, id):

    try:

        order_item = OrderItem.objects.get(id=id)
        print(order_item.user.username)

        if request.method == 'POST':

            status = request.POST['status']

            order_item.order_status = status

            order_item.save()



            current_user = order_item.user
            print(current_user)
            subject = f'{order_item} {order_item.order_status}'

            if current_user is not None:
                    mess = f'Hello\t{current_user.username}.\nYour {order_item} has been {order_item.order_status},track your order status in our website.\nThank you!'
            else:
                mess = 'Your order status has been updated.\nThank you!'
            send_mail(
                        subject,
                        mess,
                        settings.EMAIL_HOST_USER,
                        [current_user.email],
                        fail_silently = False
                     )

            messages.success(request, 'Status updated successfully')

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        

    except OrderItem.DoesNotExist:

        messages.error(request, 'Oops!Something gone wrong')
        
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    

def coupon_status(request, id):

    try:

        coupon = Coupon.objects.get(id=id)

        if coupon.is_expired:

            coupon.is_expired = False

            coupon.save()

            messages.success(request, f'Coupon {coupon} activated succesfully')

            return redirect(coupon_list)
        
        else:

            coupon.is_expired = True

            coupon.save()

            messages.success(request, f'Coupon {coupon} deactivated succesfully')

            return redirect(coupon_list)
    except Coupon.DoesNotExist:

        messages.error(request, 'Oops!Something gone wrong')
        
        return redirect(coupon_list)
    




def review_management(request):
    reviews = ReviewRating.objects.all().order_by('-id')
    return render(request, 'admin/review.html',{'reviews' : reviews})




def remove_review(request, id):
    try:
        review = ReviewRating.objects.get(id=id)
        review.delete()
        messages.success(request,'Review removed succesfully')
        return redirect(review_management)
    
    
    except ReviewRating.DoesNotExist:
        messages.warning(request, 'Oops!Something went wrong')
        return redirect(review_management)
    