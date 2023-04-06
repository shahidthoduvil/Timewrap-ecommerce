


from order.models import Order,OrderItem

from product.models import Wishlist, WishlistItem, Cart,CartItem

def revenue(request):
    reveneue=0
    tax=0
    total_revenue=0


    order=Order.objects.all()
    for order in order:
        tax +=order.payment.tax

    
    item=OrderItem.objects.all()
    for item in item:
        if item.order_status=='Delivered':
            total_revenue += item.item_total

    reveneue=total_revenue +tax
    return dict(total_revenue=reveneue)










def counter(request):
    wishlist_count = 0
    cart_count = 0
    if request.user.is_authenticated:
        try:
            wishlist = Wishlist.objects.get(user=request.user)
            wishlist_items = WishlistItem.objects.filter(wishlist=wishlist)

            for item in wishlist_items:
                wishlist_count += 1
        except Wishlist.DoesNotExist:
            pass

        try:
            cart = Cart.objects.get(user=request.user, is_paid=False)
            cart_items = CartItem.objects.filter(cart=cart)
            for item in cart_items:
                cart_count += 1
        except Cart.DoesNotExist:
            pass
    
    return dict(wishlist_count=wishlist_count,cart_count=cart_count)

