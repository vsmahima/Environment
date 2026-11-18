from django.shortcuts import render,redirect,get_object_or_404
from .models import Registration,ProductModel,Validation
from .forms import ProductAddingForms, ValidationForms,updatelist_validform

from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages


# Create your views here.
def home(request):
    return render(request,"home.html")

def about(request):
    return render(request,"about.html")
def contact(request):
    return render(request,"contact.html")

def register(request):
    if request.method == "POST":
        profile=request.FILES.get("profile")
        full_name=request.POST.get("full_name")
        email=request.POST.get("email")
        user_name=request.POST.get("user_name")
        password=request.POST.get("password")
        gender=request.POST.get("gender")
        dob=request.POST.get("dob")
        address=request.POST.get("address")
        phone_number=request.POST.get("phone_number")
        
        mydata=Registration(
            profile=profile,
            full_name=full_name,
            email=email,
            user_name=user_name,
            password=password,
            gender=gender,
            dob=dob,
            address=address,
            phone_number=phone_number
        )
        mydata.save()
        print("saved")
    
    
    return render(request,"register.html")

def dashboard(request):
    form=Validation.objects.all
    mydata=Registration.objects.all()
    return render(request,"dashboard.html",{"mydata":mydata,"form":form })

def update(request,pk):
    data=Registration.objects.get(id=pk)
    if request.method=="POST":
        if request.FILES.get("profile"):
            data.profile=request.FILES.get("profile")
        data.full_name=request.POST.get("full_name")
        data.email=request.POST.get("email")
        data.user_name=request.POST.get("user_name")
        data.password=request.POST.get("password")
        data.gender=request.POST.get("gender")
        data.dob=request.POST.get("dob")
        data.address=request.POST.get("address")
        data.phone_number=request.POST.get("phone_number")
        data.save()
        print("saved succesfully")
    return render(request,"update.html", {"data":data})

def delete(request,pk):
    data=Registration.objects.get(id=pk)
    if request.method=="POST":
        data.delete()
        return redirect("dashboard")
    return render(request,"delete.html")
def login(request):
    if request.method=='POST':
        uname=request.POST.get("username")
        pswd=request.POST.get("password")
        data=Registration(user_name=uname,password=pswd)
        if data:
            return redirect("dashboard")

    return render(request,"login.html")

def product(request):
    if request.method == "POST":
        data=ProductAddingForms(request.POST,request.FILES)
        if data.is_valid():
            data.save()
            print("saved")
    return render(request,"product.html")

def validate(request):
    if request.method == "POST":
            form=ValidationForms(request.POST,request.FILES)
            
            if form.is_valid():
                user=form.save()
                fullname=form.cleaned_data["fullname"]
                email=form.cleaned_data["email"]
                print("saved")
                subject = "Registration confirmation"
                message = f"""Hello {form.fullname},
                    Your registration has been succefully completed
                
                    Thank You.
                
                """
                send_mail(subject,message,
                          settings.DEFAULT_FROM_EMAIL,
                          [email],
                          fail_silently=False)
                messages.success(request,"Registration succesfull")
    else:
        form=ValidationForms()
    return render(request,
                  "validate.html",
                  {"form":form})

def update_list(request,pk):
    form =Validation.objects.get(id=pk)
    user=get_object_or_404(Validation,id=pk)
    if request.method=="POST":
        form =updatelist_validform(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form=updatelist_validform(instance=user)

    return render(request,"update_list.html",{"data":form})
