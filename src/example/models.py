from django.db import models


class ImageQuery(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="images/", max_length=500)

    def __str__(self):
        return self.name


class Dataset(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="dataset/")
    # data texture
    contrast = models.FloatField(default=0.0)
    homogeneity = models.FloatField(default=0.0)
    entropy = models.FloatField(default=0.0)
    energy = models.FloatField(default=0.0)
    correlation = models.FloatField(default=0.0)
    # data color
    h0 = models.IntegerField(default=0)
    h1 = models.IntegerField(default=0)
    h2 = models.IntegerField(default=0)
    h3 = models.IntegerField(default=0)
    h4 = models.IntegerField(default=0)
    h5 = models.IntegerField(default=0)
    h6 = models.IntegerField(default=0)
    h7 = models.IntegerField(default=0)
    s0 = models.FloatField(default=0.0)
    s1 = models.FloatField(default=0.0)
    s2 = models.FloatField(default=0.0)
    v0 = models.FloatField(default=0.0)
    v1 = models.FloatField(default=0.0)
    v2 = models.FloatField(default=0.0)

    def __str__(self):
        return self.name
