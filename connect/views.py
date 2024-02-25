from os import uname
import razorpay
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render
from .models import Contact
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Contact
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.core.mail import send_mail



def user_reg(request):
    context = {}
    if(request.method=="POST"):
        uname = request.POST['uname']
        upass = request.POST['upass']
        ucpass = request.POST['ucpass']
        if uname =="" or upass == "" or ucpass == "":
            context['error'] = "Please fill all the fields"
            return render(request, "registration.html", context)
        elif upass != ucpass:
            context['error'] = "Passward and confirm passward should be same"
            return render(request, "registration.html", context)
        else:
            user_object = User.objects.create(password= upass, username = uname, email = uname)
            user_object.set_password(upass)
            user_object.save()
            context['success'] = "Registration Successfull, kindly login"
            return render(request, "registration.html", context)
            
    else:
        return render(request,"registration.html")
    
def user_logout(request):
    logout(request)
    return redirect("/")


def index(request):
    return render(request, "index.html")

def home(request):
    c = Contact.objects.filter(uname=request.user.username)
    context = {'contact': c}
    return render(request, "home.html", context)


def user_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['uname']
        p = request.POST['upass']
        user = authenticate(username=u, password=p)
        try:
            if user:
                login(request, user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    return render(request, 'login.html', locals())

@login_required
def add_contact(request):
    error = ""
    if request.method == "POST":
        name = request.POST['Name']
        phon_number = request.POST['Number']
        email = request.POST["email"]
        category = request.POST["category"]
        location = request.POST["Location"]
        
        try:
            Contact.objects.create(name=name, phone_number=phon_number, email=email, category=category, location=location, uname=request.user.username)
            error = "no"
        except:
            error = "yes"

    return render(request, 'add_contact.html', {'error': error})

@login_required
def edit_Contact(request,cid):
    Cont = Contact.objects.get(id=cid)
    if request.method == "POST":
        name = request.POST['Name']
        phon_number = request.POST['Number']
        email = request.POST["email"]
        category = request.POST["category"]
        location = request.POST["Location"]
        Fva = Cont.addtoFva

        Cont.name = name
        Cont.phone_number = phon_number
        Cont.email=email
        Cont.category=category
        Cont.location=location
        Cont.addtoFva = Fva
        
        try:
            Cont.save()
            error = "no"
        except:
            error = "yes"
    return render(request, 'edit_contact.html', locals())

def deleteContact(request,cid):
    if not request.user.is_authenticated:
        return redirect('login')
    contact = Contact.objects.get(id=cid)
    contact.delete()
    return redirect("/home")


@require_POST
def toggle_favorite(request, contact_id):
    try:
        contact = Contact.objects.get(id=contact_id)
        contact.addtoFva = not contact.addtoFva
        contact.save()
        return JsonResponse({'success': True, 'favorite': contact.addtoFva})
    except Contact.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Contact not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    

def Filter_Contact(request, cid):
    context = {}

    if cid == '1':
        contact = Contact.objects.filter(category="1").filter(uname=request.user.username)
    elif cid == '2':
        contact = Contact.objects.filter(category="2").filter(uname=request.user.username)
    elif cid == '3':
        contact = Contact.objects.filter(category="3").filter(uname=request.user.username)
    elif cid == 'fav':
        contact = Contact.objects.filter(addtoFva=True).filter(uname=request.user.username)
    
        

    context['contact'] = contact
    return render(request, "home.html", context)

def search_contact(request):
    searchfield = request.GET.get('searchfield')
    contact_results = Contact.objects.filter(name__icontains=searchfield).filter(uname=request.user.username)
    return render(request, 'search_results.html', {'contact_results': contact_results, 'searchfield': searchfield})

def about_page(request):
    return render(request, "about.html")




# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
 
 
def contrib(request):
    currency = 'INR'
    amount = 20000  # Rs. 200
 
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'
 
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
 
    return render(request, 'contrib.html', context=context)
 
 
# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):
 
    # only accept POST request.
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                amount = 20000  # Rs. 200
                try:
 
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
 
                    # render success page on successful caputre of payment
                    render_result = render(request, 'paymentsuccess.html')
                
                    # call the send mail view
                    sendusermail(request)
                    return render_result
                except:
 
                    # if there is an error while capturing payment.
                    return render(request, 'paymentfail.html')
            else:
 
                # if signature verification fails.
                return render(request, 'paymentfail.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()
    

# mail integration
def sendusermail(request):
    msg = """Dear User,

Thank you for your 200 Rupee contribution to the Connectify application. Your support is invaluable and will directly contribute to the improvement and maintenance of our platform.

We appreciate your generosity and are grateful to have you as part of our community.

Best regards,
Connectify Team"""
    send_mail(
        "Payment Successfull",
        msg,
        "maheshmorde2511@gmail.com",
        ["mordemahi@gmail.com"],  # You can add user's email here
        fail_silently=False,
    )
    return HttpResponse('hello')
