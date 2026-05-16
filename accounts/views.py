from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from .serializers import RegisterSerializer
import bcrypt

from django.views.decorators.csrf import csrf_exempt
# from rest_framework_simplejwt.tokens import RefreshToken


@csrf_exempt
@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"msg": "User Registered"})
    return Response(serializer.errors)


@csrf_exempt
@api_view(['POST'])
def login(request):

    user_input = request.data.get('username')
    password = request.data.get('password')

    user = User.objects.filter(username=user_input).first() or User.objects.filter(email=user_input).first()

    if user and bcrypt.checkpw(password.encode(), user.password.encode()):

        # SESSION CREATE
        request.session['user_id'] = user.id

        return Response({
            "msg": "Login Success",
            "user_id": user.id,
            "username": user.username
        })

    return Response({
        "msg": "Invalid Credentials"
    })


# @csrf_exempt
# @api_view(['POST'])
# def login(request):
#     user_input = request.data.get('username')
#     password = request.data.get('password')

#     user = User.objects.filter(username=user_input).first() or User.objects.filter(email=user_input).first()

#     if user and bcrypt.checkpw(password.encode(), user.password.encode()):
#         request.session['user_id'] = user.id   
#         return Response({"msg": "Login Success"})

#     return Response({"msg": "Invalid Credentials"})


@api_view(['GET'])
def check_session(request):
    user_id = request.session.get('user_id')

    if user_id:
        from .models import User
        user = User.objects.get(id=user_id)
 
        return Response({
            "logged_in": True,
            "username": user.username,  
            "user_id": user.id
        })

    return Response({"logged_in": False})

@api_view(['POST'])
def logout(request):

    request.session.flush()

    return Response({
        "msg": "Logged Out"
    })