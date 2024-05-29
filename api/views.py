from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
from rest_framework import authentication,permissions
from rest_framework.response import Response
from api.serializers import *
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework import authentication,permissions

# Create your views here.

class UserRegister(APIView):

    def post(self,request,*args,**kwargs):

        serializer=Registration(data=request.data)

        if serializer.is_valid():

            serializer.save()

        return Response(serializer.data)
    

class TodoViewSetView(ViewSet):

    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def list(self,request,*args,**kwargs):

        qs=Taskmodel.objects.all()

        serializer=TodoSerializer(qs,many=True)

        return Response(serializer.data)
    
    def create(self,request,*args,**kwargs):

        serializer=TodoSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save(user=request.user)

        return Response(serializer.data)
    
    def destroy(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        qs=Taskmodel.objects.get(id=id)
        
        if qs.user==request.user:

            qs.delete()

            return Response({"message":"Todo Deleted Sucessfully"})
        
        else:
            
            return Response({"message":"Id doesn't Exist"})


    def retrieve(self,request,*args,**kwargs):

        id=kwargs.get('pk')

        qs=Taskmodel.objects.get(id=id)

        if qs.user==request.user:

            serializer=TodoSerializer(qs)

            return Response(serializer.data)
        
        else:

            return Response({'message':'no todo item'})
        

    def update(self,request,*args,**kwargs):
        
        id=kwargs.get('pk')

        qs=Taskmodel.objects.get(id=id)

        if qs.user==request.user:

            serializer=TodoSerializer(data=request.data,instance=qs)

            if serializer.is_valid():

                serializer.save()

            return Response(serializer.data)
        
        else:

            return Response({'message':'no todo item'})
        


class TodoModelViewset(ModelViewSet):  #L C R U D

    queryset=Taskmodel.objects.all()
    serializer_class=TodoSerializer
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        return Taskmodel.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
    
    def perform_update(self, serializer):
        return super().perform_update(serializer)