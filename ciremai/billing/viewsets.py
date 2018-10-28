from rest_framework import viewsets
from django.contrib.auth.models import User
from .models import Patients,Article
from .serializers import PatientSerializer,ArticleSerializer,UserSerializer


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patients.objects.all()
    serializer_class = PatientSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    
