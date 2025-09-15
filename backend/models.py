from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

# ---------------------------
# Custom User Model
# ---------------------------
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # login with email

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
 #  yeh naya add karo
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.username} ({self.role})"


# ---------------------------
# Subject & Semester
# ---------------------------
class Subject(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100, blank=True, null=True)
    code = models.CharField(max_length=20, unique=True)
    
    teacher = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'teacher'},
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.code} - {self.name}"


class Semester(models.Model):
    title = models.CharField(max_length=100, unique=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    subjects = models.ManyToManyField(Subject, blank=True)

    # merged fields from student dashboard
    midterm_date = models.DateField(blank=True, null=True)
    final_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


# ---------------------------
# Student
# ---------------------------
class Student(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'},
        null=True,
        blank=True,
        related_name="student_profile" 
      
    )
    name = models.CharField(max_length=100, blank=True, null=True)
    reg_no = models.CharField(max_length=50, unique=True, blank=True, null=True)
    reg_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    roll_no = models.CharField(max_length=30, blank=True, null=True)  # merged
    email = models.EmailField(unique=True, blank=True, null=True)
    contact = models.CharField(max_length=15, blank=True, null=True)
    father_name = models.CharField(max_length=100, blank=True, null=True)
    father_contact = models.CharField(max_length=15, blank=True, null=True)
    image = models.ImageField(upload_to='students/', blank=True, null=True)
    photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)  # merged
    department = models.CharField(max_length=100, blank=True)  # merged
    address = models.TextField(blank=True, null=True)
    

    STATUS_CHOICES = [('Active', 'Active'), ('Inactive', 'Inactive')]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Active")

    semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        if self.user:
            return f"{self.user.get_full_name()} ({self.reg_no or self.reg_number or self.roll_no})"
        return self.name or "Unnamed Student"

    @property
    def display_name(self):
        return self.user.first_name if self.user else self.name


# ---------------------------
# Teacher
# ---------------------------
class Teacher(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'teacher'},
        null=True,
        blank=True
    )
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    contact = models.CharField(max_length=20, blank=True, null=True)
    qualification = models.CharField(max_length=100)
    experience = models.PositiveIntegerField()
    image = models.ImageField(upload_to='teachers/', null=True, blank=True)
    address = models.TextField(blank=True)

    STATUS_CHOICES = [('active', 'Active'), ('inactive', 'Inactive')]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return self.user.get_full_name() if self.user else self.name


# ---------------------------
# Assigned Subject
# ---------------------------
class AssignedSubject(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    class_days = models.CharField(max_length=50)
    schedule = models.CharField(max_length=100)
    assigned_on = models.DateField(auto_now_add=True)
    class Meta:
        unique_together = ('teacher', 'semester', 'subject')

    def __str__(self):
        return f"{self.teacher} - {self.subject.name} ({self.semester.title})"


# ---------------------------
# Contact Message
# ---------------------------
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.subject}"


# ---------------------------
# Activity Log
# ---------------------------
class ActivityLog(models.Model):
    admin_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.admin_user.username} - {self.action}"

from django.db import models
from django.conf import settings

class Activity(models.Model):
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="activities"
    )
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.teacher.email} - {self.action} ({self.timestamp})"

# ---------------------------
# Student ↔ Semester Mapping
# ---------------------------
class StudentSemester(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)   #  Start Date
    end_date = models.DateField(null=True, blank=True)     # End Date

    class Meta:
        unique_together = ('student', 'semester', 'teacher')

    def __str__(self):
        teacher_name = self.teacher.user.username if self.teacher and self.teacher.user else "No Teacher"
        return f"{self.student} - {self.semester.title} - {teacher_name}"


# ---------------------------
# Upload Material
# ---------------------------
class Material(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    lecture_title = models.CharField(max_length=255)
    pdf_file = models.FileField(upload_to="materials/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.lecture_title} - {self.subject.name}"


# ---------------------------
# Quiz & Question
# ---------------------------
class Quiz(models.Model):
    title = models.CharField(max_length=200)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    due_date = models.DateField(default=timezone.now, null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True) 
    end_time = models.DateTimeField(null=True, blank=True)    
    duration_minutes = models.PositiveIntegerField(default=10)  
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} ({self.subject.name})"


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name="questions", on_delete=models.CASCADE)
    text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=1, choices=[("A","A"),("B","B"),("C","C"),("D","D")])

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    text = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text} ({'Correct' if self.is_correct else 'Wrong'})"

