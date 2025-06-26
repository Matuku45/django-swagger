from django.urls import path
from .views import PersonListCreate, PersonUpdateDelete




urlpatterns = [
    path('people/', PersonListCreate.as_view(), name='people'),
    path('people/<int:person_id>/', PersonUpdateDelete.as_view(), name='person-detail'),
]
