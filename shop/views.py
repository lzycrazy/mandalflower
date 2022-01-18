from django.db.models import query
from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from . models import Category, OrderItem, Product,Carousel,Contact,Order,Corousel
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from time import time
import razorpay
from ecommerce.settings import *
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.mail import send_mail
import os
from twilio.rest import Client
import math



client=razorpay.Client(auth=(settings.KEY_ID,settings.KEY_SECRET))


# Create your views here.
def index(request):
    caraousel=Carousel.objects.all
    coraousel=Corousel.objects.all
    category=Category.objects.all()
    product=Product.objects.all
    latest=Product.objects.order_by('-date')[1:4]
    allpro=Product.objects.all
    catt=Category.objects.order_by('-id')[1:5]
    # categoryslug=request.GET.get('category')
    # if categoryslug:
    #     product=Product.objects.filter(slug=categoryslug)
    # else:
    #     product=Product.objects.all()

    data={
        'category':category,
        'product':product,
        'cara':caraousel,
        'latest':latest,
        'allpro':allpro,
        'car':coraousel,
        'catt':catt
        
        }
    return render(request,'dash.html',data)



def basse(request):
    allpro=Product.objects.all
    category=Category.objects.all()
    catt=Category.objects.order_by('-id')[1:5]
    
   
    data={
        'category':category,
        'allpro':allpro,
        'catt':catt
    }
    return render(request,'basse.html',data)



def category(request,slug):
    category=Category.objects.all()
    catt=Category.objects.order_by('-id')[1:5]
    # product=Product.objects.all
    # category=Category.objects.filter(slug=slug)
    # categoryslug=request.GET.get('category')
    # if categoryslug:
    #     product=Product.objects.filter(slug=categoryslug)
    # else:
    #     product=Product.objects.all()

    # data={
    #     'category':category,
    #     'product':product
    # }
    product=Product.objects.filter(slug=slug)
    data={
        'product':product,
        'category':category,
        'catt':catt
    }

    return render(request,'category.html',data)

def quickview(request,id):
    

    product=Product.objects.filter(id=id)
    allpro=Product.objects.all
    category=Category.objects.all()
    catt=Category.objects.order_by('-id')[1:5]
    categoryid=request.GET.get('category')
    if categoryid:
        product=Product.objects.filter(id=categoryid)
    

    data={
        'product':product,
        'category':category,
        'catt':catt,
        'allpro':allpro

         }
    return render(request,'quickview.html',data)

 

# shopping cart

