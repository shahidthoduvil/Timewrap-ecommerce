from django.shortcuts import render, redirect
from product.models import Banner, Category, Product, Brand, Material,MultipleImg,Color,Variation,Coupon
from order.models import Order,OrderItem
from user.models import Account
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib import messages
from django.http import HttpResponse,HttpResponseBadRequest
from django.contrib.auth.decorators import user_passes_test


# Create your views here.

def superadmin_check(user):
    if user.is_authenticated:
        return user.is_superadmin


def list_product(request):

    product_dict = {

        'pro': Product.objects.all(),
        'cat': Category.objects.all(),
        'band': Brand.objects.all(),
        'material': Material.objects.all(),
        'colr': Color.objects.all(),

    }
    
 
    return render(request, 'admin_side/list_product.html', product_dict)



def product_edit(request, id):



    pro_image=''
    if request.method == 'POST':
        pro_name = request.POST['product_name']
        pro_color = request.POST['product_color']
        slug = request.POST['slug']
        pro_category = request.POST['product_category']
        pro_brand = request.POST['product_brand']
        pro_material = request.POST['product_material']
        pro_description = request.POST['product_description']
        pro_specification = request.POST['product_specification']
        pro_price = request.POST['product_price']
       
        pro_stock = request.POST['product_stock']

        check=[int(pro_price),int(pro_stock)]
        for c in check:
            if c < 0:
                
                messages.error(request,'entered value is invalid')
                return redirect(product_edit)
            else:
                pass

     

        category_instance = Category.objects.get(id=pro_category)
       
        if not pro_color:

            messages.info(request,'color is not provided')
            return redirect(list_product)
    #
        else:
            try:
                color_instance = Color.objects.get(id=int(pro_color))
            except (ValueError, Color.DoesNotExist):
                messages.error(request,'color is not a valid number')
                return redirect(list_product)
          
        
        brand_instance = Brand.objects.get(id=pro_brand)
        material_instance = Material.objects.get(id=pro_material)
        
        if not    pro_category or    pro_category.isspace() :
            messages.error(request, "category cannot be empty or contain only spaces.")
            return redirect(product_edit)
        
        if not  pro_brand or  pro_brand.isspace() :
            messages.error(request, "category cannot be empty or contain only spaces.")
            return redirect(product_edit)
     
        if not pro_material or pro_material.isspace() :
            messages.error(request, "category cannot be empty or contain only spaces.")
            return redirect(product_edit)
     
        if not pro_name or pro_name.isspace() :
            messages.error(request, "name cannot be empty or contain only spaces.")
            return redirect(product_edit)
     
        if not pro_description or pro_description.isspace() :
            messages.error(request, "description cannot be empty or contain only spaces.")
            return redirect(product_edit)
     
        if not pro_specification or pro_specification.isspace() :
            messages.error(request, "specification cannot be empty or contain only spaces.")
            return redirect(product_edit)
     
    


        
  
        try:
            update_product = Product.objects.get(id=id)
            pro_image = request.FILES['pro_image']
            update_product.image = pro_image
            update_product.save()
        except:
             pass
     
  
        update_product = Product.objects.filter(id=id)
        update_product.update(title=pro_name, slug=slug, color=color_instance, description=pro_description, price=pro_price,
                              stock=pro_stock, category=category_instance, brand=brand_instance, material=material_instance,
                              specification=pro_specification)
        return redirect(list_product)

    return render(request, "admin_side/list_product.html")

def add_product(request):
   
    product_dict = {

        'cat': Category.objects.all(),
        'band': Brand.objects.all(),
        'material': Material.objects.all(),
        # 'colr': Color.objects.all()
    }

    if request.method == 'POST':
   
        pro_name = request.POST['name']
    
        
        slug = request.POST['slug']

        pro_description = request.POST['description']

        pro_specification = request.POST['specification']

        pro_price = request.POST['price']
    
        pro_stock = request.POST['stock']

        check=[int(pro_price),int(pro_stock)]

        for c in check:
            if c < 0:
                
                messages.error(request,'entered value is invalid')
                return redirect(add_product)
            else:
                pass

      


        pro_category = request.POST['category']
          
        pro_material = request.POST['material']
        pro_brand = request.POST['brand']



        try:

            pro_image = request.FILES['image']

            
        except KeyError:
            pro_image = None
       
    
  
     
          
        
        category_instance = Category.objects.get(id=pro_category)
       
        # color_instance = Color.objects.get(id=pro_color)
       
        brand_instance = Brand.objects.get(id=pro_brand)
     
     
        material_instance = Material.objects.get(id=pro_material)

        products = Product.objects.all()

