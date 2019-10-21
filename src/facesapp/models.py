from django.db import models

# Create your models here.

class Image(models.Model):
    """" Model representing the images received from MBAlert app server """
    IMAGE_SOURCES = (
        (1, 'Incidents'),
        (2, 'Children'),
        (3, 'Activities'),
        (4, 'Comments'),
    )

    source = models.IntegerField(
        choices=IMAGE_SOURCES,
        default=1
    )
    source_id = models.BigIntegerField()
    title = models.CharField(max_length=255, null=True)
    path = models.ImageField()
    features_encoding = models.BinaryField(null=True)
    compare_till_id = models.BigIntegerField(default=0)
    current_comparison_id = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.title


class Comparison(models.Model):
    """ Model to store image comparisons with other iamges """

    # id of the image (main entity)
    image = models.ForeignKey(Image, on_delete=models.DO_NOTHING, null=True, related_name='image')

    # id of the image to which it is being compared
    compared_image = models.ForeignKey(Image, on_delete=models.DO_NOTHING, null=True, related_name='compared_with')

    # distance value from comparison
    face_distance = models.CharField(null=True, max_length=20)

    # sent back to server
    sent_back = models.BooleanField()

    # reply by server
    reply_by_server = models.TextField(null=True, default='NULL')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id} - {self.image.title} (compared with {self.compared_image.title})'