class QuizResult(models.Model):
    STATUS_CHOICES = [
        ("Not Attempted", "Not Attempted"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
    ]

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="quiz_results"
    )
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="results")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Not Attempted")
    score = models.IntegerField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.student.username} - {self.quiz.title} ({self.status})"

# ---------------------------
# Performance
# ---------------------------
from django.db import models
from django.conf import settings
from django.utils import timezone

class QuizResult(models.Model):
    STATUS_CHOICES = [
        ("Not Attempted", "Not Attempted"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
    ]

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="quiz_results"
    )
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="results")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Not Attempted")
    score = models.IntegerField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    # New fields for timed quiz and storing answers
    started_at = models.DateTimeField(blank=True, null=True)
    answers_data = models.JSONField(blank=True, null=True)  # Stores {question_id: selected_option}

    def __str__(self):
        return f"{self.student.username} - {self.quiz.title} ({self.status})"

class Performance(models.Model):
    semester = models.ForeignKey(
        'Semester',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    assignment = models.IntegerField(default=0)   # default=0
    quiz = models.IntegerField(default=0)         #  default=0
    midterm = models.IntegerField(default=0)      #  default=0
    final = models.IntegerField(default=0)        #  default=0
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    remarks = models.TextField(null=True, blank=True)
    

    def __str__(self):
        return f"{self.student} - {self.subject}"
    def get_event_title(self):
        if self.assignment > 0:
            return "Assignment Due"
        elif self.quiz > 0:
            return "Quiz"
        elif self.midterm > 0:
            return "Midterm Exam"
        elif self.final > 0:
            return "Final Exam"
        return "Performance Update"
# ---------------------------
# Announcements
# ---------------------------
class Announcement(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    type = models.CharField(max_length=50)
    category = models.CharField(max_length=20, blank=True, null=True)  # merged
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_posted = models.DateField(null=True, blank=True)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title


# ---------------------------
# Assignments
# ---------------------------
class Assignment(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to="assignments/")
    description = models.TextField(blank=True, null=True)

    #  Kisne upload kiya (teacher ya student)
    uploaded_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="uploaded_assignments"
    )

    #  Agar student hai to kaun sa student hai
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="assignments"
    )

    #  Grading fields
    grade = models.CharField(max_length=10, blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)
    graded = models.BooleanField(default=False)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.subject.name})"


class StudentAssignment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="student_assignments")
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name="student_submissions")
    submission_file = models.FileField(upload_to="student_submissions/", blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    graded = models.BooleanField(default=False)
    grade = models.CharField(max_length=10, blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.student.reg_no} - {self.assignment.title}"

# ---------------------------
# Feedback
# ---------------------------
class Feedback(models.Model):
    FEEDBACK_TYPES = [
        ('complaint', 'Complaint'),
        ('suggestion', 'Suggestion'),
        ('question', 'Question'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    feedback_type = models.CharField(max_length=50, choices=FEEDBACK_TYPES)
    feedback_text = models.TextField()
    
    email = models.EmailField(blank=True, null=True)
    submitted_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.feedback_type} - {self.user}"
# ---------------------------
from django.conf import settings
from django.db import models

class TeacherFeedback(models.Model):
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='teacher_feedbacks'
    )
    feedback = models.TextField()
    student = models.ForeignKey(
        'Student', on_delete=models.CASCADE, related_name='student_feedbacks', null=True, blank=True
    )
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.teacher.username}"



class StudentPerformance(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    roll_no = models.CharField(max_length=20)
    subject = models.CharField(max_length=100)
    marks_obtained = models.FloatField()
    total_marks = models.FloatField()
    remarks = models.TextField(blank=True, null=True)
    date_recorded = models.DateField(auto_now_add=True)

    def percentage(self):
        return round((self.marks_obtained / self.total_marks) * 100, 2)

    def __str__(self):
        return f"{self.student.username} - {self.subject}"
    





from django.db import models
from django.conf import settings

class Task(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    is_submitted = models.BooleanField(default=False)  # True = Submitted, False = Not Submitted

class Achievement(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)

class Note(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()

class Todo(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)

class Event(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    date = models.DateField()


class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.message[:20]}"



class LectureFeedback(models.Model):
    lecture = models.ForeignKey(Material, on_delete=models.CASCADE, related_name="lecture_feedbacks")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="feedbacks")
    feedback_text = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.student} → {self.lecture.lecture_title} ({self.rating}⭐)"
