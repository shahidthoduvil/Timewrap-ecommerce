from django.shortcuts import render
from product.models import Category,Product,Banner,Brand
from django.shortcuts import get_object_or_404

# Create your views here.


# .......................................................user side.......................................................
def home(request):
    
    products=Product.objects.all().filter(is_available=True)
    
    banner=Banner.objects.all()
    
    all_cat=Category.objects.all()
    all_brand=Brand.objects.all()
   
    




    context={'products':products,
             'banner':banner,
             'all_cat':all_cat,
             'all_brand':all_brand
              
             }
       
        

    return render(request,'user_side/home.html',context)

def category(request):
    all_cat=Category.objects.all()
    return{'all_cat':all_cat}




#.........................................................admin side..................................................