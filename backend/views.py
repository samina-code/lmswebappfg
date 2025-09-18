from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.admin.views.decorators import staff_member_required

from django.contrib.auth import get_user_model



# Models
from backend.models import CustomUser, Semester, Student, Teacher, Subject, AssignedSubject
from .forms import (
    StudentForm, TeacherForm, SemesterForm,
    AssignSubjectForm, AssignSemesterForm, ContactForm
)

User = get_user_model()

# ---------Public Views -----------

def home(request):
    return render(request, 'backend/Home.html')


from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import ContactForm

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()  # save in DB

            # send email
            subject = "New Contact Message"
            message = f"""
            You have received a new message:

            Name: {contact.name}
            Email: {contact.email}
            Message:
            {contact.message}
            """
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,   # sender email (must be configured)
                ["234noureena@gmail.com"],       # receiver email
                fail_silently=False,
            )

            messages.success(request, 'Thanks! Your message has been sent.')
            return redirect('contact')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = ContactForm()
    return render(request, 'backend/contact.html', {'form': form})

# ------------------- Authentication -------------------

def SignIn(request):
    if request.user.is_authenticated:
        return redirect('admindashboard')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password.")
            return redirect('SignIn')

        user = authenticate(request, username=user.username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admindashboard')
        else:
            messages.error(request, "Invalid credentials or not authorized.")
            return redirect('SignIn')

    return render(request, 'backend/SignIn.html')

def logout_view(request):
    request.session.flush()
    return redirect('SignIn')


from django.shortcuts import redirect, get_object_or_404
from .models import ContactMessage

# backend/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import ContactMessage

def inbox(request):
    messages = ContactMessage.objects.order_by("-created_at")
    return render(request, "admin/inbox.html", {"messages": messages})

def message_detail(request, pk):
    message = get_object_or_404(ContactMessage, pk=pk)
    if not message.is_read:
        message.is_read = True
        message.save()
    return render(request, "admin/message_detail.html", {"message": message})

def mark_message_read(request, pk):
    message = get_object_or_404(ContactMessage, pk=pk)
    message.is_read = True
    message.save()
    return redirect("inbox")


# ------------------- Dashboard -------------------

@staff_member_required
def admin_dashboard(request):
  total_students = Student.objects.count()   # direct Student model
  total_teachers = Teacher.objects.count() 
  total_semesters = Semester.objects.count()
  semester_data = Student.objects.values('semester__title').annotate(total=Count('id'))
  unread_messages = ContactMessage.objects.filter(is_read=False)

  labels = [item['semester__title'] if item['semester__title'] else "Unassigned" for item in semester_data]
  data = [item['total'] for item in semester_data]


  recent_activities = ActivityLog.objects.all().order_by('-timestamp')[:5]
  context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_semesters': total_semesters,
        'recent_activities': recent_activities,
         "unread_messages": unread_messages,
        "unread_count": unread_messages.count(),
    }
  return render(request, 'backend/admindashboard.html', context)

# ------------------- Chart Data -------------------
from .models import Feedback

@staff_member_required
def admin_dashboard(request):
    # existing counts
    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    total_semesters = Semester.objects.count()
    semester_data = Student.objects.values("semester__title").annotate(total=Count("id"))

    labels = [item["semester__title"] if item["semester__title"] else "Unassigned" for item in semester_data]
    data = [item["total"] for item in semester_data]

    recent_activities = ActivityLog.objects.all().order_by("-timestamp")[:5]

    # 🔹 Messages / Feedback
    unread_contact = ContactMessage.objects.filter(is_read=False).count()
    unread_feedback = LectureFeedback.objects.filter(is_read=False).count()
    unread_user_feedback = Feedback.objects.filter(is_read=False).count()

    total_unread = unread_contact + unread_feedback + unread_user_feedback

    context = {
        "total_students": total_students,
        "total_teachers": total_teachers,
        "total_semesters": total_semesters,
        "recent_activities": recent_activities,
        "unread_count": total_unread,
        "labels": labels,
        "data": data,
    }
    return render(request, "backend/admindashboard.html", context)
@staff_member_required
def open_messages(request):
    # mark all as read
    ContactMessage.objects.filter(is_read=False).update(is_read=True)
    LectureFeedback.objects.filter(is_read=False).update(is_read=True)
    Feedback.objects.filter(is_read=False).update(is_read=True)

    # redirect to Gmail
    return redirect("https://mail.google.com/")

from django.http import JsonResponse
from .models import Semester, Student, Teacher, AssignedSubject, ActivityLog
from django.http import JsonResponse
from .models import Student, Semester  # adjust if models are elsewhere

# Students by Semester
@staff_member_required
def students_chart(request):
    semesters = list(Semester.objects.values('id', 'name').order_by('id'))
    student_counts = (
        Student.objects
        .values('semester__id')
        .annotate(total=Count('id'))
    )
    counts_map = {row['semester__id']: row['total'] for row in student_counts}

    labels = [s['name'] for s in semesters]
    data = [counts_map.get(s['id'], 0) for s in semesters]

    return JsonResponse({"labels": labels, "data": data})

# Teachers by Semester (based on AssignedSubject)
def chart_data_teachers_by_semester(request):
    semesters = Semester.objects.all()
    labels = [s.title for s in semesters]
    data = [
        Teacher.objects.filter(assignedsubject__semester=s).distinct().count()
        for s in semesters
    ]
    return JsonResponse({'labels': labels, 'data': data})

#  Subjects per Semester (Activity Overview)
def chart_data_semester_activity(request):
    semesters = Semester.objects.all()
    labels = [s.title for s in semesters]
    data = [s.subjects.count() for s in semesters]   #  ManyToMany relation ka use
    return JsonResponse({'labels': labels, 'data': data})

#  Recent Admin Activity (Last 7 actions)
def chart_data_recent_activity(request):
    activities = ActivityLog.objects.order_by("-timestamp")[:7]
    labels = [a.timestamp.strftime("%d-%b %H:%M") for a in activities]  # X-axis me time
    data = list(range(1, len(activities) + 1))  # sirf dummy count (y-axis), ya ap log count bhi rakh sakte ho
    actions = [a.action for a in activities]  # Tooltip ke liye actions bhejna

    return JsonResponse({
        'labels': labels,
        'data': data,
        'actions': actions
    })

# ------------------- Student Management -------------------

@staff_member_required
def manage_students(request):
    students = Student.objects.all()
    return render(request, 'backend/managestudent.html', {'students': students})
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import StudentForm


from .models import ActivityLog

import random, string
from .models import CustomUser, Student, ActivityLog
from django.contrib import messages
from django.shortcuts import redirect, render


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from .forms import StudentForm
from .models import Student, CustomUser, ActivityLog
import random, string
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save(commit=False)

            #  Duplicate email check
            if CustomUser.objects.filter(email=student.email).exists():
                messages.error(request, "❌ This email is already registered!")
                return redirect('manage_students')

            # Random password generate
            raw_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

            #  CustomUser create
            user = CustomUser.objects.create_user(
                email=student.email,
                username=student.email,
                password=raw_password,
                role='student',
                first_name=student.name
            )

            student.user = user
            student.generated_password = raw_password
            student.save()

            #  Send email to student
            email_sent = False
            try:
                subject = "Welcome to SmartLearning 🎓"
                text_content = (
                    f"Hello {student.name},\n\n"
                    f"Your SmartLearning account has been created.\n\n"
                    f"Login Details:\n"
                    f"Email: {student.email}\n"
                    f"Password: {raw_password}\n\n"
                    f"Please login and change your password immediately.\n\n"
                    f"Regards,\nSmartLearning Team"
                )

                html_content = f"""
                <html>
                <body>
                    <h2>Welcome {student.name}! 🎉</h2>
                    <p>Your <b>SmartLearning</b> account has been created successfully.</p>
                    <p><b>Email:</b> {student.email}<br>
                       <b>Password:</b> {raw_password}</p>
                    <p style="color:red;">⚠️ Please login and change your password immediately.</p>
                    <br>
                    <p>Regards,<br><b>SmartLearning Team</b></p>
                </body>
                </html>
                """

                email = EmailMultiAlternatives(
                    subject,
                    text_content,
                    "234noureena@gmail.com",   # sender
                    [student.email],           # receiver
                )
                email.attach_alternative(html_content, "text/html")
                email.send()
                email_sent = True

            except Exception as e:
                email_error = str(e)

            #  Activity log
            ActivityLog.objects.create(
                admin_user=request.user,
                action=f"Added new student: {student.name} (Email: {student.email}  ; password:{raw_password})"
            )

            # Show success/error message
            if email_sent:
                messages.success(request, f"✅ Student added! Email sent to: {student.email} ; password:{raw_password}")
            else:
                messages.warning(request, f"⚠️ Student added but email failed: {email_error}")

            return redirect('manage_students')
        else:
            messages.error(request, "❌ Please correct the errors below.")
    else:
        form = StudentForm()

    students = Student.objects.all()
    return render(request, 'backend/managestudent.html', {'form': form, 'students': students})


