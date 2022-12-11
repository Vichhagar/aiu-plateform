from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_TYPE = [
        ('admin', 'admin'),
        ('official', 'official'),
        ('normal', 'normal')
    ]
    profileImage = models.ImageField(upload_to='images/', null=True, blank=True)
    userType = models.CharField(max_length=10, choices=USER_TYPE, default='normal')
    userBio = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class Activity(models.Model):
    activityOrganizer = models.ForeignKey(User, on_delete=models.CASCADE)
    activityTitle = models.CharField(max_length=50)
    activityLocation = models.CharField(max_length=100)
    activityDiscription = models.TextField()
    activityDate = models.DateTimeField()
    activityOpenDate = models.DateTimeField()
    activityCloseDate = models.DateTimeField()

    def __str__(self):
        return f"{self.activityTitle} organized by {self.activityOrganizer}"

class ActivityParticepationList(models.Model):
    class Meta:
        unique_together = (('userID', 'activityID'),)

    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    activityID = models.ForeignKey(Activity, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.userID} join {self.activityID}"