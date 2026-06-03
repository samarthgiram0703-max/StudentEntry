from django.shortcuts import render, redirect, get_object_or_404
from base.models import Student

# Create your views here.
def home(request):
    students = Student.objects.all()
    
    name = request.GET.get('name')
    age = request.GET.get('age')
    grade = request.GET.get('grade')
    gender = request.GET.get('gender')
    location = request.GET.get('location')
    
    if name:
        students = students.filter(name__icontains=name)
    if age:
        students = students.filter(age=age)
    if grade:
        students = students.filter(grade__iexact=grade)
    if gender:
        students = students.filter(gender__iexact=gender)
    if location:
        students = students.filter(location__icontains=location)
        
    return render(request, 'home.html', {'students': students})

def add_student(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        grade = request.POST.get('grade')
        gender = request.POST.get('gender')
        mobile_number = request.POST.get('mobile_number')   
        location = request.POST.get('location')
        student = Student(name=name, age=age, grade=grade, gender=gender, mobile_number=mobile_number, location=location)
        student.save()
        return redirect('home')
    return render(request, 'add.html')

def update_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        student.name = request.POST.get('name')
        student.age = request.POST.get('age')
        student.grade = request.POST.get('grade')
        student.gender = request.POST.get('gender')
        student.mobile_number = request.POST.get('mobile_number')
        student.location = request.POST.get('location')
        student.save()
        return redirect('home')
    return render(request, 'update.html', {'student': student})

def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        student.delete()
        return redirect('home')
    return render(request, 'delete.html', {'student': student})