from rest_framework import generics
from .models import Product
from .serializers import PrimaryProductSerializer

class ProductCreateAPIView(generics.CreateAPIView):
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
    
class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = PrimaryProductSerializer
    