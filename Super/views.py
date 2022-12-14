from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from SuperType.models import SuperType
from .serializers import SuperSerializer
from .models import Super
from Super import serializers

@api_view(['GET', 'POST'])
def supers_list(request):

    if request.method == 'GET':
        type_param = request.query_params.get('type')
        if type_param:
            supers = Super.objects.filter(super_type__type=type_param)
            serializer = SuperSerializer(supers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            super_types = SuperType.objects.all()
            supers_dictionary = {}

            for super_type in super_types:
                supers = Super.objects.filter(super_type_id=super_type.id)
                super_serializer = SuperSerializer(supers, many=True)
                supers_dictionary[super_type.type] = {
                    "supers": super_serializer.data
                }
            return Response(supers_dictionary, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = SuperSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def super_detail(request, pk):
    super = get_object_or_404(Super, pk=pk)

    if request.method == 'GET':
        serializer = SuperSerializer(super)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = SuperSerializer(super, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        super.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)