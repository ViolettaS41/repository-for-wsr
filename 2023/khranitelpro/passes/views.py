import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from .models import PassRequest, Department, Employee
from datetime import datetime,timedelta

class PassRequestView(View):
    def get(self, request):
        passes = PassRequest.objects.all().vales()
        return JsonResponse(list(passes), safe=True)

    def post(self, request):
        try:
            data = json.load(request.body)

            visit_date = datetime.strptime(data.get('visit_date'), '%Y-%m-%d').date()
            if visit_date < datetime.today().date() + timedelta(days=1) or visit_date>datetime.today().date()+timedelta(days=15):
                return JsonResponse({'error': "Дата должна быть между завтра и 15 днями вперед"}, status=400)

            birth_date = datetime.strptime(data.get('bith_date'), '%Y-%m-%d').date()
            if (datetime.today().date() - birth_date).days/365<16:
                return JsonResponse({"error": 'Возраст посетителя должен быть не менее 16 лет'}, status=400)


            department = Department.objects.get(id=data.get('department_id'))
            employee = Employee.objects.get(id=data.get('employee_id'))
            pass_request = PassRequest.objects.create(
                visitor_first_name = data.get('visitor_first_name'),
                visitor_last_name=data.get('visitor_last_name'),
                visit_date = data.get('visit_date'),
                department=department,
                employee=employee,
                phone=data.get('phone'),
                email=data.get('email'),
                passport_series=data.get('passport_series'),
                passport_number=data.get('passport_number'),
                note=data.get('note'),
            )
            return JsonResponse({"id": pass_request.id, "status":"created"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

def index(request):
    return render(request, 'index.html')

def pass_request_form(request):
    if request.method == "POST":
        visitor_first_name = request.POST['visitor_first_name']
        visitor_last_name = request.POST['visitor_last_name']
        visit_date = request.POST['visit_date']
        department_id = request.POST['department_id']
        employee_id = request.POST['employee_id']

        department = Department.objects.get(id=department_id)
        employee = Employee.objects.get(id=employee_id)

        PassRequest.objects.create(
            visitor_first_name=visitor_first_name,
            visitor_last_name = visitor_last_name,
            visit_date = visit_date,
            department = department,
            employee=employee

        )
        return redirect('index')

    departments = Department.objects.all()
    return render(request, 'pass_request_form.html')#, {'departments': departments})
