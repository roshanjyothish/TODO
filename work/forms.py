from django import forms
# from django.contrib.auth.models import User    OR
from work.models import User,Taskmodel



class Register(forms.ModelForm):
    
    class Meta:

        model=User

        fields=['username','first_name','last_name','email','password']

        widgets={
            'username':forms.TextInput(attrs={'class':'form-control','placeholder':'enter a username'}),
            'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':'enter your first name'}),
            'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'enter your last name'}),
            'email':forms.TextInput(attrs={'class':'form-control','placeholder':'enter your email address'}),
            'password':forms.TextInput(attrs={'class':'form-control','placeholder':'enter a password'})
        }



class TaskForm(forms.ModelForm):

    class Meta:

        model=Taskmodel

        fields=['task_name','task_description']

        widgets={
            'task_name':forms.TextInput(attrs={'class':'form-control','placeholder':'enter the task'}),
            'task_description':forms.Textarea(attrs={'class':'form-control','column':20,'rows':5,'placeholder':'enter the description'})
        }





# class Loginform(forms.Form):

#     username=forms.CharField()
#     password=forms.CharField()


class Loginform(forms.Form):

    username=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control',
                                                                            'placeholder':'Username'}))
    password=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control',
                                                                           'placeholder':'password'}))