# Loop through each product and update the price and stock fields
        for product in products:
    # Validate the price and stock fields
            if product.price < 0:
        # Handle invalid input
             product.price = 0

            if product.stock < 0:
        # Handle invalid input
                product.stock = 0

    # Save the updated product to the database
        product.save()




        if not    pro_category or    pro_category.isspace() :
            messages.error(request, "category cannot be empty or contain only spaces.")
            return redirect(add_product)
        
        if not  pro_brand or  pro_brand.isspace() :
            messages.error(request, "category cannot be empty or contain only spaces.")
            return redirect(add_product)
     
        if not pro_material or pro_material.isspace() :
            messages.error(request, "category cannot be empty or contain only spaces.")
            return redirect(add_product)
     
        if not pro_name or pro_name.isspace() :
            messages.error(request, "name cannot be empty or contain only spaces.")
            return redirect(add_product)
     
        if not pro_description or pro_description.isspace() :
            messages.error(request, "description cannot be empty or contain only spaces.")
            return redirect(add_product)
     
        if not pro_specification or pro_specification.isspace() :
            messages.error(request, "specification cannot be empty or contain only spaces.")
            return redirect(add_product)
       

        product = Product.objects.create(
             title=pro_name, slug=slug, description=pro_description, price=pro_price, stock=pro_stock, image=pro_image, category=category_instance, brand=brand_instance, material=material_instance, specification=pro_specification)
        try:
          multi_images = request.FILES.getlist('images')
        except:
            pass


        for image in multi_images:
            MultipleImg.objects.create(product=product,img=image)


       # product.save()
        return redirect(list_product)

    return render(request, 'admin_side/add_product.html', product_dict)



def product_delete(request, id):
    del_pro = Product.objects.filter(id=id)
    del_pro.delete()

    return redirect(list_product)



def material(request):
    mater_edit = {

        'material': Material.objects.all(),
    }
    return render(request, "admin_side/material.html", mater_edit)


# material edit


@user_passes_test(superadmin_check)
def material_edit(request, id):

    mat_name = request.POST['ma_name']
    slug = request.POST['slug']


    if not mat_name or mat_name.isspace():
        messages.error(request, "Material name cannot be empty or contain only spaces.")
        return redirect(material)
    
    mat_update = Material.objects.filter(id=id)

    mat_update.update(material_name=mat_name, slug=slug)

    return redirect(material)

    # material add



def material_add(request):
    mat_name = request.POST['m_name']
    slug = request.POST['slug']

    if ' ' in mat_name.strip(): # check if mat_name contains spaces
        messages.error(request, "Material name cannot contain spaces.")
        return redirect(material)
    
    if not mat_name or mat_name.isspace():
        messages.error(request, "Material name cannot be empty or contain only spaces.")
        return redirect(material)
    
    if Material.objects.filter(slug=slug).exists():
        messages.error(request, f"A material with slug '{slug}' already exists.")
        return redirect(material)


    mat_add = Material.objects.create(material_name=mat_name, slug=slug)
    mat_add.save()

    return redirect(material)

# material delete


def material_delete(request, id):
    del_mat = Material.objects.filter(id=id)
    del_mat.delete()
    return redirect(material)


def color(request):
    color_dict = {
        'colr': Color.objects.all()
    }

    return render(request, "admin_side/color.html", color_dict)


# color_edit


def color_edit(request, id):
    colr_name = request.POST['col_name']
    slug = request.POST['slug']

    if not colr_name or colr_name.isspace():
        messages.error(request, "Color name cannot be empty or contain only spaces.")
        return redirect(color)
    color_update = Color.objects.filter(id=id)
    color_update.update(color_name=colr_name, slug=slug)
    return redirect(color)

# color_add

def color_add(request):
    c_name = request.POST['c_name']
    slug = request.POST['slug']

    if not c_name or c_name.isspace():
        messages.error(request, "Color name cannot be empty or contain only spaces.")
        return redirect(color)
    color_add = Color.objects.create(color_name=c_name, slug=slug)
    color_add.save()
    return redirect(color)


# color_delete


