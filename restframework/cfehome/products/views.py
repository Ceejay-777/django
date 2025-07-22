from rest_framework import generics, mixins, status, permissions, authentication
from .models import Product
from .serializers import PrimaryProductSerializer
from ..api.permissions import IsStaffEditorPermission
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from api.authentication import TokenAuthentication

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = PrimaryProductSerializer
    authentication_classes = [authentication.SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission] # Ordering matters
    
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
            instance.content = instance.title
            
class ProductDestroyAPIView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = PrimaryProductSerializer
    lookup_field = 'pk'
    
    def perform_destroy(self, instance):
        # Perform operations
        super().perform_destroy(instance)
        
class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = PrimaryProductSerializer
    
class ProductMixinView(
    mixins.ListModelMixin, 
    mixins.RetrieveModelMixin, 
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView
    ):
    queryset = Product.objects.all()
    serializer_class = PrimaryProductSerializer
    lookup_field = 'pk'
    
    def get(self, request, *args, **kwargs):
        pk= kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        if pk is None:
            return Response({"detail": "No id provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        return self.update(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.patch(request, *args, **kwargs)

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
    