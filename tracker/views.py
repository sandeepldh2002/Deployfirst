from django.shortcuts import render, redirect
from django.contrib import messages
from tracker.models import Transaction
from django.db.models import Sum
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import logging
logger = logging.getLogger(__name__)

# Create your views here.


def registration(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name') 
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = User.objects.filter(
            Q(email = email) | Q(username = username) #like if condition
        )

        if user_obj.exists():
            messages.error(request, "Email or Username already exists")
            return redirect('/registration/')
        
        user_obj = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username,
            email = email   
        )
        user_obj.set_password(password) #django pasword ko encrypt krne ke liye set_password method provide krta ha 
        user_obj.save()
        messages.info(request, 'Successfully Your Account has been Created')
        return redirect('/registration/')

    
    return render(request, 'registration.html')

def login_page(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(
                username = username
        )

        if not user_obj.exists():
            messages.info(request, "Username does not exist")
            return redirect('/login/')

        user_obj = authenticate(username = username, password = password) #authenticate ek function ha ek method ha

        if not user_obj:
            messages.info(request, "Invalid Cardentials")
            return redirect('/login/')
        
        login(request, user_obj) #login apka authenticate ko cookie ke inside session me jakar kr bind kr dega 
        return redirect('/')


    return render(request, 'login.html')


def logout_page(request):
    logout(request)
    messages.info(request, "Logged out Successfully")
    return redirect('/login/')


@login_required(login_url='/login/')
def index(request):
    print(request.user)
    print(request.user.is_authenticated) # True or False return krega if user login to phir True return krega if user login nhi to false return krega
    if request.method == 'POST':
        description = request.POST.get('description')
        amount = request.POST.get('amount')

        print(description, amount)
        # print(type(amount))
        
        if description is "": # "" means none 
            messages.info(request, "Description can not be blank")
            return redirect('/')

        try:
            amount = float(amount)
        except Exception as e:        
                messages.info(request, "Amout field should be a number")
                return redirect('/')
        

        Transaction.objects.create(
            description = description,
            amount = amount,
            Created_by = request.user
        )
        
        return redirect('/')

    context = {'transactions': Transaction.objects.filter(Created_by = request.user),
                'balance': Transaction.objects.filter(Created_by = request.user).aggregate(total_balance = Sum('amount'))['total_balance'] or 0, # either none or return 0
                'income': Transaction.objects.filter(Created_by = request.user, amount__gte = 0).aggregate(income = Sum('amount'))['income'] or 0,
                'expense': Transaction.objects.filter(Created_by = request.user, amount__lte = 0).aggregate(expense = Sum('amount'))['expense'] or 0,
                }
    return render(request, 'index.html', context)

@login_required(login_url='/login/')
def deleteTransaction(request, uuid):
    Transaction.objects.get(uuid = uuid).delete()
    return redirect('/')