def color_delete(request, id):
    colr_del = Color.objects.filter(id=id)
    colr_del.delete()
    return redirect(color)


def brand(request):
    brand_dict = {
        'band': Brand.objects.all(),
    }

    return render(request, "admin_side/brand.html", brand_dict)


def brand_edit(request, id):
    band_image=None
  
    if request.method == 'POST':

        band_name = request.POST['b_name']
        slug = request.POST['slug']
        
       
        if not band_name or band_name.isspace():
            messages.error(request, "Brand name cannot be empty or contain only spaces.")
            return redirect(brand)

    
        try:
            
            band_update = Brand.objects.get(id=id)
            band_image = request.FILES['b_image']
            
            band_update.brand_image = band_image
            band_update.save()
        except:
             band_image=None
    

         

       
    
        band_update = Brand.objects.filter(id=id)
        band_update.update(brand_name=band_name, slug=slug)
        return redirect(brand)

    return render(request, "admin_side/brand.html")

# brand add


def brand_add(request):
    band_name=None
    band_name = request.POST['b_name']

     
       
    if not band_name or band_name.isspace():
            messages.error(request, "Brand name cannot be empty or contain only spaces.")
            return redirect(brand)
    

    try:
        band_image = request.FILES['b_image']
    except KeyError:
      band_image=None

    slug = request.POST['slug']

    band_add = Brand.objects.create(
        brand_name=band_name, brand_image=band_image, slug=slug)
    band_add.save()

    return redirect(brand)

# brand delete

def brand_delete(request, id):
    del_band = Brand.objects.filter(id=id)
    del_band.delete()
    return redirect(brand)

def banner(request):
    banner = Banner.objects.all()
    context = {
        'banner': banner
    }

    return render(request, "admin_side/banner.html", context)



def banner_delete(request, id):
    del_ban = Banner.objects.filter(id=id)
    del_ban.delete()
    return redirect(banner)


def banner_add(request):
    bann_image=''
    bann_name = request.POST['b_name']
    bann_description = request.POST['b_description']
    try:
       bann_image = request.FILES['b_image']
    except:
        pass
    if not bann_name or bann_name.isspace() and bann_description or bann_description.isspace():
            messages.error(request, "Brand  cannot be empty or contain only spaces.")
            return redirect(banner)
    

    bann_add = Banner.objects.create(
        heading=bann_name, image=bann_image, description=bann_description)
    bann_add.save()

    return redirect(banner)


def banner_edit(request, id):
    bann_image=''
    if request.method == 'POST':

        bann_name = request.POST['b_name']
        bann_description = request.POST['b_description']

        if not bann_name or bann_name.isspace() and bann_description or bann_description.isspace() and bann_image or bann_image.isspace():
            messages.error(request, "Brand  cannot be empty or contain only spaces.")
            return redirect(banner)

        
        try:
           image_update = Banner.objects.get(id=id)
           bann_image = request.FILES['b_image']
           image_update.image = bann_image
           image_update.save()
        except:
           pass
      

        bann_update = Banner.objects.filter(id=id)
        bann_update.update(heading=bann_name, description=bann_description)
        return redirect(banner)
    else:
        return render(request, "admin_side/banner.html")




def color_variant(request):
    product=Product.objects.all()
    varaint=Variation.objects.all()
    colr=Color.objects.all()
    context={
        'product':product,
        'varaint':varaint,
        'colr':colr    
        }
    return render(request,"admin_side/color_variant.html",context)

def varaint_add(request):
    if request.method=='POST':
        color=request.POST['color']
        product=request.POST['product']
           
       
        

        product_instance=Product.objects.get(id=product)
        color_intance=Color.objects.get(id=color)
        variant=Variation.objects.create(color=color_intance,product=product_instance)
        variant.save()
        return redirect(color_variant)
    else:
        return render(request,"admin_side/color_variant.html")

from django.http import Http404


def variant_edit(request,id):

    if request.method=='POST':
        color = request.POST['edit_color']

        color_instance = Color.objects.get(id=color)

        update_variant = Variation.objects.filter(id=id)
        
        update_variant.update(color=color_instance)

        return redirect(color_variant)
    
    else:

        return render(request, "admin_side/color_variant.html")


def varaint_delete(request,id):
    del_var= Variation.objects.filter(id=id)
    del_var.delete()
    return redirect(color_variant)




