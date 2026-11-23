from django.shortcuts import render,redirect,get_object_or_404
from .models import Registration,ProductModel,Validation
from .forms import ProductAddingForms, ValidationForms,updatelist_validform

from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages


#Api header section

from rest_framework.views import APIView
from rest_framework.response import Response
from . serializers import StudentSerialzer
from . models import Student
from rest_framework import status



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

        data=Registration.objects.filter(user_name=uname).first()
        if data and data.password ==pswd:
            request.session["username"] = data.user_name
            request.session["fullname"] = data.full_name
            request.session["email"] = data.email
            request.session["user_id"]= data.id
            print(request.session.items())
            # return redirect("dashboard")
            # setting cookies

            response =redirect("dashboard")
            response.set_cookie("username",
                                data.user_name,
                                max_age=60,
                                expires=True)
            response.set_cookie("fullname",
                                data.full_name,
                                max_age=3600,
                                expires=True)
            return response

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


def profile(request):
    if not request.session.get("user_id"):
        return redirect("login")
    user=Registration.objects.get(id=request.session["user_id"])
    return render(request,"profile.html",{"user":user})

def logout(request):
    response =redirect("login")
    response.delete_cookie("username")
    response.delete_cookie("fullname")
    return response


# API handling functions

class StudentList(APIView):
    def post(self,request):
        serializer = StudentSerialzer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                        status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)