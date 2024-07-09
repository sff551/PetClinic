from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password

class Customer(models.Model):
    custId = models.CharField(max_length=50, primary_key=True)
    custPassword = models.TextField(max_length=128)
    custName = models.TextField(max_length=100)
    custTelNo = models.CharField(max_length=15)
    custAdd = models.TextField(max_length=128)
    custDateReg = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk: 
            self.custPassword = make_password(self.custPassword)
        super(Customer, self).save(*args, **kwargs)

class Pet(models.Model):
    petId=models.CharField(max_length=50, primary_key=True)
    custId=models.ForeignKey(Customer, on_delete=models.CASCADE)
    petImg = models.ImageField(upload_to='petImage/', blank=True, null=True) 
    petName=models.TextField(max_length=100)
    petNeuterDate=models.DateField(blank=True, null=True)
    petVaccinationDate=models.DateField(blank=True, null=True)
    petServiceName=models.TextField(max_length=100, null=True)
    petServiceDateReceived=models.DateField(blank=True, null=True)

class Staff(models.Model):
    staffId = models.CharField(max_length=50, primary_key=True)
    staffName = models.TextField(max_length=100)
    staffPassword = models.TextField(max_length=128)
    last_login = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk or self._state.adding or self._password_changed():
            self.staffPassword = make_password(self.staffPassword)
        super().save(*args, **kwargs)

    def _password_changed(self):
        """
        Helper method to check if the password has changed.
        """
        if self.pk:
            try:
                old_instance = Staff.objects.get(pk=self.pk)
                return self.staffPassword != old_instance.staffPassword
            except Staff.DoesNotExist:
                return True
        return True

class Doctor(models.Model):
    docId=models.CharField(max_length=50, primary_key=True)
    docName=models.TextField(max_length=100)
    docPassword=models.TextField(max_length=100)
    last_login = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk or self._state.adding or self._password_changed():
            self.docPassword = make_password(self.docPassword)
        super().save(*args, **kwargs)

    def _password_changed(self):
        """
        Helper method to check if the password has changed.
        """
        if self.pk:
            try:
                old_instance = Doctor.objects.get(pk=self.pk)
                return self.docPassword != old_instance.docPassword
            except Doctor.DoesNotExist:
                return True
        return True 

class Admin(models.Model):
    adminId = models.CharField(max_length=50, primary_key=True)
    adminName = models.TextField(max_length=100)
    adminPassword = models.TextField(max_length=128)
    last_login = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk or self._state.adding or self._password_changed():
            self.adminPassword = make_password(self.adminPassword)
        super().save(*args, **kwargs)

    def _password_changed(self):
        """
        Helper method to check if the password has changed.
        """
        if self.pk:
            try:
                old_instance = Admin.objects.get(pk=self.pk)
                return self.adminPassword != old_instance.adminPassword
            except Admin.DoesNotExist:
                return True 
        return True

class TreatmentPet(models.Model):
    petId = models.ForeignKey(Pet, on_delete=models.CASCADE)
    docId=models.ForeignKey(Doctor, on_delete=models.CASCADE)
    petServiceName=models.TextField(max_length=100, null=True)
    petServiceDateReceived=models.DateField(blank=True, null=True)