@login_required(login_url="/users/login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("index")


@login_required(login_url="/users/login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/users/login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/users/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    # Math.max(0,1)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/users/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")

@login_required(login_url="/users/login")
def cart_detail(request):
    
    category=Category.objects.all()
    catt=Category.objects.order_by('-id')[1:5]
    categoryslug=request.GET.get('category')
    if categoryslug:
        product=Product.objects.filter(slug=categoryslug)
    else:
        product=Product.objects.all()

    data={
        'category':category,
        'catt':catt
       
        }
    return render(request, 'cart/cart_detail.html',data)


# endcart

def handlelogin(request):
    
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        

        user=authenticate(username=username,password=password)
        
        if user is not None:
            login(request, user)
            
            messages.success(request,'Successfully logged In')
            return redirect('/')

        else:
            messages.error(request,'User not Signup')
            return redirect('/') 
    # return render(request,'/')


    # return render(request,'userlogin.html')

def signup(request):
    category=Category.objects.all()
    data={
            'category':category
        }
    if request.method=="POST":
        username=request.POST.get('username')
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        email=request.POST.get('email')
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')

        if User.objects.filter(username=username).exists():
            messages.info(request,"Username already taken")
            return redirect("signup")
        
        if User.objects.filter(email=email).exists():
            messages.info(request,"Email already taken")
            return redirect("signup")


        if len(username)>10:
            messages.error(request,"Username must be under 10 character")
            return redirect("signup")

        if not username.isalnum():
            messages.error(request,"Username should only contain letters and numbers")
            return redirect("signup")
        
        if pass1 != pass2:
            messages.error(request,"Password do not matched")
            return redirect("signup")

        # create user
        myuser=User.objects.create_user(username,email,pass1)
        myuser.fname=fname
        myuser.lname=lname
        myuser.save()

        data={
            'category':category
        }
        messages.success(request,"User Created")
        return redirect("/")
        
    else:

        # messages.error(request,"User is not created")
        return render(request,'signup.html',data)
    

    


# def signup1(request):
    if request.method=="POST":
        username=request.POST.get('username')
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        email=request.POST.get('email')
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')

        if User.objects.filter(username=username).exists():
            messages.info(request,"Username already taken")
            return redirect("/")
        
        if User.objects.filter(email=email).exists():
            messages.info(request,"Email already taken")
            return redirect("/")


        if len(username)>10:
            messages.error(request,"Username must be under 10 character")
            return redirect("/")

        if not username.isalnum():
            messages.error(request,"Username should only contain letters and numbers")
            return redirect("/")
        
        if pass1 != pass2:
            messages.error(request,"Password do not matched")
            return redirect("")

        # create user
        myuser=User.objects.create_user(username,email,pass1)
        myuser.fname=fname
        myuser.lname=lname
        myuser.save()

        messages.success(request,"User Created")
        return redirect("/")
    else:
        messages.error(request,"User is not created")
        return redirect("signup")
    
        

def handlelogin1(request):
    category=Category.objects.all()
    catt=Category.objects.order_by('-id')[1:5]
    categoryslug=request.GET.get('category')
    if categoryslug:
        product=Product.objects.filter(slug=categoryslug)
    else:
        product=Product.objects.all()

    data={
        'category':category,
        'catt':catt
    }
   
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        

        user=authenticate(username=username,password=password)
        
        if user is not None:
            login(request, user)
            
            messages.success(request,'Successfully logged In')
            return redirect("/")

        else:
            messages.error(request,'User not Signup')
            return redirect('userlogin') 

        

    return render(request,'userlogin.html',data)
    

def handlelogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/')

def contact(request):
    catt=Category.objects.order_by('-id')[1:5]
    category=Category.objects.all()
    categoryslug=request.GET.get('category')
    if categoryslug:
        product=Product.objects.filter(slug=categoryslug)
    else:
        product=Product.objects.all()

    data={
        'category':category,
        'catt':catt
       
        }
    if request.method=='POST': 
        
        name=request.POST.get('name','')
        email=request.POST.get('email','')
        phone=request.POST.get('phone','')
        desc=request.POST.get('desc','')

        print(name)

        contact=Contact(name=name,email=email,phone=phone,desc=desc)
        

        subject=name
        message=desc
        email_from=settings.EMAIL_HOST_USER
        try:
            send_mail(subject,message,email_from ,['poojachauhan2102@gmail.com'])
            contact.save()
            messages.info(request,"Message Sent Successfully")
            return redirect('/')
             
        except Exception as e:
            return redirect('/contact')

       

    return render(request,"contact.html",data)

# def search(request):
#     category=Category.objects.all()
#     categoryslug=request.GET.get('category')
#     if categoryslug:
#         product=Product.objects.filter(slug=categoryslug)
#     else:
#         product=Product.objects.all()

   
#     query=request.GET.get('query')
#     product=Product.objects.filter(desc__icontains=query)
#     # product=Product.objects.filter(desc__title=query)
#     product=Product.objects.filter(name__icontains=query)
#     product=Product.objects.filter(price__icontains=query)
#     product=Product.objects.filter(slug__icontains=query)

#     data={
#         'product':product,
#          'category':category,
#     }
#     return render(request,"index.html",data)


def search(request):
    catt=Category.objects.order_by('-id')[1:5]
    query=request.GET['query']

    product=Product.objects.filter(desc__icontains=query)
    product=Product.objects.filter(name__icontains=query)
    product=Product.objects.filter(price__icontains=query)
    product=Product.objects.filter(slug__icontains=query)
    data={
        'product':product,
        'catt':catt
    }
    return render(request,'search.html',data)

def checkout(request):
    catt=Category.objects.order_by('-id')[1:5]
    category=Category.objects.all()
    categoryslug=request.GET.get('category')
    if categoryslug:
        product=Product.objects.filter(slug=categoryslug)
    else:
        product=Product.objects.all()


    amount_str=request.POST.get('amount')
    amount_float=float(amount_str)
    amount=int(amount_float)
    amount=amount*100
   

    payment=client.order.create({'amount':amount,'currency':'INR','payment_capture':'1'})
    # print(payment)
    
    order_id=payment['id']
    amount=payment['amount']
    

    context={
        'order_id':order_id,
        'payment':payment,
        'amount':amount,
        'category':category,
        'catt':catt
    }

    return render(request,"cart/checkout.html",context)
        
     

def placeorder(request):
    catt=Category.objects.order_by('-id')[1:5]
    category=Category.objects.all()
    categoryslug=request.GET.get('category')
    if categoryslug:
        product=Product.objects.filter(slug=categoryslug)
    else:
        product=Product.objects.all()

    
    if request.method=="POST":
        
        
        cart=request.session.get('cart') #to get cart all fields
        
        name=request.POST.get('name')
        email=request.POST.get('email')
        address=request.POST.get('address')
        city=request.POST.get('city')
        state=request.POST.get('state')
        zipcode=request.POST.get('zipcode')
        phone=request.POST.get('phone')
        payment_type=request.POST.get('payment_type')
        
        amount=request.POST.get('amt')
        # print(amount)
        # print(cart)
        order_id=request.POST.get('order_id')
        
        payment=request.POST.get('payment')

        
        
        

       
        data={
            'order_id':order_id,
            'amount':amount,
            'category':category,
            'catt':catt
            
           
        }
    
        
        order=Order(name=name,email=email,address=address,city=city,state=state,zipcode=zipcode,phone=phone,payment_type=payment_type,amount=amount,payment_id=order_id)
        order.save()
        for i in cart:
            a=(int(cart[i]['price']))
            b=cart[i]['quantity']
            total=a*b
            orderitem=OrderItem(
                        order=order,
                        product=cart[i]['name'],
                        image=cart[i]['image'],
                        quantity=cart[i]['quantity'],
                        price=cart[i]['price'],
                        total=total
                        

                 )
            orderitem.save()

            
             
        if payment_type=="cod":
            # messages.success(request,"Successfully Ordered")

            cart_clear(request)
            messages.success(request, "Your have Ordered Successfully")

            return redirect('thankyou')
            
            
        cart_clear(request)
        # messages.success(request, "Your have Ordered Successfully")
        # print("You have Ordered Successfully")
        # return redirect('thankyou')
    # return redirect('shopping-cart-show')

    
    return render(request,"cart/placeorder.html",data)






@csrf_exempt
def thankyou(request):
    
    cart=request.session.get('cart')
    # print('cart',cart)
    
    if request.method=="POST":
       
        a=request.POST
        order_id=""
        for key,val in a.items():
            if key=='razorpay_order_id':
                order_id=val
                break
        
        user=Order.objects.filter(payment_id=order_id).first()
       
        subject=order_id
        message="You have ordered Successfully"

        email_from=EMAIL_HOST_USER
      
        try:
            send_mail(subject,message,email_from,['poojachauhan2102@gmail.com'])
            
            user.paid=True
            user.save()
            return redirect('thankyou')

        except Exception as e:
            return redirect('/placeorder')


    return render(request,'cart/thankyou.html')
   

def myorder(request):
    order=Order.objects.all
    orderitems=OrderItem.objects.all

    cart_clear(request)
    orderitem=OrderItem.objects.order_by('product')[1:4]
    
    data={
        'order':order,
        'orderitems':orderitems,
        'orderitem':orderitem
    }

    return render(request,'myorder.html',data)

def about(request):
    category=Category.objects.all()
    catt=Category.objects.order_by('-id')[1:5]
    categoryslug=request.GET.get('category')
    if categoryslug:
        product=Product.objects.filter(slug=categoryslug)
    else:
        product=Product.objects.all()

    data={
        'category':category,
        'catt':catt
        
        
        }

    return render(request,'about.html',data)


# @csrf_exempt
# def verifypayment(request):
#     if request.method=="POST":
#         data=request.POST
#         try:
#             client.utility.verify_payment_signature(data)
#             razorpay_payment_id=data['razor_order_id']
#             razorpay_payment_id=data['razor_payment_id']
            
#             return render(request,'verifypayment.html')
#         except:
#             return HttpResponse("Invalid Payment details")
