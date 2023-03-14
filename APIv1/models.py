from django.db import models

# Create your models here.


class Website(models.Model):
    # name = models.CharField(max_length=30)
    url = models.CharField(max_length=200)
    pdf = models.FileField(upload_to="APIv1/uploadedPdf/")
    textFilePath = models.CharField(max_length=300)
    summaryFilePath = models.CharField(max_length=300)


class Sentences(models.Model):
    sentenceText = models.CharField(max_length=100)
    selected = models.BooleanField(default=False)
    website = models.ForeignKey(Website,on_delete=models.CASCADE)
