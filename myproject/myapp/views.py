from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import PersonModel
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.hashers import make_password

class PersonListCreate(APIView):
    @swagger_auto_schema(
        operation_description="Get all registered users",
        responses={200: openapi.Response(description="List of users")}
    )
    def get(self, request):
        people = list(PersonModel.objects.values("id", "name", "email"))
        return Response(people)

    @swagger_auto_schema(
        operation_description="Register a new user",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name', 'email', 'password', 'repeat_password', 'agree_terms'],
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD),
                'repeat_password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD),
                'agree_terms': openapi.Schema(type=openapi.TYPE_BOOLEAN),
            },
        ),
        responses={201: openapi.Response(description="User registered")}
    )
    def post(self, request):
        data = request.data
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        repeat_password = data.get('repeat_password')
        agree_terms = data.get('agree_terms')

        # Validation
        if not all([name, email, password, repeat_password]):
            return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)
        if password != repeat_password:
            return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
        if not agree_terms:
            return Response({'error': 'You must agree to the Terms of Service'}, status=status.HTTP_400_BAD_REQUEST)
        if PersonModel.objects.filter(email=email).exists():
            return Response({'error': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)

        # Hash password and save
        hashed_password = make_password(password)
        person = PersonModel.objects.create(
            name=name,
            email=email,
            password=hashed_password,
            agree_terms=agree_terms
        )

        return Response({'message': 'User registered', 'id': person.id}, status=status.HTTP_201_CREATED)


class PersonUpdateDelete(APIView):
    @swagger_auto_schema(
        operation_description="Update a user's info",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD),
            },
        ),
        responses={200: "User updated"}
    )
    def put(self, request, person_id):
        person = get_object_or_404(PersonModel, id=person_id)
        data = request.data

        person.name = data.get('name', person.name)
        email = data.get('email')
        if email and email != person.email:
            if PersonModel.objects.filter(email=email).exists():
                return Response({'error': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)
            person.email = email

        password = data.get('password')
        if password:
            person.password = make_password(password)

        person.save()
        return Response({'message': 'User updated'})

    @swagger_auto_schema(
        operation_description="Delete a user",
        responses={200: "User deleted", 404: "Not found"}
    )
    def delete(self, request, person_id):
        person = get_object_or_404(PersonModel, id=person_id)
        person.delete()
        return Response({'message': 'User deleted'})
