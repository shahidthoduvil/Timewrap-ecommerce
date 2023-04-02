


from order.models import Order,OrderItem

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

