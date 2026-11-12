from django import forms
from .models import ProductModel,Registration,Validation
import re


class ProductAddingForms(forms.ModelForm):
    class Meta:
        model = ProductModel
        fields = "__all__"


class ValidationForms(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput)
    confirmpassword = forms.CharField(
        widget=forms.PasswordInput
    )
    class Meta:
        model = Validation
        fields = "__all__"

    def clean_fullname(self):
        fullname=self.cleaned_data["fullname"]
        if len(fullname)<4:
            raise forms.ValidationError("Enter valid name")
        return fullname

    def clean_username(self):
        username=self.cleaned_data["username"]
        if len(username)<4:
            raise forms.ValidationError("Enter valid username")
        return username
    def clean_email(self):
            email=self.cleaned_data["email"]   
            if Validation.objects.filter(email=email).exists():
                raise forms.ValidationError("Email already exists")
            return email
    def clean_password(self):
        password=self.cleaned_data["password"]
        if len(password)<8:
            raise forms.ValidationError("password should be more then 8 characters")
        if not re.search(r'[A-Z]',password):
            raise forms.ValidationError("Password should contain atleast one upper case")
        if not re.search(r'[a-z]',password):
            raise forms.ValidationError("Password should contain atleast one lower case")
        if not re.search(r'[0-9]',password):
            raise forms.ValidationError("Password should contain atleast one digit")
        if not re.search(r'[@#$%^&?/]',password):
                    raise forms.ValidationError("Password sgould contain atleast one special character")
                
        return password

    def clean(self):
        data=super().clean()
        password=data.get("password")
        confirmpassword=data.get("confirmpassword")
        if password and confirmpassword:
             if password != confirmpassword:
                  self.add_error("confirmpassword","password and confirm paasword should match")
        return data

class updatelist_validform(forms.ModelForm):
     class Meta:
          model=Validation
          fields="__all__"

         