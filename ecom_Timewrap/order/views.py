from django.shortcuts import render,redirect
from product.models import Cart,CartItem
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseBadRequest
from django.contrib import messages
from.models import OrderItem,Order,Payment,ReviewRating
from.models import Address
from django.utils import timezone
import razorpay
from django.conf import settings
from.form import ReviewForm
from django.core.mail import send_mail




# Create your views here.

def success_page(request):
    try:
        order_id = request.GET.get('razorpay_order_id') 
        print('Order id = ',order_id)
        cart = Cart.objects.get(user=request.user,razor_pay_order_id=order_id)

        # Payment details storing
        user = request.user
        transaction_id = request.GET.get('razorpay_payment_id')
        cart_total = cart.get_cart_total()
        tax = cart.get_tax()
        grand_total = cart.get_grand_total()
        if cart.coupon:
            coupon_discount = cart.coupon.discount_price
        else:
            coupon_discount = 0 
    
        
        payment = Payment.objects.create(
            user=user, transaction_id=transaction_id, cart_total=cart_total, tax=tax, grand_total=grand_total,discount=coupon_discount)
        payment.save()

        # Creating the order in Order table
        try:
            delivery_address = Address.objects.get(user=request.user,default=True)
        except Address.DoesNotExist:
            messages.error(request,"select an address")
            return redirect('checkout')

        order = Order.objects.create(
            order_id=order_id, user=user, delivery_address=delivery_address, payment=payment)

        # Storing ordered products in OrderItem table
        order_items = CartItem.objects.filter(cart=cart)
        for item in order_items:
            item.product.stock -= item.quantity
            item.product.save()

            ordered_item = OrderItem.objects.create(
                user=user, order=order, product=item.product, item_price=item.get_product_price(), quantity=item.quantity, item_total=item.get_sub_total())
            ordered_item.save()
            if item.variant:
                ordered_item.variant = item.variant.color.color_name
                ordered_item.save()
        # Deleting the cart once it is ordered/paid

        cart.is_paid = False
        cart.delete()
        context={
            'order_id':order_id
        }
    except:
        messages.error(request, 'Oops!Something gone wrong')
        
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    

    return render(request,"user_side/success_page.html",context)

  
def order_details(request,order_id):
    try:
        order = Order.objects.get(uid=order_id)
        order_items = OrderItem.objects.filter(order=order)
        print(order_items)
    except:
        pass 
    return render(request, 'user_side/order_details.html', {'order_items' : order_items})


def order_tracking(request, item_id):
    current_date = timezone.now()
    item = OrderItem.objects.get(id=item_id)

    context = {
        'item' : item,
        'current_date' : current_date
    }
    return render(request,'user_side/order_tracking.html',context)

def order_list(request):
    orders = Order.objects.filter(user=request.user,)
    return render(request, 'user_side/order_list.html', {'orders' : orders})


def invoice(request,order_id):
    try:
        order = Order.objects.get(uid=order_id,user=request.user)
        print(order)

        order_items = OrderItem.objects.filter(order=order)

        context = {
            'order' : order,
            'order_items' : order_items,
        }
    except:
        messages.error(request, 'Oops!Something gone wrong')
        
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    


    return render(request,"user_side/invoice.html",context)


def refund(request):
    return render(request,"user_side/refund.html")


def cancel_order(request, item_id=None, order_id=None):



        client = razorpay.Client(auth=(settings.KEY, settings.SECRET))

        order = Order.objects.get(user=request.user, order_id=order_id)

        payment_id = order.payment.transaction_id

        item = OrderItem.objects.get(order=order, id=item_id)

        item_amount = item.item_total 

 
        

        refund = client.payment.refund(payment_id,{'amount':item_amount})

        if refund is not None:

            item.order_status = 'Refunded'
            item.product.stock += item.quantity
            item.save()


            current_user = request.user
            subject = "Refund succesfull!"
            mess = f'Greetings {current_user.username}.\nYour refund for the product {item} of order: {order.order_id} has been succesfully generated. \nThank you for shopping with us!'
            send_mail(
                subject,
                mess,
                settings.EMAIL_HOST_USER,
                [current_user.email],
                fail_silently=False
            )

            item.product.save()
            return render(request, 'user_side/refund.html',{'order_id':order_id})
        else:
                return HttpResponse('Payment Not Captured')
  
        
 
    


        





def submit_review(request, product_id):
    if request.method == 'POST':
        try:
            review = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=review)  
            # Checks whether the review of the product by the user exists.
            # If exists, it will detect that review needs to be updated.
            # Else save it as a new review
            # If instance not passed, it will save it as a new review
            form.save()
            messages.success(request, 'Thank you! Your review has been updated')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            
            if form.is_valid():
                data = ReviewRating()
                data.review = form.cleaned_data['review']
                data.rating = form.cleaned_data['rating']
                data.user = request.user
                data.product_id = product_id
                data.save()
                messages.success(request, 'Thank you! Your review have been saved.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
    messages.error(request, 'Not success')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))