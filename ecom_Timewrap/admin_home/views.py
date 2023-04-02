from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib import messages,auth
from user.models import Account
from product.models import Product,Coupon,Category
from order.models import Order,OrderItem
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from admin_product.views import superadmin_check
from django.urls import resolve
from django.db.models import Sum, DateField

from datetime import datetime, timedelta
from django.db.models.functions import TruncDay, Cast
from order.models import Payment
import matplotlib.pyplot as plt
from django.http import HttpResponse
from io import BytesIO



# Create your views here.
@user_passes_test(superadmin_check)
def admin_home(request):
  
    user = Account.objects.all().count()

    product = Product.objects.all().count()

    category = Category.objects.all().count()

    coupon = Coupon.objects.all().count()

    order = Order.objects.all().count()

    item = OrderItem.objects.all()



    today = datetime.today()
    date_range = 7

    # Get the date 7 days ago
    four_days_ago = today - timedelta(days=date_range)
    print("======================================================")

    #filter orders based on the date range
    payments = Payment.objects.filter(paid_date__gte=four_days_ago, paid_date__lte=today) 
    

    # Getting the sales amount per day

    sales_by_day = payments.annotate(day=TruncDay('paid_date')).values('day').annotate(total_sales=Sum('grand_total')).order_by('-day')

    # Getting the dates which sales happpened

    sales_dates = Payment.objects.annotate(sale_date=Cast('paid_date', output_field=DateField())).values('sale_date').distinct()
    
    
    context = {

        'user': user,
        'item': item,
        'category': category,
        'product': product,
        'coupon': coupon,
        'order': order,
        'sales_by_day' : sales_by_day,
        'sales_dates' :sales_dates,
    }
    return render(request,'admin_side/admin_home.html',context)


def admin_login(request):

    if request.method=='POST':
        email=request.POST['email']
        u_password=request.POST['password']

        print(email, u_password)

        user=authenticate(email=email,password=u_password)
        
        if user is not None:
            if user.is_superadmin:
                auth.login(request,user)
                return redirect(admin_home)
            else:
                messages.info(request,'you are not admin')
                return redirect(admin_login)
        else:
            messages.info(request,'invalid login credential')
            return redirect(admin_login)
    else:
        return render(request,"admin_side/admin_login.html") 
    

def admin_logout(request):
    auth.logout(request)
    return redirect(admin_login)






def my_bar_chart_view(request):
    

    products_1000 = Product.objects.filter(price__range=(1, 999))
    count = 0
    for product in products_1000:
        count+=1

    products_1000_2000 = Product.objects.filter(price__range=(1000, 1999))
    count1 = 0
    for product in products_1000_2000:
        count1+=1

    products_2000_3000 = Product.objects.filter(price__range=(2000, 2999))
    count2 = 0
    for product in products_2000_3000:
        count2+=1

    products_3000_4000 = Product.objects.filter(price__range=(3000, 4000))
    count3 = 0
    for product in products_3000_4000:
        count3+=1



    x_values = ['1000', '2000', '3000', '4000']
    y_values = [count, count1, count2, count3]

    # Create bar chart
    plt.bar(x_values, y_values)

    # Set title and labels for x and y axis
    plt.title("Bar Chart")
    plt.xlabel("Price")
    plt.ylabel("Number of Products")

    # Save the chart as a PNG file
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Serve the file as a HTTP response
    response = HttpResponse(buffer, content_type='image/png')
    response['Content-Disposition'] = 'attachment; filename="my_bar_chart.png"'
    return response


