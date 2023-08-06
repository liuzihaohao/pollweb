from django.db import models
from django.contrib.auth.models import User

# Create your models here.

Grade=(
    ('A','public_disclosure'),
    ('B','partial_disclosure'),
    ('C','internal_disclosure'),
    ('D','partial_internal_disclosure'),
    ('E','internal_confidentiality'),
    ('F','strictly_confidential'),
    ('G','system_confidentiality'),
)

Grade_U=(
    ('A','public'),
    ('B','public_to_staff'),
    ('C','secrecy'),
)

class Activity(models.Model):
    id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=100)
    text=models.TextField()
    admins=models.ManyToManyField('auth.User',related_name="alladmins")
    start_time=models.DateTimeField()
    end_time=models.DateTimeField()
    public_grade=models.CharField(max_length=1,choices=Grade)
    is_all_registered=models.BooleanField()
    registered_list=models.ManyToManyField('auth.User',related_name="allregistered",null=True)
    question_list=models.TextField()
    create_data=models.DateTimeField(auto_now_add=True)
    last_change_data=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField()
    def __str__(self):
        ordering = ['-start_time']
        return self.title

class Result(models.Model):
    id=models.AutoField(primary_key=True)
    from_user=models.ForeignKey('auth.User',on_delete=models.CASCADE)
    from_activity=models.ForeignKey('Activity',on_delete=models.CASCADE)
    answer_list=models.TextField()
    public_grade_u=models.CharField(max_length=1,choices=Grade_U)
    create_data=models.DateTimeField(auto_now_add=True)
    last_change_data=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title