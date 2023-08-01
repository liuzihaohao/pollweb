from django.db import models

# Create your models here.

class Log(models.Model):
    id=models.AutoField(primary_key=True)
    from_user=models.ForeignKey('auth.User',on_delete=models.DO_NOTHING)
    from_obj=models.TextField()
    do_type=models.CharField(max_length=50)
    create_data=models.DateTimeField()
    class Meta:
        ordering = ['-create_data']