from .models import ActivityLog

def delete_student(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    
    # Pehle student ka naam store kia qk phir (delete ke baad access nahi hoga)
    student_name = student.name  
    
    student.delete()

    #  Activity log add karein
    ActivityLog.objects.create(
        admin_user=request.user, 
        action=f"Deleted student: {student_name}"
    )

    messages.success(request, "Student successfully deleted!")  # success msg
    return redirect('view_students')





@staff_member_required
def view_students(request):
    students = Student.objects.all()
    return render(request, 'backend/adminviewstudent.html', {'students': students})

def assign_semester_to_student(request):
    success = False
    if request.method == 'POST':
        form = AssignSemesterForm(request.POST)
        if form.is_valid():
            form.save()
            success = True
            form = AssignSemesterForm()  # reset form
    else:
        form = AssignSemesterForm()

    return render(request, 'backend/adminstudentsemester.html', {
        'form': form,
        'success': success
    })

# ------------------- Teacher Management -------------------
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Teacher, ActivityLog, CustomUser
from .forms import TeacherForm
import random, string
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Teacher, ActivityLog, CustomUser
from .forms import TeacherForm
import random, string

from django.core.mail import send_mail
import random, string

from django.core.mail import EmailMultiAlternatives
import random, string

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from .forms import TeacherForm
from .models import Teacher, CustomUser, ActivityLog
import random, string
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def manage_teachers(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST, request.FILES)
        if form.is_valid():
            teacher = form.save(commit=False)

            # 🔹 Duplicate email check
            if CustomUser.objects.filter(email=teacher.email).exists():
                messages.error(request, "❌ This email is already registered!")
                return redirect("manageaddteacher")

            #  Random password generate
            raw_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

            #  CustomUser create
            user = CustomUser.objects.create_user(
                email=teacher.email,
                username=teacher.email,
                password=raw_password,
                role='teacher',
                first_name=teacher.name
            )

            teacher.user = user
            teacher.generated_password = raw_password
            teacher.save()

            #  Email send to teacher
            email_sent = False
            try:
                subject = "Welcome to SmartLearning 🎓"
                text_content = (
                    f"Hello {teacher.name},\n\n"
                    f"Your SmartLearning account has been created.\n\n"
                    f"Login Details:\n"
                    f"Email: {teacher.email}\n"
                    f"Password: {raw_password}\n\n"
                    f"Please login and change your password immediately.\n\n"
                    f"Regards,\nSmartLearning Team"
                )

                html_content = f"""
                <html>
                <body>
                    <h2>Welcome {teacher.name}! 🎉</h2>
                    <p>Your <b>SmartLearning</b> account has been created successfully.</p>
                    <p><b>Email:</b> {teacher.email}<br>
                       <b>Password:</b> {raw_password}</p>
                    <p style="color:red;">⚠️ Please login and change your password immediately.</p>
                    <br>
                    <p>Regards,<br><b>SmartLearning Team</b></p>
                </body>
                </html>
                """

                email = EmailMultiAlternatives(
                    subject,
                    text_content,
                    "234noureena@gmail.com",  # sender
                    [teacher.email],          # receiver
                )
                email.attach_alternative(html_content, "text/html")
                email.send()
                email_sent = True

            except Exception as e:
                email_error = str(e)

            #  Activity log
            ActivityLog.objects.create(
                admin_user=request.user,
                action=f"Added new teacher: {teacher.name} (Email: {teacher.email}   ; password:{raw_password})"
            )

            #  Show admin message
            if email_sent:
                messages.success(request, f"✅ Teacher added! Email sent to: {teacher.email} ;  password: {raw_password}")
            else:
                messages.warning(request, f"⚠️ Teacher added but email failed: {email_error}")

            return redirect("manageaddteacher")

        else:
            messages.error(request, "❌ Please correct the errors below.")
    else:
        form = TeacherForm()

    teachers = Teacher.objects.all()
    return render(request, 'backend/manageaddteacher.html', {
        'teachers': teachers,
        'form': form
    })



from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.contrib import messages
from backend.models import Teacher
from backend.forms import TeacherForm


from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import Teacher
from .forms import UpdateTeacherForm

from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import Teacher, ActivityLog
from .forms import UpdateTeacherForm

def update_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)

    if request.method == 'POST':
        form = UpdateTeacherForm(request.POST, request.FILES, instance=teacher)
        if form.is_valid():
            form.save()
            #  Activity log entry
            ActivityLog.objects.create(
                admin_user=request.user,
                action=f"Updated teacher: {teacher.name}"
            )

            messages.success(request, "Teacher successfully updated!")
            return redirect('view_teachers')
        else:
            # yeh sirf POST & invalid case me chalega
            for field, errors in form.errors.items():
                label = form[field].label
                for error in errors:
                    messages.error(request, f"{label}: {error}")
    else:
        form = UpdateTeacherForm(instance=teacher)

    return render(request, "backend/mangeupdatetea.html", {
        "form": form,
        "teacher": teacher
    })

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Teacher, ActivityLog

def delete_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    teacher_name = teacher.name   # naam save kar lia delete se pehle
    teacher.delete()

    #  Activity Log entry
    ActivityLog.objects.create(
        admin_user=request.user,
        action=f"Deleted teacher: {teacher_name}"
    )

    messages.success(request, 'Teacher deleted successfully.')
    return redirect('view_teachers')  # Must match URL name exactly

@staff_member_required
def view_teachers(request):
    teachers = Teacher.objects.all()
    return render(request, 'backend/mangeviewtea.html', {'teachers': teachers})




# ------------------- Subject Assignment -------------------
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Teacher, Semester, Subject, AssignedSubject, ActivityLog

def assign_subject(request, teacher_id):
    # Get the teacher
    teacher = get_object_or_404(Teacher, pk=teacher_id)

    # Get all semesters and subjects
    semesters = Semester.objects.all()
    subjects = Subject.objects.all()

    if request.method == 'POST':
        # Get the selected semester, subject, class_days and timing
        semester_id = request.POST.get('semester')
        subject_id = request.POST.get('subject')
        class_days = request.POST.get('class_days')  
        schedule=request.POST.get("schedule") 
        if semester_id and subject_id and class_days and schedule:
            semester = get_object_or_404(Semester, id=semester_id)
            subject = get_object_or_404(Subject, id=subject_id)

            # Check if this subject is already assigned to this teacher in this semester
            already_assigned = AssignedSubject.objects.filter(
                teacher=teacher,
                semester=semester,
                subject=subject
            ).exists()

            if not already_assigned:
                # Assign the subject with class_days and timing
                AssignedSubject.objects.create(
                    teacher=teacher,
                    semester=semester,
                    subject=subject,
                    class_days=class_days,
                    schedule=schedule
                )

                # Add activity log
                ActivityLog.objects.create(
                    admin_user=request.user,
                    action=f"Assigned subject '{subject.title}' to teacher '{teacher.name}' "
                           f"in semester '{semester.title}' on {class_days} at {schedule}"
                )
                messages.success(request, f"{subject.title} has been assigned to {teacher.name}.")
                return redirect('view_teachers')
            else:
                messages.error(request, "Subject already assigned to this teacher in this semester.")
        else:
            messages.error(request, "Please select semester, subject, class days, and schedule.")

    # Render the template
    return render(request, 'backend/manageassignsubject.html', {
        'teacher': teacher,
        'semesters': semesters,
        'subjects': subjects,
    })

