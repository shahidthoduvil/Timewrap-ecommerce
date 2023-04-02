from django.shortcuts import render,redirect

from django.contrib import messages,auth
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.contrib.auth.models import User,AbstractUser
from django.core.mail import send_mail
import random
from .models import UserOTP
from django.conf import settings
from .form import RegistrationForm
from .models import Account,Address
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from product.models import Cart,CartItem
from home.views import home

from .form import AddressForm





# Create your views here.


#................................................. user  side views..........................................................

def sign_up(request):
        
        if request.method=='POST':
             form=RegistrationForm(request.POST)
             if form.is_valid():
                first_name=form.cleaned_data['first_name']
                last_name=form.cleaned_data['last_name']
                phone_number=form.cleaned_data['phone_number']
                email=form.cleaned_data['email']
                password=form.cleaned_data['password']
                username=form.cleaned_data['username']
                user=Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password,phone_number=phone_number)
                user.save()
                #user activation

                current_site=get_current_site(request)
                mail_subject = 'Please activate your account'
                message = render_to_string('user_side/account_verification.html',{
                'user' : user,
                'domain' : current_site,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user),
                })
                to_email = email
                send_email = EmailMessage(mail_subject, message, to=[to_email])
                send_email.send()
                messages.success(request,'Thank you for registring with us,we have sent you a verification email to your email address.please verify it. ')
                
                return redirect('login')
                                 #  /?command=verfication&email='+email
                
        else:
             
          form=RegistrationForm()
        context={
             'form':form
        }
    
       
        return render(request,'user_side/sign_up.html',context)



def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active=True
        user.save()
        messages.success(request, 'congratulation Your account is activated.')
        return redirect('login')
    else:
        messages.error(request, 'invalid activation link')
        return redirect('sign_up')
  




   
def login(request):
    if request.user.is_authenticated:
        return redirect(home)
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request,user)
            return redirect(home)
        else:
            messages.error(request,'invalid login credentials')
            return redirect(login)
         
    return render(request,"user_side/login.html")

def otp_email(request):
    usr = None
    if request.method=='POST':
        get_otp = request.POST.get('otp')
        print(get_otp)
        if get_otp:
            get_usr = request.POST.get('email')
            try:
                usr = Account.objects.get(email=get_usr)
            except Account.DoesNotExist:
                messages.warning(request, f'Account with email {get_usr} does not exist.')
                return render(request, 'user_side/otp_email.html')
            otp_db = UserOTP.objects.filter(user=usr).last()
            print('++++++++',otp_db.otp)
            if int(get_otp) == otp_db.otp:

                usr.is_active = True
                auth.login(request,usr)

                return redirect('home')
                        
            else:
                messages.warning(request, f'You Entered a wrong OTP')
                return render(request, 'user_side/otp_login.html', {'otp': True, 'usr': usr})
           
        else:
            email = request.POST.get('email')
            try:
                usr = Account.objects.get(email=email)
            except Account.DoesNotExist:
                messages.warning(request, f'Account with email {email} does not exist.')
                return render(request, 'user_side/otp_email.html')

            usr_otp = random.randint(100000, 999999)
            UserOTP.objects.create(user=usr, otp=usr_otp)
            mess = f'Hello\t{usr},\nYour OTP to verify your account for timewrap is {usr_otp}\nThanks!'
            send_mail(
                     "welcome to timewrap E-commerce-Verify your Email",
                     mess,
                    settings.EMAIL_HOST_USER,
                    [usr.email],
                    fail_silently=False
                    )
            return render(request, 'user_side/otp_login.html', {'otp': True, 'usr': usr})
       
    else:
        return render(request, 'user_side/otp_email.html')



def otp_login(request):
    
    return render(request, 'user_side/otp_login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request,"you are logged out.")
    return redirect('home')





  



def reset_password(request):
    if request.method=='POST':
         email=request.POST['email']
         if Account.objects.filter(email=email).exists():
            user=Account.objects.get(email=email)
            current_site=get_current_site(request)
            mail_subject = 'RESET YOUR PASSWORD '
            message = render_to_string('user_side/reset_validation.html',{
            'user' : user,
            'domain' : current_site,
            'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
            'token' : default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request,'password reset email has been sent to your email address.')
            return redirect(login)
         else:
            messages.error(request,'Account does not exist') 
            return redirect(reset_password)
         
    return render(request, "user_side/reset_password.html")
    
def reset_validation(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid']= uid
        messages.success(request, 'please reset your password')
        return redirect('confirm_password')
    else:
        messages.error(request, 'link has been expired!')
     
   
        return redirect('login')



def confirm_password(request):
        if request.method=='POST':
            password=request.POST['password']
            confirm_password=request.POST['confirm_password']

            if password==confirm_password:
                uid=request.session.get('uid')
                user=Account.objects.get(pk=uid)
                user.set_password(password)
                user.save()
                messages.success(request,'password reset successful')
                return redirect(login)
            else:
                messages.error(request,'password do not match!')
                return redirect('confirm_password')
        else:
          return render(request, "user_side/confirm_password.html")

     
       

@login_required(login_url='login')
def profile(request):
 
    return render(request,"user_side/user_dashboard/profile.html")


def edit_profile(request,id):
        if request.method =='POST':
          first_name=request.POST['f_name']
          phone_number=request.POST['phone_number']
  

          edit_user=Account.objects.filter(id=id)
        
          edit_user.update(username=first_name,phone_number=phone_number)

          return redirect(profile)
       
        else:
            return render(request,"user_side/user_dashboard/edit_profile.html")

def dp_edit(request):
    user=request.user.id
    user=Account.objects.get(id=user)
    try:
        image=request.FILES['user_image']
        user.pic=image
        user.save()
    except:
        pass

    return redirect(profile)




def address_view(request):
        context={
        'address':Address.objects.filter(user=request.user)

    }
        return render(request,"user_side/user_dashboard/address.html",context)


def add_address(request):


    address = Address.objects.filter(user=request.user)
    if request.method == 'POST':

        print(address)
        
        form = AddressForm(request.POST)

        if form.is_valid():

            address = form.save(commit=False)

            address.user = request.user

            address.save()

            return redirect(address_view)
    else:

        form = AddressForm()
   

 
    return render(request,"user_side/user_dashboard/add_address.html",{'form':form})


def edit_address(request, id):

    address =Address.objects.get(id=id)
    if request.method == 'POST':

        form = AddressForm(request.POST, instance=address)

        if form.is_valid():

            form.save()

            return redirect(address_view)
    else:
         form = AddressForm(instance=address)
            
    return render(request, 'user_side/user_dashboard/edit_address.html',{'form':form})








def address_delete(request,id):

    Address.objects.get(id=id).delete()

    return redirect(address_view)











