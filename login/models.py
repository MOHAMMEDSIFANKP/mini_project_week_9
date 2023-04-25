from django.db import models

# Create your models here.


class card(models.Model):
    brand = models.CharField(max_length=10)
    model = models.CharField(max_length=10)
    image = models.ImageField(upload_to='mobile_image')
    price = models.CharField(max_length=50)
    
    def __str__(self) -> str:
        return self.brand + ' -' + self.model