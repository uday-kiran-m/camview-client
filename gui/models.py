from django.db import models

# Create your models here.
class cams(models.Model):
    camname = models.CharField(max_length=50,blank=False,default='cam')
    note = models.TextField(max_length=200)
    url = models.CharField(max_length=100)
    online = models.BooleanField(default=False)
    errormsg = models.CharField(max_length=50,blank=True)

    def __str__(self) -> str:
        return self.camname
    class Meta:
        verbose_name_plural = "Cams"

    

