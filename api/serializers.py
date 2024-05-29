from rest_framework import serializers
from work.models import *

class Registration(serializers.ModelSerializer):

    class Meta:

        model=User

        fields=['id','username','email','password','first_name','last_name']

        read_only_fields=['id']

    def create(self,validated_data):

        return User.objects.create_user(**validated_data)
    


class TodoSerializer(serializers.ModelSerializer):

    user=serializers.StringRelatedField(read_only=True)

    class Meta:

        model=Taskmodel

        fields="__all__"

        read_only_field=['id','created_date','user','completed']