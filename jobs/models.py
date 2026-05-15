from django.db import models
from accounts.models import User

class Job(models.Model):
    title = models.CharField(max_length=200)
    desc = models.TextField()

    salary = models.CharField(max_length=100, null=True, blank=True)
    vacancy = models.IntegerField(null=True, blank=True)

    deadline = models.DateField()

    hr_email = models.EmailField(null=True, blank=True)
    hr_mobile = models.CharField(max_length=15, null=True, blank=True)
    hr_name = models.CharField(max_length=100, null=True, blank=True)

    company_website = models.URLField(null=True, blank=True)

    job_type = models.CharField(max_length=100)
    experience = models.FloatField()

    company_location = models.CharField(max_length=200)

    isActive = models.BooleanField(default=True)

    photo = models.ImageField(upload_to='jobs/', null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)