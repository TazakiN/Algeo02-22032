from django.db import models


class Image(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="images/", max_length=500)

    def __str__(self):
        return self.name


class Dataset(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="dataset/")
    contrast = models.FloatField(
        default=0.0
    )  # Tambahkan ini jika data Anda adalah float
    homogeneity = models.FloatField(
        default=0.0
    )  # Tambahkan ini jika data Anda adalah float
    entropy = models.FloatField(
        default=0.0
    )  # Tambahkan ini jika data Anda adalah float

    def __str__(self):
        return self.name
