from django.db import models

# Create your models here.
class Meet(models.Model):
     sno= models.AutoField(primary_key=True)
     code=models.CharField(max_length=15)

     def __str__(self):
          return self.code


class Messages(models.Model):
     sno= models.AutoField(primary_key=True)
     content=models.CharField(max_length=500)
     meet=models.ForeignKey(Meet, on_delete=models.CASCADE)

     def __str__(self):
          return self.content