# ------------------- Semester Management -------------------



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from .models import Semester, Subject
from .forms import SemesterForm, SubjectForm




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from .models import Semester, Subject
from .forms import SemesterForm, SubjectForm
from .models import Semester, Subject, ActivityLog
from .forms import SemesterForm, SubjectForm


def manage_semesters(request):
    semester_id = request.POST.get("semester_id") or request.GET.get("semester_id")
    semester = get_object_or_404(Semester, id=semester_id) if semester_id else None

    semester_form = SemesterForm(request.POST or None, instance=semester)
    subject_form = SubjectForm(request.POST or None, semester=semester)

    # Add Semester
    if 'add_semester' in request.POST:
        if semester_form.is_valid():
          saved_semester = semester_form.save()
              #  Log activity
          ActivityLog.objects.create(
                admin_user=request.user,
                action=f"Added Semester '{saved_semester.title}'"
            )
          messages.success(request, "Semester saved successfully!")
        return redirect('manage_semesters')

    # Add Subject
    elif 'add_subject' in request.POST:
        if subject_form.is_valid():
            subject = subject_form.save()
            if semester:
                semester.subjects.add(subject)
                  # Log activity
            ActivityLog.objects.create(
                admin_user=request.user,
                action=f"Added Subject '{subject.title}' to Semester '{semester.title if semester else 'N/A'}'"
            )
            messages.success(request, f"Subject '{subject.title}' added successfully!")
            return redirect('manage_semesters')

    # Delete Subject
    elif 'delete_subject' in request.POST:
        subject_id = request.POST.get("subject_id")
        subject = get_object_or_404(Subject, id=subject_id)
        subject.delete()
        messages.success(request, "Subject deleted successfully!")
        return redirect('manage_semesters')

    # Load all semesters with subjects
    semesters = Semester.objects.prefetch_related('subjects').all()

    return render(request, 'backend/mangesemester.html', {
        'form': semester_form,
        'subject_form': subject_form,
        'semesters': semesters
    })



    
    
 

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Student
from .forms import AssignSemesterForm

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Student, StudentSemester
from .forms import AssignSemesterForm

