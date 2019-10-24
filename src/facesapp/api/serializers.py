from rest_framework import serializers
from ..models import Image as ImageModel

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageModel
        fields = ['id', 'source', 'source_id', 'attachment_id', 'title', 'path', 'features_encoding', 'compare_till_id', 'current_comparison_id', 'created_at', 'updated_at']