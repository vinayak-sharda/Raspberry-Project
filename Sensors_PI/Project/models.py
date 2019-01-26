from django.db import models

class Project(models.Model):
	photo = models.ImageField(upload_to="")

