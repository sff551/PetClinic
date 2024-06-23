from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.hashers import check_password
from Administrative.models import Customer, Pet, Staff, Doctor,  Admin, TreatmentPet
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from Administrative.models import Pet
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt

def mainpage(request):
    return render (request, "mainpage.html")


def adminlogin(request):
    if request.method == 'POST':
        adminId1 = request.POST['adminId']
        adminPassword1 = request.POST['adminPassword']
        
        print(f"Admin ID: {adminId1}")  # Debugging line
        print(f"Provided Password: {adminPassword1}")
        # Authenticate admin
        try:
            admin = Admin.objects.get(adminId=adminId1)
            if check_password(adminPassword1, admin.adminPassword):
                request.session['adminId'] = admin.adminId
                request.session['adminName'] = admin.adminName
                if admin.last_login is not None:
                    request.session['lastLogin'] = admin.last_login.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    request.session['lastLogin'] = 'First login'  # Or any other appropriate message
                
                # Update last login time
                admin.last_login = timezone.now()
                admin.save()
                
                return redirect('adminhome')
            else:
                # Handle incorrect password
                context = {'message1': 'Incorrect password. Please try again.'}
        except Admin.DoesNotExist:
            # Handle admin not found
            context = {'message1': 'Admin ID not found. Please try again.'}
    
    return render(request, 'adminlogin.html')


def loginstaff(request):
    if request.method == 'POST':
        staffId1 = request.POST.get('staffId')
        staffPassword1 = request.POST.get('staffPassword')

        print(f"Staff ID: {staffId1}")  # Debugging line
        print(f"Provided Password: {staffPassword1}")
        try:
            # Fetch the staff member with the given ID
            staff_member = Staff.objects.get(staffId=staffId1)
            print(f"Stored Hashed Password: {staff_member.staffPassword}")

            # Check if the provided password matches the stored password
            if check_password(staffPassword1, staff_member.staffPassword):
                # Update the last login timestamp
                staff_member.last_login = timezone.now()
                staff_member.save()

                # Store staff information in session
                request.session['staffId'] = staff_member.staffId
                request.session['staffName'] = staff_member.staffName
                request.session['lastLogin'] = staff_member.last_login.strftime('%Y-%m-%d %H:%M:%S')

                # Redirect to the homepagestaff.html page upon successful login
                return redirect('homepagestaff')
            else:
                context = {'message1': 'Incorrect password. Please try again.'}
        except Staff.DoesNotExist:
            context = {'message1': 'Staff ID not found. Please try again.'}

        return render(request, "loginstaff.html", context)

    return render(request, "loginstaff.html", {'message1': ''})

def logindoctor(request):
    if request.method == 'POST':
        docId1 = request.POST['docId']
        docPassword1 = request.POST['docPassword']

        try:
            # Fetch the doctor with the given ID
            doctor_member = Doctor.objects.get(docId=docId1)

            # Check if the provided password matches the stored password
            if check_password(docPassword1, doctor_member.docPassword):
                # Update last login time
                doctor_member.last_login = timezone.now()
                doctor_member.save()

                # Store doctor information in session
                request.session['docId'] = doctor_member.docId
                request.session['docName'] = doctor_member.docName
                request.session['lastLogin'] = doctor_member.last_login.strftime('%Y-%m-%d %H:%M:%S')

                # Redirect to the homepagestaff.html page upon successful login
                return redirect('homepagedoctor')  # Redirect to the correct URL name for homepagedoctor.html
            else:
                context = {
                    'message1': 'Incorrect password. Please try again.'
                }
        except Doctor.DoesNotExist:
            context = {
                'message1': 'Doctor ID not found. Please try again.'
            }

        return render(request, "logindoctor.html", context)
    else:
        context = {
            'message1': ''
        }
    return render(request, "logindoctor.html", context)
    
