from django.db import models

# Create your models here.
class Meet(models.Model):
     sno= models.AutoField(primary_key=True)
     code=models.CharField(max_length=15)
     status=models.BooleanField(default=False)

     def __str__(self):
          return self.code


class Message(models.Model):
     sno= models.AutoField(primary_key=True)
     content= models.TextField()
     code=models.CharField(max_length=15)
     meet=models.ForeignKey(Meet, on_delete=models.CASCADE)

     def __str__(self):
          return self.content[0:15]



class Buffer(models.Model):
     sno= models.AutoField(primary_key=True)
     content= models.TextField()
     code=models.CharField(max_length=15)
     meet=models.ForeignKey(Meet, on_delete=models.CASCADE)

     def __str__(self):
          return self.content[0:15]