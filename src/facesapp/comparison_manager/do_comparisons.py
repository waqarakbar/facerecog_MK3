from django.db.models import F
from ..models import Image as ImageModel, Comparison
import numpy as np
import face_recognition
from django.conf import settings
from django.http import JsonResponse

def do_comparisons(request):
    # get 10 images which have not been fully processed (unknown images) - compared_till_id > current_comparison_id
    images = ImageModel.objects.filter(compare_till_id__gt=F('current_comparison_id'))[:10]

    for current_img in images:

        # load current image (unknown) - loading image in real time - too slow
        # current_image_loaded = face_recognition.load_image_file(str(settings.MEDIA_ROOT) + "/" + str(current_img.path))
        # unknown_face_encodings = face_recognition.face_encodings(current_image_loaded)[0]

        # that blob thingy, get encodings from already saved in DB
        unknown_face_encodings = np.fromstring(current_img.features_encoding)
        # print(unknown_face_encodings)
        # print(type(unknown_face_encodings))


        # get images with IDs b/w current_comparison_id and compare_till_date of the current_image
        # apply some limit to keep the things cool
        # each iteration will increase current_comparison_id and once it is equal to compare_till_id
        # of the current_image, then this current_image will be skipped in next cycle
        comp_images = ImageModel.objects.filter(id__gt=current_img.current_comparison_id, id__lte=current_img.compare_till_id).exclude(source_id=current_img.source_id)[:10]

        print(current_img)
        print(comp_images)

        # loop the known images (comp_images) and compare each with current_image (unknown)
        last_compared_id = 0
        for comp_curr_img in comp_images:

            # load comparison image (known), realtime but very slow
            # comp_curr_img_load = face_recognition.load_image_file(str(settings.MEDIA_ROOT)+"/"+str(comp_curr_img.path))
            # cke = face_recognition.face_encodings(comp_curr_img_load)[0]

            # load the encodings fro DB, saved as blob
            cke = np.fromstring(comp_curr_img.features_encoding)
            # print(cke)
            # print(type(cke))
            known_face_encodings = [
                cke
            ]

            face_distances = face_recognition.face_distance(known_face_encodings, unknown_face_encodings)
            # print(face_distances)

            # if the distance b/w the two are in acceptable range, then save
            # the references in comparisons table
            if face_distances[0] <= settings.ACCEPTABLE_FACE_DISTANCE:
                # face distance matches our criteria of minimum value, save the match
                comparison = Comparison()
                comparison.image_id = current_img.id
                comparison.compared_image_id = comp_curr_img.id
                comparison.face_distance = face_distances[0]
                comparison.sent_back = 0
                comparison.save()

            last_compared_id = comp_curr_img.id

        # update the current_comparison_id of original image (current_image)
        current_img.current_comparison_id = last_compared_id
        current_img.save()
        # print(current_img)

    return JsonResponse({
        'message': 'Current cycle completed'
    }, status=200)