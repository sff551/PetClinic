from django.contrib import admin
from.models import Customer, Pet, Staff, Doctor, Admin

# Register your models here.

admin.site.register(Customer)
admin.site.register(Pet)
admin.site.register(Staff)
admin.site.register(Doctor)
admin.site.register(Admin)