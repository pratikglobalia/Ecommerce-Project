from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings
from django.core.mail import send_mail
from random import randrange

# Create your views here.


def Home(request):
    men = ProductModel.objects.filter(category='mens')
    women = ProductModel.objects.filter(category='womens')
    kids = ProductModel.objects.filter(category='kids')
    try:
        user = User.objects.get(email=request.session['useremail'])
        return render(request, 'index.html', {'user': user, 'mproduct': men, 'wproduct': women, 'kproduct': kids})
    except:
        return render(request, 'index.html', {'mproduct': men, 'wproduct': women, 'kproduct': kids})


def About(request):
    try:
        user = User.objects.get(email=request.session['useremail'])
        return render(request, 'about.html', {'user': user})
    except:
        return render(request, 'about.html')


def Product(request):
    product = ProductModel.objects.all().order_by('-id')
    try:
        user = User.objects.get(email=request.session['useremail'])
        return render(request, 'products.html', {'user': user, 'products': product})
    except:
        return render(request, 'products.html', {'products': product})


def Single_product(request, pk):
    product = ProductModel.objects.get(id=pk)
    if request.method == "POST":
        try:
            user = User.objects.get(email=request.session['useremail'])
            duplicate = CartModel.objects.filter(product=product)
            if not duplicate:
                cart = CartModel.objects.create(
                    user=user,
                    product=product,
                    quantity=request.POST['quantity']
                )
                cart = CartModel.objects.filter(user=user)       
                return render(request, 'cart.html', {'user':user, 'cart':cart})
            else:
                return redirect('cart')
        except:
            messages.error(request, 'Login Required!, Please Login!!!')
            return redirect('login')
    return render(request, 'single_product.html', {'sproduct': product})
    

def ShoppingCart(request):
    user = User.objects.get(email=request.session['useremail'])
    cart = CartModel.objects.filter(user=user)
    return render(request, 'cart.html', {'user': user, 'cart': cart})   


def RemoveCartProduct(request, pk):
    cart = CartModel.objects.get(id=pk)
    cart.delete()
    return redirect('cart')


def Contact(request):
    try:
        user = User.objects.get(email=request.session['useremail'])
        return render(request, 'contact.html', {'user': user})
    except:
        if request.method == 'POST':
            contact = ContactModel.objects.create(
                name=request.POST['name'],
                email=request.POST['email'],
                message=request.POST['message'],
            )
        return render(request, 'contact.html')


def Signup(request):
    if request.method == 'POST':
        try:
            User.objects.get(email=request.POST.get('email'))
            messages.error(request, 'Email already exist!!!')
        except:
            if request.POST.get('password') == request.POST.get('confirm_password'):
                global signup
                signup = {
                    'name': request.POST.get('username'),
                    'mobile_number': request.POST.get('mobilenumber'),
                    'email': request.POST.get('email'),
                    'password': make_password(request.POST.get('password'))
                }
                otp = randrange(1000, 9999)
                subject = 'welcome to Hexashop'
                message = f'Your OTP is {otp}. please enter correctly'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [request.POST.get('email'), ]
                send_mail(subject, message, email_from, recipient_list)
                return render(request, 'otp.html', {'otp': otp})
            else:
                messages.error(
                    request, 'Password and confirm-password are not match!!!')
    return render(request, 'signup.html')


def UserOTP(request):
    if request.method == 'POST':
        if request.POST.get('otp') == request.POST.get('uotp'):
            global signup
            User.objects.create(
                name=signup['name'],
                mobile_number=signup['mobile_number'],
                email=signup['email'],
                password=signup['password']
            )
            messages.success(request, 'Account created Successfully!!!')
            return redirect('login')
        messages.error(request, 'Invalid OTP, Please Try Again!!!')
        return redirect('signup')
    return render(request, 'otp.html')


def Login(request):
    try:
        user = User.objects.get(email=request.session['useremail'])
        return redirect('/')
    except:
        if request.method == 'POST':
            try:
                udata = User.objects.get(email=request.POST['email'])
                if check_password(request.POST['password'], udata.password):
                    request.session['useremail'] = udata.email
                    messages.success(
                        request, f'Hello  {udata.name} , WelCome  To  HexaShop!')
                    return redirect('/')
                messages.error(request, 'Invalid password!!!')
            except:
                messages.error(request, 'Invalid email!!!')
        return render(request, 'login.html')


def Logout(request):
    del request.session['useremail']
    return redirect('/')


def Profile(request):
    user = User.objects.get(email=request.session['useremail'])
    if request.method == 'POST':
        user.mobile_number = request.POST['mobilenumber'] or user.mobile_number
        user.address = request.POST['address'] or user.address
        user.postcode = request.POST['postcode'] or user.postcode
        user.area = request.POST['area'] or user.area
        user.city = request.POST['city'] or user.city
        user.country = request.POST['country'] or user.country
        user.state = request.POST['state'] or user.state
        user.save()
    return render(request, 'profile.html', {'user': user})


def ChangePassword(request):
    user = User.objects.get(email=request.session['useremail'])
    if request.method == 'POST':
        if check_password(request.POST['oldpassword'], user.password):
            if request.POST['newpassword'] == request.POST['confirmpassword']:
                user.password = make_password(request.POST['newpassword'])
                user.save()
                messages.success(request, 'Password Change Successfully!!!!')
                return redirect('profile')
            else:
                messages.error(
                    request, 'NewPassword and ConfirmPassword Not Match!!!!')
        else:
            messages.error(request, 'Invalid old-password!!!!')
    return render(request, 'changepass.html', {'user': user})


def ForgotPassword(request):
    if request.method == 'POST':
        if User.objects.filter(email=request.POST['email']):
            global user
            user = User.objects.get(email=request.POST['email'])
            otp = randrange(100000, 999999)
            subject = 'Welcome To Hexashop'
            message = f'Your New Password is {otp}. please do not share with anyone!!'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [request.POST.get('email'), ]
            send_mail(subject, message, email_from, recipient_list)
            return render(request, 'resetotp.html', {'otp': otp})
        messages.error(
            request, 'Email does not exist, please enter valid email!!!')
    return render(request, 'forgotpass.html')


def ResetOTP(request):
    if request.method == 'POST':
        if request.POST.get('otp') == request.POST.get('uotp'):
            global user
            user.password = make_password(request.POST.get('uotp'))
            user.save()
            messages.success(request, 'Password Reset SuccessFully!!!')
            return redirect('login')
        messages.error(request, 'Invalid Password, Please Try Again')
        return redirect('forgotpass')
    return render(request, 'resetotp.html')


def Library(request):
    if request.method == 'POST':
        product = ProductModel.objects.filter(category=request.POST['category'])
        a = request.POST.getlist('name')
        data = ProductModel.objects.filter(category__in=a)
        if product:
            return render(request, 'library.html', {'product':product})
        else:
            return render(request, 'library.html', {'data':data})
    return render(request, 'library.html')
     
     
def Search(request):
    if request.method =='POST':
        search = request.POST['search']
        product = ProductModel.objects.filter(product_name=search)
        product1 = ProductModel.objects.filter(category=search)
        if product:
            return render(request, 'library.html', {'product':product})
            
        elif product1:
            return render(request, 'library.html', {'product':product1})
            
        else:
            return render(request, 'library.html', {'msg':f'no match related to"{search}"'})
    return render(request, 'library.html')