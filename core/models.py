from django.db import models
from django.contrib.auth.models import User

class Organ(models.Model):
    organ_id = models.AutoField(primary_key=True)
    organ_name = models.CharField(max_length=50)

    def __str__(self):
        return self.organ_name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

class Donor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    organ = models.ForeignKey(Organ, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    blood_group = models.CharField(max_length=5)

    # Both fields REQUIRED now!
    aadhar_image = models.FileField(upload_to='aadhar_images/', null=False, blank=False)
    blood_report = models.FileField(upload_to='blood_reports/', null=False, blank=False)

    contact = models.CharField(max_length=15)
    matched = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    cancelled = models.BooleanField(default=False)
    cancelled_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        organ_name = self.organ.organ_name if self.organ else "No Organ"
        return f"{self.name} ({organ_name})"

class Recipient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    organ = models.ForeignKey(Organ, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    blood_group = models.CharField(max_length=5)

    # Both fields REQUIRED now!
    aadhar_image = models.FileField(upload_to='aadhar_images/', null=False, blank=False)
    blood_report = models.FileField(upload_to='blood_reports/', null=False, blank=False)

    contact = models.CharField(max_length=15)
    matched = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    cancelled = models.BooleanField(default=False)
    cancelled_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        organ_name = self.organ.organ_name if self.organ else "No Organ"
        return f"{self.name} ({organ_name})"

class MatchedTransplantation(models.Model):
    transplantation_id = models.AutoField(primary_key=True)
    donor_name = models.CharField(max_length=100)
    recipient_name = models.CharField(max_length=100)
    organ = models.ForeignKey(Organ, on_delete=models.SET_NULL, null=True, blank=True)
    donor_blood_group = models.CharField(max_length=5)
    recipient_blood_group = models.CharField(max_length=5)
    matched_on = models.DateTimeField(auto_now_add=True)
    donor = models.ForeignKey('Donor', on_delete=models.SET_NULL, null=True, blank=True)
    recipient = models.ForeignKey('Recipient', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        organ_name = self.organ.organ_name if self.organ else "No Organ"
        return (
            f"Transplant {self.transplantation_id}: "
            f"{self.donor_name} ({self.donor_blood_group}) -> "
            f"{self.recipient_name} ({self.recipient_blood_group}) [{organ_name}]"
        )

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notif_type = models.CharField(max_length=20, default='info')
    message = models.TextField()
    donor = models.ForeignKey(Donor, on_delete=models.SET_NULL, null=True, blank=True)
    recipient = models.ForeignKey(Recipient, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"To {self.user.username}: {self.notif_type} [{self.created_at:%Y-%m-%d %H:%M}]"

class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.name} <{self.email}> @ {self.created_at.date().isoformat()}"
