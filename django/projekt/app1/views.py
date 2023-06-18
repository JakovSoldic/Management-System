from django.shortcuts import render, redirect
from .form import CustomUserCreationForm, SubjectForm, StudentUpdateForm, ProfessorUpdateForm, EnrollmentForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Subject, User, Enrollment, Role
from django.shortcuts import get_object_or_404

# Create your views here.
def is_admin(user):
    admin_role = Role.objects.get(role='admin')
    return user.role == admin_role

def is_student(user):
    student_role = Role.objects.get(role='student')
    return user.role == student_role

def is_professor(user):
    professor_role = Role.objects.get(role='professor')
    return user.role == professor_role

@user_passes_test(is_admin)
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if user.role.role == 'admin':
                user.is_superuser = True
                user.is_staff = True
            user.save()
            return redirect('/main_page_admin')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'register.html', context)

def authenticate_user(email, password):
    User = get_user_model()
    try:
        user = User.objects.get(email=email)
        if user.check_password(password):
            return user
    except User.DoesNotExist:
        return None

def home(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email, password)

        user = authenticate_user(email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/main')
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'home.html')

@login_required
def main(request):
    user = request.user

    if user.is_authenticated:
        role = user.role

        if role.role == 'admin':
            return redirect('/main_page_admin')
        elif role.role == 'professor':
            return redirect('/main_page_professor')
        elif role.role == 'student':
            return redirect('/main_page_student')

    return redirect('home')

@user_passes_test(is_admin)
def main_page_admin(request):
    if request.method == 'POST':
        subject_id = request.POST.get('subject_id')
        student_id = request.POST.get('student_id')
        edit_student_id = request.POST.get('edit_student_id')
        professor_id = request.POST.get('professor_id')
        edit_professor_id = request.POST.get('edit_professor_id')
        
        if subject_id:
            subject = get_object_or_404(Subject, id=subject_id)
            form = SubjectForm(request.POST, instance=subject)
            if form.is_valid():
                form.save()
                messages.success(request, 'Predmet ažuriran')
                return redirect('/main_page_admin')
        
        elif student_id:
            student = get_object_or_404(User, id=student_id)
            student.delete()
            messages.success(request, 'Student izbrisan')
            return redirect('/main_page_admin')
        
        elif edit_student_id:
            student = get_object_or_404(User, id=edit_student_id)
            form = StudentUpdateForm(request.POST, instance=student)
            if form.is_valid():
                user = form.save(commit=False)
                password = request.POST.get('password')
                if password:
                    user.set_password(password)
                user.save()
                messages.success(request, 'Student ažuriran')
                return redirect('/main_page_admin')
        
        elif professor_id:
            professor = get_object_or_404(User, id=professor_id)
            professor.delete()
            messages.success(request, 'Profesor izbrisan')
            return redirect('/main_page_admin')
        
        elif edit_professor_id:
            professor = get_object_or_404(User, id=edit_professor_id)
            form = ProfessorUpdateForm(request.POST, instance=professor)
            if form.is_valid():
                user = form.save(commit=False)
                password = request.POST.get('password')
                if password:
                    user.set_password(password)
                user.save()
                messages.success(request, 'Profesor ažuriran')
                return redirect('/main_page_admin')

        else:
            form = SubjectForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Predmet dodan')
                return redirect('/main_page_admin')
    else:
        form = SubjectForm()

    subjects = Subject.objects.all() 
    professors = User.objects.filter(role__role='professor')
    students = User.objects.filter(role__role='student')

    context = {
        'form': form,
        'subjects': subjects,
        'professors': professors,
        'students': students,
    }
    return render(request, "main_page_admin.html", context)

@user_passes_test(is_professor)
def main_page_professor(request):
    if request.method == 'POST':
        status_change = request.POST.get('status_change')
        student_id = request.POST.get('edit_status_id')
        subject_id = request.POST.get('subject_id')

        if status_change == '(Potpis izgubljen)':
            enrollment = Enrollment.objects.get(student_id=student_id, subject_id=subject_id)
            enrollment.status = 'potpis izgubljen'
            enrollment.save()
            messages.success(request, 'Status ažuriran')
            return redirect('/main_page_professor')

        elif status_change == '(Predmet položen)':
            enrollment = Enrollment.objects.get(student_id=student_id, subject_id=subject_id)
            enrollment.status = 'polozen'
            enrollment.save()
            messages.success(request, 'Status ažuriran')
            return redirect('/main_page_professor')

        elif status_change == '(Predmet upisan)':
            enrollment = Enrollment.objects.get(student_id=student_id, subject_id=subject_id)
            enrollment.status = 'upisan'
            enrollment.save()
            messages.success(request, 'Status ažuriran')
            return redirect('/main_page_professor')
    
    subjects = Subject.objects.filter(carrier=request.user)

    context = {
        'subjects': subjects,
    }
    return render(request, "main_page_professor.html", context)

@user_passes_test(is_student)
def main_page_student(request):
    form = EnrollmentForm()  # Initialize the form variable here

    if request.method == 'POST':
        subject_id = request.POST.get('subject_id')
        subject_delete = request.POST.get('subject_delete')
        
        if subject_id:
            subject = get_object_or_404(Subject, id=subject_id)
            form = EnrollmentForm(request.POST)
            if form.is_valid():
                Enrollment.objects.create(student=request.user, subject=subject, status='upisan')
                messages.success(request, 'Predmet upisan')
                return redirect('/main_page_student')
        
        if subject_delete:
            enrollment = Enrollment.objects.filter(student=request.user, subject_id=subject_delete, status='upisan').first()
            if enrollment:
                enrollment.delete()
                messages.success(request, 'Predmet ispisani')
            else:
                messages.error(request, 'Nemoguće ispisati predmet. Status nije "upisan"')
            return redirect('/main_page_student')

    subjects = Subject.objects.all()
    enrolled_subjects = Enrollment.objects.filter(student=request.user).values_list('subject', flat=True)
    available_subjects = subjects.exclude(id__in=enrolled_subjects)
    see_enrolled = Enrollment.objects.filter(student=request.user)
    total_points = 0
    upisan_enrollments = Enrollment.objects.filter(student=request.user, status='upisan')
    for enrollment in upisan_enrollments:
        total_points += enrollment.subject.points


    context = {
        'enrolled': see_enrolled,
        'subjects': available_subjects,
        'enrollment_form': form,
        'total_points': total_points if total_points else 0
    }
    return render(request, "main_page_student.html", context)

def upisni_list(request, student_id):
    student = get_object_or_404(User, id=student_id)
    enrollments = Enrollment.objects.filter(student=student)

    context = {
        'student': student,
        'enrollments': enrollments,
    }
    return render(request, 'upisni_list.html', context)

def logout_view(request):
    logout(request)
    return redirect('/home')