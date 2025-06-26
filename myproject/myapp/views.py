from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import PersonModel
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class PersonListCreate(APIView):
    @swagger_auto_schema(
        operation_description="Get all people",
        responses={200: openapi.Response(description="List of people")}
    )
    def get(self, request):
        people = list(PersonModel.objects.values())
        return Response(people)

    @swagger_auto_schema(
        operation_description="Add a new person",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name', 'lastname'],
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'lastname': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={201: openapi.Response(description="Person added")}
    )
    def post(self, request):
        data = request.data
        name = data.get('name')
        lastname = data.get('lastname')
        if not name or not lastname:
            return Response({'error': 'Missing name or lastname'}, status=status.HTTP_400_BAD_REQUEST)

        person = PersonModel.objects.create(name=name, lastname=lastname)
        return Response({'message': 'Person added', 'id': person.id}, status=status.HTTP_201_CREATED)


class PersonUpdateDelete(APIView):
    @swagger_auto_schema(
        operation_description="Update a person",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'lastname': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={200: "Person updated"}
    )
    def put(self, request, person_id):
        person = get_object_or_404(PersonModel, id=person_id)
        data = request.data
        person.name = data.get('name', person.name)
        person.lastname = data.get('lastname', person.lastname)
        person.save()
        return Response({'message': 'Person updated'})

    @swagger_auto_schema(
        operation_description="Delete a person",
        responses={200: "Person deleted", 404: "Not found"}
    )
    def delete(self, request, person_id):
        person = get_object_or_404(PersonModel, id=person_id)
        person.delete()
        return Response({'message': 'Person deleted'})
