from rest_framework import generics
from .models import Product
from .serializers import PrimaryProductSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = PrimaryProductSerializer
    
    def perform_create(self, serializer):
        # serializer.save(user=self.request.user)
        print(serializer.validated_data)
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content', None)
        if not content:
            content = title
        serializer.save(content=content)
        # Send a Django signal
        
class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = PrimaryProductSerializer
    lookup_field = 'pk'
    
class ProductUpdateAPIView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = PrimaryProductSerializer
    lookup_field = 'pk'
    
    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.titlw
    
class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = PrimaryProductSerializer

@api_view(["GET", "POST"])
def product_alt_view(request, pk=None, *args, **kwargs):
    method = request.method
    
    if method == "GET":
        if pk is not None:
            obj = get_object_or_404(Product, pk=pk)
            data = PrimaryProductSerializer(obj).data
            return Response(data)
        
        queryset = Product.objects.all()
        data = PrimaryProductSerializer(queryset, many=True).data
        return Response(data)
    
    if method == "POST":
        serializer = PrimaryProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            title = serializer.validated_data.get('title')
            content = serializer.validated_data.get('content', None)
            if not content:
                content = title
            serializer.save(content=content)
            return Response(serializer.data)

        return Response({"Invalid": "Bad data"}, status=405)
    