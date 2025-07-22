from rest_framework import viewsets, mixins
from .models import Product
from .serializers import PrimaryProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    '''
    get -> list -> Queryset
    get -> retrieve -> Product instance
    post -> create -> New Instance
    put -> update
    patch -> partial update
    delete -> destroy
    '''
    
    queryset = Product.objects.all()
    serializer_class = PrimaryProductSerializer
    lookup_field= 'pk'
    
class ProductGenericViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet):
    '''
    get -> list -> Queryset
    get -> retrieve -> Product instance
    '''
    
    queryset = Product.objects.all()
    serializer_class = PrimaryProductSerializer
    lookup_field= 'pk'