def assign_semester(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    if request.method == 'POST':
        form = AssignSemesterForm(request.POST)
        if form.is_valid():
            # Check if this student already has a semester assigned
            if StudentSemester.objects.filter(student=student).exists():
                messages.error(request, "This student already has a semester assigned!")
                return redirect('assign_semester', student_id=student.id)
            # Save the StudentSemester instance
            assign = form.save(commit=False)
            assign.student = student  # ensure correct student
            assign.save()
            messages.success(request, "Semester successfully assigned!")
            return redirect('view_students')
        else:
            messages.error(request, "Invalid data submitted, please try again.")
    else:
        # prefill the student field
        form = AssignSemesterForm(initial={'student': student})

    return render(request, 'backend/adminstudentsemester.html', {
        'form': form,
        'student': student
    })





from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Student
from .forms import StudentForm

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import UpdateStudentForm
from .models import Student

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import UpdateStudentForm
from .models import Student
def update_student(request, student_id):
    student = get_object_or_404(Student, pk=student_id)

    if request.method == 'POST':
        form = UpdateStudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            student = form.save(commit=False)

            #  Update linked CustomUser fields if needed
            if student.user:
                # Update email (or any other unique fields stored in CustomUser)
                student.user.email = form.cleaned_data.get('email', student.user.email)
                student.user.save()

            student.save()  # Save Student model after updating user
            messages.success(request, "Student successfully updated!")
            return redirect('view_students')
        else:
            # Loop through errors and show messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = UpdateStudentForm(instance=student)

    return render(request, 'backend/adminupdatestudent.html', {
        'form': form,
        'student': student
    })






from django.http import JsonResponse

def get_subjects_by_semester(request):
    semester_id = request.GET.get('semester_id')
    subjects = []

    if semester_id:
        try:
            semester = Semester.objects.get(id=semester_id)
            subjects = list(semester.subjects.values('id', 'title', 'code'))
        except Semester.DoesNotExist:
            subjects = []

    return JsonResponse({'subjects': subjects})





def teacher_subjects(request, teacher_id):
    teacher = Teacher.objects.get(id=teacher_id)
    assigned_subjects = AssignedSubject.objects.filter(teacher=teacher)
    return render(request, "backend/teacher_subjects.html", {
        "teacher": teacher,
        "assigned_subjects": assigned_subjects
    })

@login_required
def delete_assigned_subject(request, pk):
    assigned = get_object_or_404(AssignedSubject, id=pk)
    teacher_id = assigned.teacher.id
    assigned.delete()
    return redirect("teacher_subjects", teacher_id=teacher_id)












from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from .models import Student, Teacher, Semester, AssignedSubject, Subject

# -------- Students by Semester --------
@staff_member_required
def students_chart(request):
    # All semesters (include those with zero students)
    semesters = list(Semester.objects.values('id', 'name').order_by('id'))

    # Counts per semester (only where students exist)
    student_counts = (
        Student.objects
        .values('semester__id')
        .annotate(total=Count('id'))
    )
    counts_map = {row['semester__id']: row['total'] for row in student_counts}

    labels = [s['name'] for s in semesters]
    data = [counts_map.get(s['id'], 0) for s in semesters]

    return JsonResponse({"labels": labels, "data": data})


# -------- Teachers by Semester (via AssignedSubject) --------
@staff_member_required
def teachers_chart(request):
    # All semesters (include those with zero teachers)
    semesters = list(Semester.objects.values('id', 'name').order_by('id'))

    # Distinct teachers teaching in each semester (via AssignedSubject)
    teacher_counts = (
        AssignedSubject.objects
        .values('semester__id')
        .annotate(total=Count('teacher', distinct=True))
    )
    counts_map = {row['semester__id']: row['total'] for row in teacher_counts}

    labels = [s['name'] for s in semesters]
    data = [counts_map.get(s['id'], 0) for s in semesters]

    return JsonResponse({"labels": labels, "data": data})


# -------- Semester Activity (subjects per semester) --------
@staff_member_required
def semester_activity_chart(request):
    # All semesters (include those with zero subjects)
    semesters = list(Semester.objects.values('id', 'name').order_by('id'))

    # Distinct subjects assigned in each semester
    subject_counts = (
        AssignedSubject.objects
        .values('semester__id')
        .annotate(total=Count('subject', distinct=True))
    )
    counts_map = {row['semester__id']: row['total'] for row in subject_counts}

    labels = [s['name'] for s in semesters]
    data = [counts_map.get(s['id'], 0) for s in semesters]

    return JsonResponse({"labels": labels, "data": data})








from django.http import JsonResponse
from .models import Student, Semester

def chart_data_students_by_semester(request):
    semesters = Semester.objects.all()
    labels = []
    data = []

    for sem in semesters:
        labels.append(sem.title)
        count = Student.objects.filter(semester=sem).count()  # har semester me student count
        data.append(count)

    return JsonResponse({
        'labels': labels,
        'data': data,
    })









#teacher 
from django.shortcuts import render, redirect
from django.contrib import messages

# Home Page


# Sign In Page (Teacher / Student)

from django.contrib.auth import authenticate, login

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import LoginForm

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect

# backend/views.py
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.conf import settings

def SignIn(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            if user.role == "admin":
                return redirect("admindashboard")
            elif user.role == "teacher":
                return redirect("teacher_dashboard")
            elif user.role == "student":
                return redirect("student_dashboard")
        else:
            messages.error(request, "Invalid credentials or not authorized.")

    return render(request, "backend/SignIn.html")

# Teacher Dashboard
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UpdateTeacherForm

from django.shortcuts import render
from backend.models import Performance, Subject, TeacherFeedback
import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Student, AssignedSubject, Assignment, Activity

    
  


from django.db.models import F, Avg
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from django.shortcuts import render, get_object_or_404
from django.db.models import F, Avg
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import (
    Teacher, AssignedSubject, StudentSemester, Performance,
    StudentAssignment, Activity, LectureFeedback
)



#
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import F, Avg
from .models import Teacher, Student, Assignment, Subject, Performance, Activity, LectureFeedback, AssignedSubject, StudentSemester
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import F, Avg
from django.contrib import messages

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import F, Avg
from django.db.models import Q
from backend.models import (
    Teacher, AssignedSubject, StudentSemester, Performance,
    Assignment, Activity, LectureFeedback, Student
)



from django.http import JsonResponse


def mark_feedback_as_read(request, fb_id):
    if request.method == "POST":
        teacher = get_object_or_404(Teacher, user=request.user)

        try:
            fb = LectureFeedback.objects.get(id=fb_id, lecture__subject__assignedsubject__teacher=teacher)
            fb.is_read = True
            fb.save()

            unread_count = LectureFeedback.objects.filter(
                lecture__subject__assignedsubject__teacher=teacher,
                is_read=False
            ).count()

            return JsonResponse({"status": "success", "unread_count": unread_count})
        except LectureFeedback.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Feedback not found"})
    return JsonResponse({"status": "error", "message": "Invalid request"})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, F, Q
from .models import (
    Teacher, AssignedSubject, StudentSemester, Student, 
    Assignment, Performance, Activity, LectureFeedback, Semester
)


@login_required
def teacher_dashboard(request):
    #  Get teacher linked to current user
    try:
        teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        messages.error(request, "Teacher profile not found.")
        return redirect("Home")

    #  Assigned subjects
    assigned_subjects = AssignedSubject.objects.filter(teacher=teacher)
    teacher_subject_ids = assigned_subjects.values_list("subject_id", flat=True)

    #  Semesters this teacher teaches
    teacher_semesters = assigned_subjects.values_list("semester_id", flat=True).distinct()
    selected_semester = teacher_semesters.first() if teacher_semesters.exists() else None

    #  Total students
    total_students = StudentSemester.objects.filter(
        semester_id__in=teacher_semesters
    ).count()

    #  Total subjects
    total_subjects = assigned_subjects.count()

    #  Average score for selected semester
    student_ids = (
        StudentSemester.objects.filter(semester_id=selected_semester)
        .values_list("student_id", flat=True)
        if selected_semester else []
    )

    avg_scores = Performance.objects.filter(
        student_id__in=student_ids, semester_id=selected_semester
    ).annotate(
        total_score=F("assignment") + F("quiz") + F("midterm") + F("final")
    ).aggregate(avg=Avg("total_score"))

    average_score = avg_scores["avg"] or 0

    # Pending assignments
    pending_assignments = Assignment.objects.filter(
        student__id__in=student_ids,
        subject_id__in=teacher_subject_ids,
        graded=False
    ).count()

    #  All student assignments for this teacher
    student_assignments = Assignment.objects.filter(
        Q(subject__id__in=teacher_subject_ids) | Q(subject__isnull=True)
    ).select_related("student", "subject").order_by("-uploaded_at")

    # Handle grading (POST request)
    if request.method == "POST" and "submission_id" in request.POST:
        submission_id = request.POST.get("submission_id")
        grade = request.POST.get("grade")
        feedback = request.POST.get("feedback", "")

        submission = get_object_or_404(Assignment, id=submission_id)
        submission.graded = True
        submission.grade = grade
        submission.feedback = feedback
        submission.save()

        # Update Performance (no duplicates)
        if grade and grade.isdigit():
            new_marks = int(grade)

            # Student ka latest semester nikaalo
            student_semester_obj = StudentSemester.objects.filter(
                student=submission.student
            ).order_by("-id").first()

            if student_semester_obj:
                semester_id = student_semester_obj.semester.id

                # Pehle check karo existing record
                perf = Performance.objects.filter(
                    student=submission.student,
                    subject=submission.subject,
                    semester_id=semester_id
                ).first()

                if perf:
                    #  sirf assignment update karo
                    perf.assignment = new_marks
                    perf.save()
                else:
                    #  agar nahi hai to naya banao
                    Performance.objects.create(
                        student=submission.student,
                        subject=submission.subject,
                        semester_id=semester_id,
                        assignment=new_marks
                    )

        messages.success(request, f"✅ Marks saved for {submission.student}")
        return redirect("teacher_dashboard")

    #  Recent activities
    recent_activities = Activity.objects.filter(
        teacher=request.user
    ).order_by("-timestamp")[:5]

    # Feedback notifications
    all_feedback = LectureFeedback.objects.filter(
        lecture__subject_id__in=teacher_subject_ids
    ).select_related("student", "lecture").order_by("-id")

    unread_count = all_feedback.filter(is_read=False).count()
    feedback_messages = all_feedback[:10]

    #  Context for template
    context = {
        "total_students": total_students,
        "total_subjects": total_subjects,
        "average_score": round(average_score, 2),
        "pending_assignments": pending_assignments,
        "recent_activities": recent_activities,
        "assigned_subjects": assigned_subjects,
        "selected_semester": selected_semester,
        "student_assignments": student_assignments,
        "feedback_messages": feedback_messages,
        "unread_feedback_count": unread_count,
    }

    return render(request, "backend/teacher/teacherdashboard.html", context)


def mark_all_feedback_as_read(request):
    teacher = get_object_or_404(Teacher, user=request.user)

    LectureFeedback.objects.filter(
        lecture__subject__assignedsubject__teacher=teacher,
        is_read=False
    ).update(is_read=True)

    return JsonResponse({"status": "success", "unread_count": 0})

@login_required
def mark_all_feedback_as_read(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    subject_ids = AssignedSubject.objects.filter(teacher=teacher).values_list("subject_id", flat=True)

    LectureFeedback.objects.filter(
        lecture__subject_id__in=subject_ids,
        is_read=False
    ).update(is_read=True)

    return JsonResponse({"status": "success", "unread_count": 0})
@login_required
def mark_all_feedback_as_read(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    subject_ids = AssignedSubject.objects.filter(teacher=teacher).values_list("subject_id", flat=True)

    LectureFeedback.objects.filter(
        lecture__subject_id__in=subject_ids,
        is_read=False
    ).update(is_read=True)

    return JsonResponse({"status": "success", "unread_count": 0})

#  My Subjects
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Subject, Semester, Teacher, AssignedSubject

# backend/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import AssignedSubject, Semester

@login_required
def teacher_my_subjects(request):
    # Get Teacher object for logged-in user
    teacher_obj = Teacher.objects.filter(user=request.user).first()
    if not teacher_obj:
        semester_subjects = []
    else:
        assigned_subjects = AssignedSubject.objects.filter(teacher=teacher_obj).select_related('subject', 'semester', 'teacher')
        
        semesters = Semester.objects.all()
        semester_subjects = []
        for sem in semesters:
            subjects_in_sem = assigned_subjects.filter(semester=sem)
            if subjects_in_sem.exists():
                semester_subjects.append({
                    "semester": sem,
                    "subjects": subjects_in_sem
                })
    
    context = {
        "semester_subjects": semester_subjects,
        "semesters": Semester.objects.all(),
    }
    return render(request, "backend/teacher/teacher-my-subjects.html", context)

# views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from backend.models import Teacher, StudentSemester, Semester


from .models import Semester, Subject
from .models import Semester, Subject, AssignedSubject
from .models import Semester, Subject, Material, Teacher


from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Semester, StudentSemester, Student, Teacher

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from backend.models import Teacher, StudentSemester, Semester
from backend.models import StudentSemester
from django.db.models import Q
from django.db import models


def tmy_students(request):
    teacher = request.user.teacher  
    semesters = Semester.objects.all()
    selected_semester = request.GET.get('semester', 'all')
    query = request.GET.get('q', '').strip()

    # Teacher ke semesters
    teacher_semesters = teacher.assignedsubject_set.values_list("semester_id", flat=True).distinct()

    students_qs = StudentSemester.objects.filter(
        semester_id__in=teacher_semesters
    ).select_related("student__user", "semester", "teacher")

    if selected_semester != "all":
        students_qs = students_qs.filter(semester_id=selected_semester)

    if query:
        students_qs = students_qs.filter(
            models.Q(student__user__first_name__icontains=query) |
            models.Q(student__user__last_name__icontains=query) |
            models.Q(student__name__icontains=query) |
            models.Q(student__roll_no__icontains=query) |
            models.Q(student__email__icontains=query)
        )

    context = {
        "students_qs": students_qs,
        "semesters": semesters,
        "selected_semester": selected_semester,
        "query": query,
    }
    return render(request, "backend/teacher/tmy-students.html", context)


from .models import Activity
from .models import Activity, Assignment
def upload_material(request):
    semesters = Semester.objects.all()
    materials = Material.objects.all()

    if request.method == "POST":
        file = request.FILES.get("pdf_file")
        semester_id = request.POST.get("semester")
        subject_id = request.POST.get("subject")
        lecture_title = request.POST.get("lecture_title")

        if file and semester_id and subject_id and lecture_title:
            try:
                semester = Semester.objects.get(id=semester_id)
                subject = Subject.objects.get(id=subject_id)
                teacher = Teacher.objects.filter(user=request.user).first()

                # Save material
                new_material = Material.objects.create(
                    teacher=teacher,
                    semester=semester,
                    subject=subject,
                    lecture_title=lecture_title,
                    pdf_file=file
                )

                # Log activity
                Activity.objects.create(
                    teacher=request.user,
                   action=f"Uploaded material '{new_material}'"
                )

                messages.success(request, f"✅ {file.name} uploaded successfully.")
                return redirect("upload_material")  
            except Exception as e:
                messages.error(request, f"❌ Upload failed: {e}")
        else:
            messages.error(request, "❌ Please fill all fields and upload a file.")

    # Render page
    return render(request, 'backend/teacher/upload-material.html', {
        "semesters": semesters,
        "materials": materials
    })

from django.http import JsonResponse
from .models import Semester

def get_subjects(request, semester_id):
    try:
        semester = Semester.objects.get(id=semester_id)
        subjects = semester.subjects.all().values("id", "name", "code")
        return JsonResponse(list(subjects), safe=False)
    except Semester.DoesNotExist:
        return JsonResponse([], safe=False)
from django.shortcuts import get_object_or_404

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Material, Activity
from django.contrib.auth.decorators import login_required

@login_required
def delete_material(request, material_id):
    material = get_object_or_404(Material, id=material_id)
    material_title = material.lecture_title
    subject_name = material.subject.name if material.subject else "Unknown Subject"
    material.delete()

    # Log activity
    Activity.objects.create(
        teacher=request.user,
        action=f"Deleted material '{material_title}' "
    )

    messages.success(request, "Material deleted successfully ")
    return redirect("upload_material")

# 🔹 Quiz Creator

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Quiz, Question, Semester, Subject
from .forms import QuizForm

from .forms import QuizForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Quiz, Question, Semester, Subject  
from .forms import QuizForm


@login_required
def quiz_creator(request):
    teacher = Teacher.objects.filter(user=request.user).first()
    assigned_subjects = Subject.objects.filter(assignedsubject__teacher=teacher).distinct()
    semesters = Semester.objects.all()

    if request.method == "POST":
        form = QuizForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            if subject not in assigned_subjects:
                messages.error(request, " You are not assigned to this subject!")
                return redirect("quiz_creator")

            quiz = form.save(commit=False)
            quiz.created_by = request.user
            quiz.save()

            questions = request.POST.getlist("questions[]")
            optionsA = request.POST.getlist("optionA[]")
            optionsB = request.POST.getlist("optionB[]")
            optionsC = request.POST.getlist("optionC[]")
            optionsD = request.POST.getlist("optionD[]")
            corrects = request.POST.getlist("correct[]")

            for q, a, b, c, d, corr in zip(questions, optionsA, optionsB, optionsC, optionsD, corrects):
                if q.strip():
                    Question.objects.create(
                        quiz=quiz,
                        text=q,
                        option_a=a,
                        option_b=b,
                        option_c=c,
                        option_d=d,
                        correct_answer=corr
                    )

            Activity.objects.create(
                teacher=request.user,
                action=f"Created quiz '{quiz.title}'"
            )

            messages.success(request, "Quiz created successfully!")
            return redirect("quiz_creator")
    else:
        form = QuizForm()

    return render(request, "backend/teacher/quiz_creator.html", {
        "form": form,
        "semesters": semesters,
        "subjects": assigned_subjects,
    })


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Student, Semester, Subject, Performance
from .forms import PerformanceForm
from django.contrib.auth.decorators import login_required

@login_required
def update_performance(request):
    teacher = Teacher.objects.filter(user=request.user).first()
    assigned_subjects = Subject.objects.filter(assignedsubject__teacher=teacher).distinct()

    students = Student.objects.all()
    semesters = Semester.objects.all()
    performances = Performance.objects.all()

    if request.method == "POST":
        student_id = request.POST.get('student')
        semester_id = request.POST.get('semester')
        subject_id = request.POST.get('subject')
        assignment_marks = request.POST.get('assignment')
        quiz_marks = request.POST.get('quiz')
        midterm_marks = request.POST.get('midterm')
        final_marks = request.POST.get('final')

        if not all([student_id, semester_id, subject_id]):
            messages.error(request, "Please select Student, Semester, and Subject.")
            return redirect('update_performance')

        subject = get_object_or_404(Subject, id=subject_id)
        if subject not in assigned_subjects:
            messages.error(request, "❌ You are not assigned to this subject!")
            return redirect("update_performance")

        student = get_object_or_404(Student, id=student_id)
        semester = get_object_or_404(Semester, id=semester_id)

        performance, created = Performance.objects.update_or_create(
            student=student,
            subject=subject,
            semester=semester,
            defaults={
                "assignment": assignment_marks,
                "quiz": quiz_marks,
                "midterm": midterm_marks,
                "final": final_marks,
            }
        )

        Activity.objects.create(
            teacher=request.user,
            action=f"Updated performance for {student.user.username if student.user else student.name}"
        )

        msg = "Performance added successfully." if created else "Performance updated successfully."
        messages.success(request, msg)

        return redirect('update_performance')

    return render(request, 'backend/teacher/updateperformance.html', {
        "students": students,
        "semesters": semesters,
        "subjects": assigned_subjects,
        "performances": performances,
    })



def get_subjects(request, semester_id):
    try:
        semester = Semester.objects.get(id=semester_id)
        subjects = list(semester.subjects.values("id", "title", "code"))
        return JsonResponse(subjects, safe=False)
    except Semester.DoesNotExist:
        return JsonResponse([], safe=False)
#  Teacher Announcement
from django.http import JsonResponse

def get_students_by_semester(request, semester_id):
    students = []
    student_semesters = StudentSemester.objects.filter(semester_id=semester_id).select_related('student__user')
    for ss in student_semesters:
        student_name = (
            f"{ss.student.user.first_name} " 
            if ss.student.user else ss.student.name
        )
        students.append({"id": ss.student.id, "name": student_name})
    return JsonResponse(students, safe=False)


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Semester, Subject, Teacher, Announcement



from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string


@login_required
def teacher_announcement(request):
    teacher = Teacher.objects.filter(user=request.user).first()
    semesters = Semester.objects.all()
    assigned_subjects = Subject.objects.filter(assignedsubject__teacher=teacher).distinct()
    announcements = Announcement.objects.filter(teacher=teacher).order_by('-date_posted')

    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        semester_id = request.POST.get("semester")
        subject_id = request.POST.get("subject")
        ann_type = request.POST.get("type")
        title = request.POST.get("title")
        description = request.POST.get("description")
        date_input = request.POST.get("date") or None

        if not all([semester_id, subject_id, ann_type, title, description]):
            return JsonResponse({"status": "error", "message": "❌ Please fill all required fields!"})

        subject = get_object_or_404(Subject, id=subject_id)
        if subject not in assigned_subjects:
            return JsonResponse({"status": "error", "message": " You are not assigned to this subject!"})

        semester = get_object_or_404(Semester, id=semester_id)

        Announcement.objects.create(
            teacher=teacher,
            semester=semester,
            subject=subject,
            type=ann_type,
            title=title,
            description=description,
            date_posted=date_input if date_input else None
        )

        Activity.objects.create(
            teacher=request.user,
            action=f"Posted announcement '{title}' for {subject.title}"
        )

        html = render_to_string("backend/teacher/announcement_list_partial.html", {
            "announcements": Announcement.objects.filter(teacher=teacher).order_by('-date_posted')
        })

        return JsonResponse({"status": "success", "html": html, "message": "✅ Announcement posted successfully!"})

    return render(request, "backend/teacher/teacher_announcement.html", {
        "semesters": semesters,
        "subjects": assigned_subjects,
        "announcements": announcements
    })

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Announcement

@login_required
def delete_announcement(request, ann_id):
    if request.method == "POST":
        try:
            ann = Announcement.objects.get(id=ann_id)
            ann.delete()
            return JsonResponse({"status": "success"})
        except Announcement.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Announcement not found"})
    return JsonResponse({"status": "error", "message": "Invalid request"})



@login_required
def upload_assignment(request):
    if request.method == "POST":
        assignment = request.FILES.get("assignment")
        if assignment:
            messages.success(request, f"{assignment.name} uploaded successfully!")
        else:
            messages.error(request, "Please upload a valid assignment.")
    return render(request, 'backend/upload_assignment.html')






from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def teacher_profile(request):
    return render(request, "backend/teacher/teacherprofile.html")   # bana lena template

@login_required
def teacher_settings(request):
    return render(request, "backend/teacher/teachersetting.html")  # bana lena template



#student dashboard 


# backend/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.models import User
from collections import defaultdict
from .models import Quiz, Answer, QuizResult, Student
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import ProfilePictureForm, CustomPasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import get_object_or_404, render

import random
from django.http import JsonResponse
from django.db.models.functions.datetime import TruncMonth
from django.db.models import Count
from django.utils.timezone import now

from collections import defaultdict
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.utils.timezone import now
# Models
from .models import (
    ContactMessage, Student, Semester, Subject, Quiz, QuizResult,
    Assignment, StudentAssignment, TeacherFeedback, Announcement,
  
)

# Forms
from .forms import (
   LoginForm, FeedbackForm, AssignmentForm, ContactForm
)

# ---------- Authentication ----------

       
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Student, Semester

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .models import  CustomUser
from .models import Student
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import  Semester


from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Student, Semester

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .models import  CustomUser
from .models import Student
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import  Semester


from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.contrib import messages


from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.db.models import Count
from django.db.models.functions import TruncMonth

from collections import defaultdict

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.timezone import now
from django.db.models import Avg, Count
from django.db.models.functions import TruncMonth

from backend.models import (
    Student, Quiz, QuizResult,
    Assignment, Announcement,
    Task, Achievement, Note, Event, Todo
)

from django.db.models import Avg
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import (
    Student, Assignment, StudentAssignment,
    Quiz, QuizResult, Note, Announcement,
    Performance
)

from django.db.models import Avg
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Student, StudentSemester, Assignment, QuizResult, Note, Announcement, Quiz, Performance

from django.db.models import Avg
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from .models import Student, StudentSemester, Assignment, QuizResult, Note, Announcement, Quiz, Performance

from django.db.models import Avg
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from .models import Student, StudentSemester, Assignment, QuizResult, Note, Announcement, Quiz, Performance


from django.db.models import Avg
from django.utils.timezone import now
from django.shortcuts import render
from .models import Student, StudentSemester, Assignment, Note, Announcement, Quiz, QuizResult, Performance

from django.utils.timezone import now
from datetime import timedelta
from django.utils.timezone import now
from .models import Notification


@login_required
def student_dashboard(request):
    user = request.user

    # Student profile
    student = Student.objects.filter(user=user).first()

    # Latest semester from StudentSemester
    assigned_semester = None
    if student:
        student_semester_obj = (
            StudentSemester.objects.filter(student=student)
            .order_by("-id")
            .first()
        )
        if student_semester_obj:
            assigned_semester = student_semester_obj.semester

    # Last 3 days ka time window
    three_days_ago = now() - timedelta(days=3)

    # Tasks → Assignments uploaded by this student (last 3 days)
    tasks = Assignment.objects.filter(uploaded_by=user, uploaded_at__gte=three_days_ago).order_by("-uploaded_at")

    # Notes → Personal notes (latest only)
    note = Note.objects.filter(student=user).last()

    # Todos → Only announcements of this student's semester (last 3 days)
    todos = (
        Announcement.objects.filter(semester=assigned_semester, date_posted__gte=three_days_ago)
        .order_by("-date_posted")
        if assigned_semester else Announcement.objects.none()
    )

    # Latest upcoming quiz for this student’s semester
    next_quiz = None
    if assigned_semester:
        next_quiz = (
            Quiz.objects.filter(
                subject__semester=assigned_semester,
                due_date__gte=now().date()
            )
            .order_by("due_date")
            .first()
        )

    # Progress → Average quiz score
    results = QuizResult.objects.filter(student=user, score__isnull=False)
    progress = int(results.aggregate(avg=Avg("score"))["avg"] or 0)

    # Events → Performance timeline (last 3 days only)
    events = (
        Performance.objects.filter(student=student, created_at__gte=three_days_ago).order_by("created_at")
        if student else []
    )

    # Chart Data → Subject wise average
    subject_scores = (
        QuizResult.objects.filter(student=user, score__isnull=False)
        .values("quiz__subject__name")
        .annotate(avg_score=Avg("score"))
    )
    subject_names = [s["quiz__subject__name"] for s in subject_scores]
    subject_marks = [s["avg_score"] for s in subject_scores]

    # Dynamic Task Checklist
    task_checklist = []
    if tasks.exists():
        task_checklist.append("Submit Assignment")
    if note:
        task_checklist.append("Review Notes")
    if next_quiz:
        task_checklist.append("Practice Quiz")

    # Dynamic Achievements (last 3 days)
    achievements = []
    quiz_results = QuizResult.objects.filter(student=user, score__isnull=False, quiz__due_date__gte=three_days_ago.date())
    for qr in quiz_results:
        achievements.append(f"{qr.quiz.title} ({qr.score}%)")

    assignments_completed = tasks.count()
    if assignments_completed > 0:
        achievements.append(f"Completed {assignments_completed} Assignments")

    
       # Notifications (safe way)
    notifications_qs = Notification.objects.filter(user=user).order_by("-created_at")
    unread_count = notifications_qs.filter(is_read=False).count()
    notifications = notifications_qs[:10]   # sirf latest 10 show karna hai


    # Announcements (last 3 days)
    if assigned_semester:
        announcements = Announcement.objects.filter(semester=assigned_semester, date_posted__gte=three_days_ago).order_by('-date_posted')[:5]
        for ann in announcements:
            notifications = list(notifications) + [f"📢 Announcement: {ann.title}"]
           
    # Upcoming Quizzes (still future-based, not restricted to 3 days)
    if assigned_semester:
        upcoming_quizzes = Quiz.objects.filter(subject__semester=assigned_semester, due_date__gte=now().date()).order_by('due_date')[:5]
        for quiz in upcoming_quizzes:
            notifications.append(f"📝 Quiz: {quiz.title} due {quiz.due_date}")

    # Assignments (last 3 days)
    if assigned_semester:
        assignments = Assignment.objects.filter(subject__semester=assigned_semester, uploaded_at__gte=three_days_ago).order_by('-uploaded_at')[:5]
        for assign in assignments:
            notifications.append(f"📂 Assignment: {assign.title} uploaded {assign.uploaded_at.date()}")
   
    context = {
        "tasks": tasks,
        "achievements": achievements,
        "note": note,
        "todos": todos,
        "next_quiz": next_quiz,
        "progress": progress,
        "events": events,
        "chart_data": {
            "labels": subject_names,
            "scores": subject_marks,
        },
        "subject_names": subject_names,
        "subject_marks": subject_marks,
        "today": now().date(),
        "task_checklist": task_checklist,
         "notifications": notifications,
        "unread_count": unread_count,
    }

    return render(request, "backend/student/id.html", context)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


@login_required
@csrf_exempt
def mark_notifications_read(request):
    if request.method == "POST":
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error"}, status=400)



@login_required
def delete_note(request, note_id):
    try:
        note = Note.objects.get(id=note_id, student=request.user)
        note.delete()
    except Note.DoesNotExist:
        pass
    return redirect('student_dashboard')


from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import Note

@login_required
def save_note(request):
    if request.method == "POST":
        content = request.POST.get("note_content", "").strip()
        if content:
            note, created = Note.objects.update_or_create(
                student=request.user,  # Pass CustomUser instance
                defaults={"text": content}
            )
    return redirect('student_dashboard')

#  API for Stats (optional: agar AJAX use karna ho)
@login_required
def id_stats_api(request):
    total_students = Student.objects.count()
    total_assignments = Assignment.objects.count()

    #  upcoming announcements
    upcoming_announcements = Announcement.objects.filter(
        date_posted__gte=now()
    ).values("title", "date_posted")

    #  submissions trend (group by month)
    submissions = Assignment.objects.annotate(
        month=TruncMonth("uploaded_at")
    ).values("month").annotate(count=Count("id")).order_by("month")

    labels = [s["month"].strftime("%b %Y") for s in submissions if s["month"]]
    data = [s["count"] for s in submissions]

    payload = {
        "totals": {
            "students": total_students,
            "assignments": total_assignments,
        },
        "announcements": list(upcoming_announcements),
        "chart": {
            "labels": labels,
            "data": data,
        },
    }
    return JsonResponse(payload)


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from collections import defaultdict
from .models import Quiz, Answer, QuizResult, Student


from collections import defaultdict
from collections import defaultdict
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from backend.models import Student, Quiz, QuizResult

from collections import defaultdict
from django.shortcuts import render
from backend.models import Quiz, QuizResult


from collections import defaultdict
from django.shortcuts import render
from backend.models import Quiz, QuizResult
from django.contrib.auth.decorators import login_required



from collections import defaultdict
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from backend.models import Quiz, QuizResult, StudentSemester

from collections import defaultdict
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Quiz, StudentSemester, QuizResult


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from collections import defaultdict
from .models import Quiz, QuizResult, Performance, Student, StudentSemester

@login_required
def my_quiz(request):
    user = request.user
    student_profile = getattr(user, 'student_profile', None)

    # Get latest semester
    student_semester = (
        StudentSemester.objects.filter(student=student_profile)
        .order_by("-id")
        .first()
    )
    assigned_semester = student_semester.semester if student_semester else None

    quizzes_by_subject = defaultdict(list)

    if assigned_semester:
        quizzes = Quiz.objects.filter(semester=assigned_semester).select_related("subject")

        for quiz in quizzes:
            if quiz.subject:
                subj_key = f"{quiz.subject.code or 'NoCode'} - {getattr(quiz.subject, 'name', None) or getattr(quiz.subject, 'title', None) or 'Unnamed Subject'}"
            else:
                subj_key = f"Subject {quiz.id}"

            result, _ = QuizResult.objects.get_or_create(
                student=request.user,   #  CustomUser instance
             quiz=quiz,
                  defaults={"status": "Not Attempted"},
)


            quizzes_by_subject[subj_key].append({
                "id": quiz.id,
                "title": quiz.title or "(No Title)",
                "due_date": quiz.due_date.strftime("%d-%m-%Y") if quiz.due_date else "-",
                "status": result.status,
                "score": result.score if result.score is not None else "-",
            })

    context = {
        "assigned_semester": assigned_semester.title if assigned_semester else None,
        "quizzes_by_subject": dict(quizzes_by_subject),
    }

    return render(request, "backend/student/my_quiz.html", context)

@login_required
def submit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    student = get_object_or_404(Student, user=request.user)

    # Example: hardcoded score (later calculate dynamically)
    score = 8  

    # Update or create QuizResult
    result, created = QuizResult.objects.update_or_create(
        student=student,
        quiz=quiz,
        defaults={
            "status": "Attempted",
            "score": score,
        }
    )

    # Update Performance automatically
    perf, created = Performance.objects.get_or_create(
        student=student,
        subject=quiz.subject,
        semester=quiz.semester,   # include semester
    )
    perf.quiz = (perf.quiz or 0) + score
    perf.save()

    messages.success(request, f"Quiz submitted! You scored {score} marks.")
    return redirect("my_quiz")

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Quiz, Question, QuizResult

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone



         
@login_required
def start_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()
    now = timezone.now()

    quiz_result, created = QuizResult.objects.get_or_create(
        student=request.user,
        quiz=quiz,
        defaults={
            "status": "In Progress",
            "score": 0,
            "started_at": now,
            "completed_at": None,
            "answers_data": {},
        }
    )

    if not quiz_result.answers_data:
        quiz_result.answers_data = {}
        quiz_result.save()

    # Agar already complete ho chuka hai
    if quiz_result.status == "Completed":
        results = []
        for q in questions:
            selected = quiz_result.answers_data.get(str(q.id), "Not Answered")
            results.append({
                "question": q.text,
                "selected": selected,
                "correct": q.correct_answer,
                "is_correct": (selected == q.correct_answer)
            })
        return render(request, "backend/student/startquiz.html", {
            "quiz": quiz,
            "questions": questions,
            "results": results,
            "score": quiz_result.score,
            "total": questions.count(),
            "message": "You have already submitted this quiz."
        })

    # Time calculate
    if quiz_result.started_at:
        elapsed = (now - quiz_result.started_at).total_seconds()
    else:
        quiz_result.started_at = now
        quiz_result.save()
        elapsed = 0

    remaining_seconds = max(0, (quiz.duration_minutes or 7) * 60 - elapsed)

    if remaining_seconds <= 0:
        quiz_result.status = "Completed"
        quiz_result.completed_at = now
        quiz_result.save()
        return render(request, "backend/student/startquiz.html", {
            "quiz": quiz,
            "questions": questions,
            "results": [],
            "score": quiz_result.score,
            "total": questions.count(),
            "message": " Time is up! Quiz auto-submitted."
        })

    #  Agar POST request hai (submit quiz)
    if request.method == "POST":
        score = 0
        results = []
        answers_data = {}

        for q in questions:
            selected = request.POST.get(str(q.id))
            answers_data[str(q.id)] = selected or "Not Answered"
            is_correct = (selected == q.correct_answer)
            if is_correct:
                score += 1
            results.append({
                "question": q.text,
                "selected": selected or "Not Answered",
                "correct": q.correct_answer,
                "is_correct": is_correct
            })

        quiz_result.status = "Completed"
        quiz_result.score = score
        quiz_result.completed_at = now
        quiz_result.answers_data = answers_data
        quiz_result.save()

        #  Performance Table Update (Overwrite Marks Only)
        student = get_object_or_404(Student, user=request.user)
        perf, created = Performance.objects.get_or_create(
            student=student,
            subject=quiz.subject,
            semester=quiz.semester,
        )
        perf.quiz = score   # <-- overwrite karega, add nahi karega
        perf.save()

        return render(request, "backend/student/startquiz.html", {
            "quiz": quiz,
            "questions": questions,
            "results": results,
            "score": score,
            "total": questions.count(),
            "message": "✅ Quiz submitted and performance updated (latest marks saved)!"
        })

    # Agar GET request hai
    return render(request, "backend/student/startquiz.html", {
        "quiz": quiz,
        "questions": questions,
        "score": None,
        "remaining_seconds": remaining_seconds,
        "quiz_duration": quiz.duration_minutes or 7
    })

@login_required
def quiz_list_view(request):
    """All quiz results ek saath list + PDF export ke liye"""
    quiz_results = QuizResult.objects.filter(student=request.user).select_related("quiz__subject")

    quizzes_by_subject = defaultdict(list)

    for result in quiz_results:
        quizzes_by_subject[result.quiz.subject.name].append({
            "title": result.quiz.title,
            "due_date": result.quiz.due_date,
            "status": result.status,
            "score": result.score if result.score is not None else "-",
        })

    return render(request, "backend/student/my_quiz.html", {"quizzes_by_subject": quizzes_by_subject})

       
       
       
  

@login_required
def profile_view(request):
    student = get_object_or_404(Student, user=request.user)
    return render(request, "profile.html", {"student": student})


@login_required
def setting(request):
    """ Student Settings Page """
    if request.method == "POST" and "old_password" in request.POST:
        # Agar user ne password change form submit kiya
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # password change ke baad login session active rakho
            messages.success(request, "Password updated successfully.")
            return redirect("setting")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, "backend/setting.html", {"form": form})


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Student, Subject



from django.shortcuts import render
from backend.models import Student, StudentSemester

def my_sem(request):
    try:
        student = Student.objects.get(user=request.user)
        student_semester = StudentSemester.objects.filter(student=student).order_by('-id').first()
        semester = student_semester.semester if student_semester else None

        #  Fetch related data
        midterm_announcement = None
        final_announcement = None
        notes = None

        if semester:
            # Fetch exam announcements
            midterm_announcement = Announcement.objects.filter(
                semester=semester, type__icontains="midterm"
            ).order_by('-date_posted').first()

            final_announcement = Announcement.objects.filter(
                semester=semester, type__icontains="final"
            ).order_by('-date_posted').first()

            # Fetch uploaded notes
            notes = Material.objects.filter(
                semester=semester,
                subject__in=semester.subjects.all()
            ).order_by('-uploaded_at')[:5]  # last 5 notes

    except Student.DoesNotExist:
        student = None
        semester = None
        student_semester = None
        midterm_announcement = None
        final_announcement = None
        notes = None

    return render(
        request,
        'backend/student/my_sem.html',
        {
            "student": student,
            "semester": semester,
            "student_semester": student_semester,
            "midterm_announcement": midterm_announcement,
            "final_announcement": final_announcement,
            "notes": notes,
        }
    )

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from backend.models import Student, Subject

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from backend.models import Student, Subject

from backend.models import Student, StudentSemester, AssignedSubject

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Student, StudentSemester, AssignedSubject, Subject


from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import Subject, Student, StudentSemester, AssignedSubject, Material, LectureFeedback


# Student Subjects + Lectures
from django.db.models import Prefetch


# Student Subjects + Lectures
@login_required
def subject_view(request):
    try:
        student = Student.objects.get(user=request.user)

        # Student ke saare semesters fetch karo
        student_semesters = StudentSemester.objects.filter(student=student)

        if student_semesters.exists():
            # In semesters ke saare subjects le aao
            subject_ids = (
                AssignedSubject.objects.filter(
                    semester__in=student_semesters.values_list("semester", flat=True)
                )
                .values_list("subject", flat=True)
                .distinct()
            )

            # Subjects ke saath unke materials (lectures) bhi prefetch karo
            subjects = Subject.objects.filter(id__in=subject_ids).prefetch_related("material_set")

        else:
            subjects = Subject.objects.none()

    except Student.DoesNotExist:
        subjects = Subject.objects.none()

    return render(request, "backend/student/subject.html", {
        "subjects": subjects
    })


# Save Lecture Feedback (AJAX request)
@login_required
@csrf_exempt

 
def save_feedback(request):
    if request.method == "POST":
        lecture_id = request.POST.get("lecture_id")   # <-- id le raha hai
        feedback_text = request.POST.get("feedback")
        rating = request.POST.get("rating")

        try:
            student = Student.objects.get(user=request.user)
            lecture = Material.objects.get(id=lecture_id)   # <-- ab id se fetch karega

            LectureFeedback.objects.create(
                lecture=lecture,
                student=student,
                feedback_text=feedback_text,
                rating=rating
            )

            return JsonResponse({"success": True, "message": "Feedback saved successfully!"})
        except Material.DoesNotExist:
            return JsonResponse({"success": False, "message": "Lecture not found!"})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})

    return JsonResponse({"success": False, "message": "Invalid request"})
        
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Performance, Student


from django.db.models import Avg
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Student, Performance

@login_required
def teacher_performance_view(request):
    student = get_object_or_404(Student, user=request.user)
    performances = Performance.objects.filter(student=student).order_by("subject__title")

    cgpa = None
    if performances.exists():
        total_percentage = 0
        to_update = []

        for perf in performances:
            # weightage: assignment (10), quiz (5), midterm (25), final (60)
            obtained = (perf.assignment or 0) + (perf.quiz or 0) + (perf.midterm or 0) + (perf.final or 0)
            total = 100  # ab fix 100 marks ka scale
            percentage = (obtained / total) * 100
            total_percentage += percentage

            perf.remarks = "Pass" if percentage >= 50 else "Fail"
            to_update.append(perf)

        # bulk update remarks
        Performance.objects.bulk_update(to_update, ["remarks"])

        # CGPA (100% = 4.0 scale)
        cgpa = round((total_percentage / performances.count()) / 25, 2)

    return render(
        request,
        "backend/student/teacherperformance.html",
        {"performances": performances, "cgpa": cgpa}
    )





from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import FeedbackForm  
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import FeedbackForm


def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            if request.user.is_authenticated:
                feedback.user = request.user
            feedback.save()

            #  User ka naam safely lena
            if feedback.user:
                if feedback.user.first_name:
                    user_name = feedback.user.first_name  # sirf first name
                elif feedback.user.username:
                    user_name = feedback.user.username    # agar first name nahi hai to username
                else:
                    user_name = feedback.user.email.split('@')[0] if feedback.user.email else "Anonymous"
            else:
                user_name = "Anonymous"

            # send email
            subject = "New Feedback Received"
            message = f"""
You have received a new feedback:

Type: {feedback.get_feedback_type_display()}
User: {user_name}
Email: {feedback.email if feedback.email else "Not Provided"}

Feedback:
{feedback.feedback_text}
"""
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,   # sender
                ["234noureena@gmail.com"],     # receiver (apna Gmail)
                fail_silently=False,
            )

            messages.success(request, "✅ Thanks! Your feedback has been sent.")
            return redirect('feedback')
        else:
            messages.error(request, "⚠️ Please fix the errors below.")
    else:
        form = FeedbackForm()

    return render(request, 'backend/student/feedback.html', {"form": form})