def register_customer(request):
    if request.method == 'POST':
        custId = request.POST.get('customerId')
        custName = request.POST.get('customerName')
        custPassword = request.POST.get('customerPassword')
        custTelNo = request.POST.get('customerTel')
        custAdd = request.POST.get('customerAddress')
        custDateReg = request.POST.get('dateRegistered')

        # Hash the password before saving
        hashed_password = make_password(custPassword)
        customer = Customer(custId=custId, custName=custName, custPassword=hashed_password, custTelNo=custTelNo, custAdd=custAdd, custDateReg=custDateReg)
        customer.save()

        context = {'message': 'Register Customer Successful'}
        return render(request, 'regnewcust.html', context)

    return render(request, 'regnewcust.html')

def register_pet(request):
    customers = Customer.objects.all()
    if request.method == 'POST':
        petId = request.POST.get('petId')
        custId = request.POST.get('owner')  
        petName = request.POST.get('petName')
        petNeuterDate = request.POST.get('petNeuterDate')
        petVaccinationDate = request.POST.get('petVaccinationDate')
        petServiceName = request.POST.get('petServiceName')
        petServiceDateReceived = request.POST.get('petServiceDateReceived')

        try:
            customer = Customer.objects.get(custId=custId)
            try:
                pet = Pet.objects.get(petId=petId)
            except Pet.DoesNotExist:
                # If the Pet object doesn't exist, create a new one
                pet = Pet(petId=petId, custId=customer, petName=petName)
                pet.save()

            # Create or update PetInfo instance
            pet_info = Pet(
                custId=customer,
                petId=pet,
                petName=petName,
                petNeuterDate=petNeuterDate,
                petVaccinationDate=petVaccinationDate,
                petServiceName=petServiceName,
                petServiceDateReceived=petServiceDateReceived,
            )

            # Save pet_info instance
            pet_info.save()

            # Handle pet image upload if present
            if 'petImg' in request.FILES:
                pet_info.petImg = request.FILES['petImg']
                pet_info.save()

            context = {
                'message': 'Register Pet Successful.',
                'customers': customers
            }
            
        except Exception as e:
            print("Error during pet registration:", e)
            context = {
                'message': 'Register Pet Failed.',
                'error': str(e),
                'customers': customers
            }

        return render(request, 'regnewpet.html', context)

    else:
        context = {
            'customers': customers,
            'message': 'Registration Unsuccessful'
        }
        return render(request, 'regnewpet.html', context)


def pet_registration(request):
    customers = Customer.objects.all()  # Fetch all customer data
    context = {
        'customers': customers
    }
    print("Customers in context:", context['customers'])  # Debug output
    return render(request, 'regnewpet.html', context)


def success(request):
    return HttpResponse("Customer registered successfully!")

def logincust(request):
    if request.method == 'POST':
        custId1 = request.POST.get('custId')
        custPassword1 = request.POST.get('custPassword')

        try:
            customer = Customer.objects.get(custId=custId1)
            if check_password(custPassword1, customer.custPassword):
                request.session['customer_id'] = customer.custId
                request.session['customer_name'] = customer.custName
                return redirect('homepagecust')
            else:
                context = {'message': 'Incorrect password. Please try again.'}
        except Customer.DoesNotExist:
            context = {'message': 'Customer ID not found. Please try again.'}

        return render(request, "logincust.html", context)

    return render(request, "logincust.html")

def homepagecust(request):
    if 'customer_id' in request.session:
        customer_id = request.session['customer_id']
        customer_name = request.session['customer_name']
        
        # Retrieve pets associated with the logged-in customer
        pets = Pet.objects.filter(custId=customer_id)
        
        context = {
            'customer_id': customer_id,
            'customer_name': customer_name,
            'pets': pets  # Pass the pets queryset to the template
        }
        return render(request, "homepagecust.html", context)
    else:
        return redirect('logincust')
        
def homepagestaff(request):
    staffId = request.session.get('staffId')
    staffName = request.session.get('staffName')
    lastLogin = request.session.get('lastLogin')

    context = {
        'staffId': staffId,
        'staffName': staffName,
        'lastLogin': lastLogin
    }

    return render(request, "homepagestaff.html", context)


