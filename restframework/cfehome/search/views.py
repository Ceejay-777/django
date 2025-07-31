from rest_framework import generics
from products.models import Product
from products.serializers import PrimaryProductSerializer
from rest_framework.response import Response

from . import client

class SearchListView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q')
        if not query:
            return Response('', status=400)
        results = client.perform_search(query)
        return Response(results)
        

class SearchListOldView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = PrimaryProductSerializer
    
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        query = self.request.GET.get('q')
        results = Product.objects.none()
        if query is not None:
            user = None
            if self.request.user.is_authenticated:
                user = self.request.user
                
            results = queryset.search(query, user=user)
        return results
    