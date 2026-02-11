from django.db import models


class Voter(models.Model):
    full_name = models.CharField(max_length=100)
    guardian = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    dob = models.DateField()
    nationality = models.CharField(max_length=50)
    constituency = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    has_voted = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Candidate(models.Model):
    name = models.CharField(max_length=100)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.name
