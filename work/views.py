from typing import Any
from django.shortcuts import render,redirect
from django.views.generic import View
from work.forms import Register,Loginform,TaskForm
from work.models import User,Taskmodel
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.utils.decorators import method_decorator

# D E C O R A T O R

def signin_required(fn):

    def wrapper(request,**kwargs):

        if not request.user.is_authenticated:

            return redirect("login")
        
        else:

            return fn(request,**kwargs)
        
    return wrapper


def mylogin(fn):

    def wrapper(request,**kwargs):

        id=kwargs.get("pk")

        obj=Taskmodel.objects.get(id=id)

        if obj.user!= request.user:

            return redirect("login")

        else:

            return fn(request,**kwargs)
        
    return wrapper

# Create your views here.

class Registration(View):

    def get(self,request,**kwargs):

        form=Register()

        return render(request,"register.html",{"form":form})
    
    def post(self,request,**kwargs):

        form=Register(request.POST)

        if form.is_valid():

            User.objects.create_user(**form.cleaned_data)

            form=Register()

            return render(request,"register.html",{"form":form})




class Signin(View):

    def get(self,request,**kwargs):

        form=Loginform()

        return render(request,"login.html",{"form":form})
    
    def post(self,request,**kwargs):

        form=Loginform(request.POST)

        if form.is_valid():

            print(form.cleaned_data)

            user_name=form.cleaned_data.get("username")
            # getting username and password from cleaned_data
            pwd=form.cleaned_data.get("password")

            user_obj=authenticate(username=user_name,password=pwd)
            # checking if the username and password are valid in the table auth_user

            if user_obj:
                print(user_obj)
                print("Valid Credential")
                # if true passing the user_obj to the login function
                login(request,user_obj)
            return redirect("addtask")
            
           
            


@method_decorator(signin_required,name="dispatch")

class Add_task(View):

    def get(self,request,**kwargs):

        form=TaskForm()
        # filter method is used to get the task of the login user
        data=Taskmodel.objects.filter(user=request.user).order_by('completed')
        return render(request,"index.html",{'form':form,'data':data})
    
    def post(self,request,**kwargs):

        form=TaskForm(request.POST)
        #task_name,task_description
        if form.is_valid():
            form.instance.user=request.user
            # request.user= get the authenticated user(login)
            form.save()
            messages.success(request,"Task added sucessfully")
            form=TaskForm()
        data=Taskmodel.objects.filter(user=request.user).order_by('completed')
        return render(request,"index.html",{'form':form,'data':data})
    

@method_decorator(signin_required,name="dispatch")
@method_decorator(mylogin,name="dispatch")
class Delete_task(View):

    def get(self,request,**kwargs):

        id=kwargs.get("pk")

        Taskmodel.objects.get(id=id).delete()

        return redirect("addtask")
    

@method_decorator(signin_required,name="dispatch")
@method_decorator(mylogin,name="dispatch")
class Task_edit(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        obj=Taskmodel.objects.get(id=id)

        if obj.completed == False:
            obj.completed = True
            obj.save()
        return redirect("addtask")
    

class Signout(View):

    def get(self,request):

        logout(request)

        return redirect("login")


class User_del(View):

    def get(self,request,**kwargs):

        id=kwargs.get("pk")

        User.objects.get(id=id).delete()

        return redirect("log")


class Update_user(View):

    def get(self,request,**kwargs):

        id=kwargs.get("pk")

        data=User.objects.get(id=id)

        form=Register(instance=data)

        return render(request,"register.html",{"form":form})
    
    # def post
