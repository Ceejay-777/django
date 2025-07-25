from rest_framework import generics, mixins, status
from .models import Product
from .serializers import PrimaryProductSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from api.mixins import StaffEditorPermissionMixin, UserQuerySetMixin

class ProductListCreateAPIView(
    UserQuerySetMixin,
    StaffEditorPermissionMixin,
    generics.ListCreateAPIView
    ):
    queryset = Product.objects.all()
    serializer_class = PrimaryProductSerializer
    # permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission] # Ordering matters
    
    def perform_create(self, serializer):
        # serializer.save(user=self.request.user)
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content', None)
        if not content:
            content = title
        serializer.save(user=self.request.user, content=content)
        # Send a Django signal
        
    # def get_queryset(self, *args, **kwargs):
    #     queryset = super().get_queryset(*args, **kwargs)
    #     request = self.request
    #     # print(request.user)
    #     return queryset.filter(user=request.user)
        
class ProductDetailAPIView(
    StaffEditorPermissionMixin,
    generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = PrimaryProductSerializer
    # lookup_field = 'pk'
    
class ProductUpdateAPIView(
    StaffEditorPermissionMixin,
    generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = PrimaryProductSerializer
    lookup_field = 'pk'
    
    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title
            
class ProductDestroyAPIView(
    StaffEditorPermissionMixin,
    generics.DestroyAPIView):
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
    