from django.urls import path
from . import views 
from .views import register_customer, staff_list_of_customers, staff_setting_page, save_customer_settings

urlpatterns = [
    path("", views.mainpage, name="mainpage"),
    path('loginstaff/', views.loginstaff, name="loginstaff"),
    path('logindoctor/', views.logindoctor, name="logindoctor"),
    path("logincust/", views.logincust, name="logincust"),
    path("homepagecust/", views.homepagecust, name="homepagecust"),
    path("homepagestaff/", views.homepagestaff, name="homepagestaff"),
    path("homepagedoctor/", views.homepagedoctor, name="homepagedoctor"),
    path("stafflistofcust/", views.stafflistofcust, name="stafflistofcust"),
    path('schedtreatment/', views.sched_treatment, name='sched_treatment'),
    path("regnewcust/", views.regnewcust, name="regnewcust"),
    path("regnewpet/", views.regnewpet, name="regnewpet"),
    path("petinfo/", views.petinfo, name="petinfo"),
    path('register/', views.register_customer, name='register_customer'),
    path("reggisterpet/", views.register_pet, name="register_pet"),
    path('success/', views.success, name='success'),
    path('adminlogin/', views.adminlogin, name='adminlogin'),
    path('adminhome/', views.adminhome, name='adminhome'),
    path('register_pet/', views.register_pet, name='register_pet'),
    path('listofcust/', views.list_customers_and_pets, name='list_customers_and_pets'),
    path('listtreatment/', views.list_treatments, name='list_treatment'),
    path('stafflistofcust/', views.staff_list_of_customers, name='staff_list_of_customers'),
    path('staffsettingpage/<str:cust_id>/', views.staff_setting_page, name='staff_setting_page'),
    path('savecustomersettings/<str:cust_id>/', views.save_customer_settings, name='save_customer_settings'),
    path('deletecustomer/<str:cust_id>/', views.delete_customer, name='delete_customer'),
    path('petsettingpage/<str:pet_id>/', views.pet_setting_page, name='pet_setting_page'),
    path('savepetsettings/<str:pet_id>/', views.save_pet_settings, name='save_pet_settings'),
    path('deletepet/<str:pet_id>/', views.delete_pet, name='delete_pet'),
    path('treatmentedit/', views.treatmentedit, name='treatmentedit'),
    path('edit_treatment/<int:treatment_id>/', views.edit_treatment, name='edit_treatment'),
    path('save_treatment/<int:treatment_id>/', views.save_treatment, name='save_treatment'),
    path('delete_treatment/<int:treatment_id>/', views.delete_treatment, name='delete_treatment'),
    path('staffdocinfo/', views.staff_doc_info, name='staff_doc_info'),
    path('add_staff/', views.add_staff, name='add_staff'),
    path('add_doctor/', views.add_doctor, name='add_doctor'),
    path('edit_staff/<str:staff_id>/', views.edit_staff, name='edit_staff'),
    path('edit_doctor/<str:doctor_id>/', views.edit_doctor, name='edit_doctor'),
    path('delete_staff/<str:staff_id>/', views.delete_staff, name='delete_staff'),
    path('delete_doctor/<str:doctor_id>/', views.delete_doctor, name='delete_doctor'),
]