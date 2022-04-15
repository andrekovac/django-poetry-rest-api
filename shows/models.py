from django.db import models


class Show(models.Model):
    """
    A 90s TV show
    """
    title = models.CharField(max_length=40, unique=True)
    album_name = models.CharField(max_length=60)
    duration = models.FloatField()
    year = models.FloatField()
    artist = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Formats entries in the Admin panel"""
        return f'{self.title} - {self.artist}'