def adminhome(request):
    adminId = request.session.get('adminId')
    adminName = request.session.get('adminName')
    lastLogin = request.session.get('lastLogin')

    # Debugging output
    print(f'adminId: {adminId}, adminName: {adminName}, lastLogin: {lastLogin}')

    context = {
        'adminId': adminId,
        'adminName': adminName,
        'lastLogin': lastLogin,
    }

    return render(request, "adminhome.html", context)

def homepagedoctor(request):
    return render (request, "homepagedoctor.html")

def staff_list_of_customers(request):
    customers = Customer.objects.all()
    pets1 = Pet.objects.all()
    context = {'customers': customers, 'pets1': pets1}
    return render(request, 'stafflistofcust.html', context)

def staff_setting_page(request, cust_id):
    customer = get_object_or_404(Customer, custId=cust_id)
    context = {'customer': customer, 'cust_id': cust_id}  # Pass the cust_id to the template
    return render(request, 'staffsettingpage.html', context)

def save_customer_settings(request, cust_id):
    if request.method == 'POST':
        customer = get_object_or_404(Customer, custId=cust_id)
        customer.custName = request.POST.get('custName')
        customer.custTelNo = request.POST.get('custTelNo')
        customer.custAdd = request.POST.get('custAdd')
        customer.custDateReg = request.POST.get('custDateReg')
        customer.save()
        messages.success(request, 'Customer data updated successfully.')
        return redirect('staff_list_of_customers')

    return redirect('staff_list_of_customers')

def stafflistofcust(request):
    data1 = Customer.objects.all()
    pets1 = Pet.objects.select_related('custId').all()
    dict0={
        'data1': data1,
        'pets1':pets1,
    }
    return render(request, "stafflistofcust.html", dict0)

def pet_setting_page(request, pet_id):
    pet = get_object_or_404(Pet, petId=pet_id)
    context = {'pet': pet, 'pet_id': pet_id}
    return render(request, 'petsettingpage.html', context)

def save_pet_settings(request, pet_id):
    if request.method == 'POST':
        pet = get_object_or_404(Pet, petId=pet_id)
        pet.petName = request.POST.get('petName')
        pet.petNeuterDate = request.POST.get('petNeuterDate')
        pet.petVaccinationDate = request.POST.get('petVaccinationDate')
        pet.petServiceName = request.POST.get('petServiceName')
        pet.petServiceDateReceived = request.POST.get('petServiceDateReceived')
        pet.save()
        messages.success(request, 'Pet data updated successfully.')
        return redirect('staff_list_of_customers')
    return redirect('staff_list_of_customers')

def delete_pet(request, pet_id):
    pet = get_object_or_404(Pet, petId=pet_id)
    pet.delete()
    messages.success(request, 'Pet deleted successfully.')
    return redirect('staff_list_of_customers')

def delete_customer(request, cust_id):
    customer = get_object_or_404(Customer, custId=cust_id)
    customer.delete()
    messages.success(request, 'Customer deleted successfully.')
    return redirect('staff_list_of_customers')

def regnewcust(request):
    return render (request, "regnewcust.html")

def regnewpet(request):
    return render (request, "regnewpet.html") 

def petinfo(request):
    return render (request, "petinfo.html")

def sched_treatment(request):
    pets = Pet.objects.all()
    doctors = Doctor.objects.all()

    if request.method == 'POST':
        petId = request.POST.get('petId')
        docId = request.POST.get('docId')
        petServiceName = request.POST.get('petServiceName')
        petServiceDateReceived = request.POST.get('petServiceDateReceived')

        try:
            pet = Pet.objects.get(petId=petId)
            doctor = Doctor.objects.get(docId=docId)
            treatment = TreatmentPet(
                petId=pet,
                docId=doctor,
                petServiceName=petServiceName,
                petServiceDateReceived=petServiceDateReceived
            )
            treatment.save()
            context = {
                'message': 'Treatment Scheduled Successfully.',
                'pets': pets,
                'doctors': doctors
            }
        except Exception as e:
            context = {
                'message': 'Failed to Schedule Treatment.',
                'error': str(e),
                'pets': pets,
                'doctors': doctors
            }
        return render(request, 'schedtreatment.html', context)
    
    else:
        context = {
            'pets': pets,
            'doctors': doctors
        }
        return render(request, 'schedtreatment.html', context)

