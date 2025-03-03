from django.db import models
from accounts.models import User


class Skill(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["name"]


class Candidate(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="candidate_profile",
        primary_key=True,
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    # phone_number = models.CharField(max_length=20)
    about = models.TextField(blank=True)
    skills = models.ManyToManyField(Skill, related_name="candidates", blank=True)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.get_full_name()


class Experience(models.Model):
    candidate = models.ForeignKey(
        Candidate, on_delete=models.CASCADE, related_name="experiences"
    )
    company_name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True)
    is_current = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.candidate.get_full_name()} - {self.company_name}"
    
    class Meta:
        ordering = ["-start_date"]


class Education(models.Model):
    candidate = models.ForeignKey(
        Candidate, on_delete=models.CASCADE, related_name="educations"
    )
    institution_name = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True)
    is_current = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.candidate.get_full_name()} - {self.institution_name}"
    
    class Meta:
        ordering = ["-start_date"]
