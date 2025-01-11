from rest_framework import generics
from ads.models import Category,Ad
from .serializers import CategorySerializer,AdListSerializer,AdDetailSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .permissions import IsEnrolled
from rest_framework.authentication import BasicAuthentication


class CategoryListView(generics.ListAPIView):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer

class CategoryDetailView(generics.RetrieveAPIView):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer
    

class AdListView(generics.ListAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdListSerializer

class AdDetailView(generics.RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdDetailSerializer
    permission_classes=[IsEnrolled]
    

class AdEnrollView(APIView):
    authentication_classes=[BasicAuthentication]
    queryset=Ad.objects.all()
    permission_classes=[IsAuthenticated]

    def post(self,request,pk):
        ad=get_object_or_404(Ad,pk=pk)
        ad.customers.add(request.user)
        return Response({'enrolled':True,})
    




