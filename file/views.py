from .models import File
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from .serializers import FileSerializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser


class Files(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
            data = request.data['data']
            store=request.user.store
            new_file=File(store=store)
            file_serializer = FileSerializers(new_file,data=data)
            if file_serializer.is_valid():
                    file_serializer.save()
                    return Response(file_serializer.data, status=status.HTTP_201_CREATED)

            else:
                return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        store = request.user.store
        if request.user.is_superuser:
            all_medias = File.objects.filter(store__isnull=True)
        else:
            all_medias = File.objects.filter(store=store)
        media_serializer = FileSerializers(all_medias, many=True)
        return Response(media_serializer.data, status=status.HTTP_201_CREATED)

   
class RemoveFiles(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = request.data['data']
        File.objects.filter(pk__in=data).delete()
        return Response('Success', status=status.HTTP_201_CREATED)
