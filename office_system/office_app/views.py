from django.shortcuts import render
from django.http import HttpResponse
from . models import Employee, Role, Department 
import datetime
from django.db.models import Q

# Create your views here.

def index(request):
    # return HttpResponse('helo i am wakar')
    return render(request, 'index.html')

def view_all_emp(request):
    emps = Employee.objects.all()
    context = {
        'emps' : emps
    }
    print(context)
    return render(request, 'view_all_emp.html', context)

def add_emp(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        salary = int(request.POST['salary'])
        role = request.POST['role']
        phone_no = int(request.POST['phone'])
        bonus = int(request.POST['bonus'])
        dept = request.POST['dept']
        hire_date = request.POST['hire_date']
        new_emp = Employee(first_name=first_name, last_name=last_name, salary=salary, role_id=role, phone=phone_no, bonus=bonus, dept_id=dept, hire_date= hire_date)
        new_emp.save()
        return HttpResponse('Employee added successfully')

    elif request.method == 'GET':
      
        context = {'roles': Role.objects.all(), 'depts': Department.objects.all()}
        return render(request, 'add_emp.html', context)

    else:   
        return HttpResponse("An Exception Occured! Employee Has Not Been Added")

def remove_emp(request, emp_id = 0):
    if emp_id:
      try:
        emp_to_be_removed = Employee.objects.get(id=emp_id)
        emp_to_be_removed.delete()
        return HttpResponse("Employee Removed Successfully")
      except Employee.DoesNotExist:
        return HttpResponse("Please enter a valid employee id") 
    emps = Employee.objects.all() 
    context = {
        'emps': emps 
    } 
    return render(request, 'remove_emp.html', context)

def filter_emp(request):
    if request.method == 'POST':
       name = request.POST['name']
       role = request.POST['role']
       dept = request.POST['dept']
       emps = Employee.objects.all()
       if name:
          emps = emps.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
       if role:
          emps = emps.filter(role__name__icontains = role)
       if dept:
          emps = emps.filter(dept__name__icontains = dept)

       context = {   
            'emps': emps 
         }
    
       return render(request, 'view_all_emp.html', context)

    elif request.method == 'GET':
        return render(request, 'filter_emp.html')
    else:
       return HttpResponse("An Exception Occured")
       

