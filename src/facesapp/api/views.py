from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes, parser_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FileUploadParser, FormParser
from ..models import Image as ImageModel
from ..api.serializers import ImageSerializer

import face_recognition
from PIL import Image, ImageDraw
import numpy as np
import os
from django.conf import settings


@api_view(['GET',])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated,))
@parser_classes((FileUploadParser, FormParser,))
def images(request):
    # List all images, or create a new snippet
    # print(request.data)
    images = ImageModel.objects.all()
    serializer = ImageSerializer(images, many=True)
    return Response(serializer.data)


@api_view(['POST',])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated,))
def new_image(request):
    # Receive encode and save new image to db
    serializer = ImageSerializer(data=request.data)
    if serializer.is_valid():
        image = serializer.save()

        # the image is saved, lets create the encodings of this image
        this_image = face_recognition.load_image_file(settings.MEDIA_ROOT + "/" + str(image.path))
        this_image_face_encoding = face_recognition.face_encodings(this_image)[0]

        # testing the blob thing for encoding
        encoding_blob = np.array(this_image_face_encoding)
        # print(encoding_blob)

        image.features_encoding = encoding_blob

        # compare till ID, xi-1
        image.compare_till_id = image.id-1

        image.save()

        return JsonResponse(serializer.data, status=201)

    return JsonResponse(serializer.errors, status=400)

