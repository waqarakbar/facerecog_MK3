from django.http import JsonResponse
from ..models import Image as ImageModel, Comparison
import requests
import json
from django.conf import settings

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
            'comparison_id': match.id,
            'image_id': match.image.id,
            'attachment_source_id': match.image.source,
            'source_entity_id': match.image.source_id,
            'attachment_id': match.image.attachment_id,
            'matched_image_id': match.compared_image.id,
            'matched_attachment_source_id': match.compared_image.source,
            'matched_source_entity_id': match.compared_image.source_id,
            'matched_attachment_id': match.compared_image.attachment_id,
            'face_distance': match.face_distance
        }
        # print(this_match)
        matches_list.append(this_match)

        # change the status
        match.sent_back = 1
        match.save()


    # push the results to MBAlert server
    url = settings.PUSH_MATCHES_URL
    headers = {'Content-Type': 'application/json', 'Token': settings.MBALERT_SERVER_TOKEN}
    r = requests.post(url, data=json.dumps(matches_list), headers=headers)
    # print(r.text)
    # print(matches_list)

    # return JsonResponse(matches_list, status=200, safe=False)
    return JsonResponse({
        'message': 'Pending matches sent to server',
        'response': r.text
    }, status=200)