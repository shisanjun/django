from django.db import models

# Create your models here.

class HostGroup(models.Model):
    name=models.CharField(max_length=32)

class Host(models.Model):
    hostname=models.CharField(max_length=32)
    ip=models.GenericIPAddressField(protocol="ipv4")
    port=models.IntegerField()
    cabinet=models.CharField(max_length=32)
    ctime=models.DateField()
    hostinfo=models.CharField(max_length=64)
    group=models.ForeignKey(to="HostGroup",to_field="id",default=1)

class UserGroup(models.Model):
    name=models.CharField(max_length=32)

class User(models.Model):
    username=models.CharField(max_length=32)
    password=models.CharField(max_length=32)
    user_group=models.ForeignKey(to="UserGroup",to_field="id")
    hosts=models.ManyToManyField("Host")
