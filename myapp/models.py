from django.db import models

# Create your models here.
class InvitationCode(models.Model):
  code = models.CharField(verbose_name="Invitation Code", max_length=10, unique=True)
  expire = models.DateTimeField(verbose_name="Expire Time")
  
  def __str__(self):
    return self.code
