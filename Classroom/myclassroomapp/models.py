from django.db import models

# Create your models here.


class UserReg(models.Model):
    Name = models.CharField(max_length=50)
    Phone = models.CharField(max_length=13)
    Email = models.CharField(max_length=50)
    Password = models.CharField(max_length=50)

class modulereg(models.Model):
    Userid =models.ForeignKey(UserReg,related_name='M_User_id',on_delete=models.CASCADE)
    #Subject = models.CharField(max_length=50)
    Module_number = models.IntegerField()
    Module_title = models.CharField(max_length=50)

class notereg(models.Model):
    Userid = models.ForeignKey(UserReg, related_name='N_User_id', on_delete=models.CASCADE)
    moduleid = models.ForeignKey(modulereg, related_name='N_Module_id', on_delete=models.CASCADE)
    Note_title = models.CharField(max_length=50)
    notefile = models.FileField(upload_to='documents/')