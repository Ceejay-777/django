from django.http import JsonResponse, HttpResponse
import json
from django.forms.models import model_to_dict
from products.models import Product
from rest_framework.response import Response
from rest_framework.decorators import api_view
from products.serializers import PrimaryProductSerializer, SecondaryProductSerializer

@api_view(["POST"])
def api_home(request, *args, **kwargs):
    # instance = Product.objects.all().order_by("?").first()
    # data = {}
    serializer = PrimaryProductSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        # instance = serializer.save()
        print(serializer.data)
        
        return Response(serializer.data)
    
    return Response({"Invalid": "Bad data"}, status=405)