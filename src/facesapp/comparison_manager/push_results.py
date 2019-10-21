from django.http import JsonResponse
from ..models import Image as ImageModel, Comparison

def push_results(request):
    # push the result from comparisons table to App server
    matches = Comparison.objects.filter(sent_back=0)[:10]
    # print(matches)

    matches_list = []
    for match in matches:
        # print(match)
        # print(match.image) # the image
        # print(match.compared_image) # compared with
        # print('------------------')
        this_match = {
            'match_id': match.id,
            'image_id': match.image.id,
            'source': match.image.source,
            'source_id': match.image.source_id,
            'matches': {
                'image_id': match.compared_image.id,
                'source': match.compared_image.source,
                'source_id': match.compared_image.source_id
            },
            'face_distance': match.face_distance
        }
        #print(this_match)
        matches_list.append(this_match)


    #return JsonResponse(matches_list, status=200, safe=False)
    return JsonResponse({
        'message': 'Pending matches sent to server'
    }, status=200)