def list_customers_and_pets(request):
    customers = Customer.objects.all()
    pets = Pet.objects.select_related('custId').all()
    
    context = {
        'customers': customers,
        'pets': pets,
    }
    
    return render(request, 'listofcust.html', context)

def list_treatments(request):
    treatments = TreatmentPet.objects.select_related('petId', 'docId').all()
    
    context = {
        'treatments': treatments
    }
    
    return render(request, 'listtreatment.html', context)

def treatmentedit(request):
    treatments = TreatmentPet.objects.select_related('petId', 'docId').all()
    
    context = {
        'treatments': treatments
    }
    
    return render(request, 'treatmentedit.html', context)

def edit_treatment(request, treatment_id):
    treatment = get_object_or_404(TreatmentPet, pk=treatment_id)
    return render(request, 'edit_treatment.html', {'treatment': treatment})

def save_treatment(request, treatment_id):
    if request.method == 'POST':
        treatment = get_object_or_404(TreatmentPet, pk=treatment_id)
        treatment.petServiceName = request.POST.get('petServiceName')
        treatment.petServiceDateReceived = request.POST.get('petServiceDateReceived')
        treatment.save()
        return redirect('treatment_edit')
    return redirect('treatment_edit')

def delete_treatment(request, treatment_id):
    treatment = get_object_or_404(TreatmentPet, pk=treatment_id)
    treatment.delete()
    return redirect('treatment_edit')

def staff_doc_info(request):
    staffs = Staff.objects.all()
    doctors = Doctor.objects.all()
    return render(request, 'staffdocinfo.html', {'staffs': staffs, 'doctors': doctors})

# View to add new staff
def add_staff(request):
    if request.method == 'POST':
        staffId = request.POST.get('staffId')
        staffName = request.POST.get('staffName')
        staffPassword = make_password(request.POST.get('staffPassword'))
        Staff.objects.create(staffId=staffId, staffName=staffName, staffPassword=staffPassword)
        return redirect('staff_doc_info')

# View to add new doctor
def add_doctor(request):
    if request.method == 'POST':
        docId = request.POST.get('docId')
        docName = request.POST.get('docName')
        docPassword = make_password(request.POST.get('docPassword'))
        Doctor.objects.create(docId=docId, docName=docName, docPassword=docPassword)
        return redirect('staff_doc_info')

# View to edit staff
def edit_staff(request, staff_id):
    staff = get_object_or_404(Staff, pk=staff_id)
    if request.method == 'POST':
        staff.staffName = request.POST.get('staffName')
        if request.POST.get('staffPassword'):
            staff.staffPassword = make_password(request.POST.get('staffPassword'))
        staff.save()
        return redirect('staff_doc_info')
    return render(request, 'edit_staff.html', {'staff': staff})

# View to edit doctor
def edit_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, pk=doctor_id)
    if request.method == 'POST':
        doctor.docName = request.POST.get('docName')
        if request.POST.get('docPassword'):
            doctor.docPassword = make_password(request.POST.get('docPassword'))
        doctor.save()
        return redirect('staff_doc_info')
    return render(request, 'edit_doctor.html', {'doctor': doctor})

# View to delete staff
def delete_staff(request, staff_id):
    staff = get_object_or_404(Staff, pk=staff_id)
    staff.delete()
    return redirect('staff_doc_info')

# View to delete doctor
def delete_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, pk=doctor_id)
    doctor.delete()
    return redirect('staff_doc_info')