# ---------- Announcements ----------
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Announcement
 # assuming you have a Student model

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from backend.models import Announcement

from datetime import timedelta
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def announcement_view(request):
    user = request.user
    try:
        student_profile = getattr(user, "student_profile", None)

        #  Latest assigned semester
        student_semester_obj = (
            StudentSemester.objects.filter(student=student_profile)
            .order_by("-id")
            .first()
        )
        assigned_semester = student_semester_obj.semester if student_semester_obj else None

        #  Purani (20 din se zyada old) announcements delete
        cutoff_date = now() - timedelta(days=20)
        Announcement.objects.filter(date_posted__lt=cutoff_date).delete()

        if assigned_semester:
            announcements = Announcement.objects.filter(
                semester=assigned_semester,
                date_posted__gte=cutoff_date   #  Only fresh announcements
            ).order_by('-date_posted')
        else:
            announcements = Announcement.objects.none()

    except AttributeError:
        announcements = Announcement.objects.none()

    context = {
        "announcements": announcements
    }
    return render(request, "backend/student/annoucement.html", context)

# ---------- Student Performance ----------
from .models import StudentPerformance

from django.shortcuts import render
from django.contrib.auth.decorators import login_required












# backend/views.py
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "backend/login/password_reset_confirm.html"   # apna template yahan do
    success_url = reverse_lazy("SignIn")  # reset ke baad kidhar redirect karna hai



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Student, Assignment, Performance
from .forms import AssignmentForm

@login_required
def upload_assignment(request):
    student = get_object_or_404(Student, user=request.user)

    if request.method == "POST":
        form = AssignmentForm(request.POST, request.FILES, student=student)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.uploaded_by = request.user
            assignment.student = student   # 🔹 ye line add karo
            assignment.save()

            messages.success(request, "Assignment uploaded successfully!")
            return redirect("upload_assignment")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = AssignmentForm(student=student)

    assignments = Assignment.objects.filter(uploaded_by=request.user).order_by("-uploaded_at")

    return render(
        request,
        "backend/student/upload_assignment.html",
        {"form": form, "assignments": assignments}
    )
