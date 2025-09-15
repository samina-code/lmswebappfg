from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

import re
from .models import (
    ContactMessage,
    Teacher,
    StudentSemester,
    Student,
    Semester,
    AssignedSubject,
    Subject,
    CustomUser,
    Material,
    Quiz,
    Question,
    Performance,
    Announcement,
    Assignment,
)

# 🎓 Student Form
class StudentForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Student
        fields = [
            'name', 'email',
            'reg_number', 'reg_no',
            'contact', 'father_name', 'father_contact',
            'image', 'address', 'semester'
        ]
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name and not re.fullmatch(r"[A-Za-z\s]{2,}", name):
            raise ValidationError("Name must contain only letters and at least 2 characters.")
        return name

    def clean_contact(self):
        contact = self.cleaned_data.get('contact')
        if contact and not re.fullmatch(r"\d{11,13}", contact):
            raise ValidationError("Contact must be 11–13 digits (e.g. 923XXXXXXXXX).")
        return contact

    def clean_father_contact(self):
        f_contact = self.cleaned_data.get('father_contact')
        if f_contact and not re.fullmatch(r"\d{11,13}", f_contact):
            raise ValidationError("Father's contact must be 11–13 digits (e.g. 923XXXXXXXXX).")
        return f_contact

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Student.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email

    def clean_reg_number(self):
        reg = self.cleaned_data.get('reg_number')
        if reg and Student.objects.exclude(pk=self.instance.pk).filter(reg_number=reg).exists():
            raise ValidationError("This registration number is already in use.")
        return reg


# 🧑 Update Student Form
class UpdateStudentForm(forms.ModelForm):
    name = forms.CharField(max_length=100, required=True, label="Student Name")
    email = forms.EmailField(required=True, label="Student Email")

    class Meta:
        model = Student
        fields = [
            'name', 'email',
            'reg_no', 'reg_number',
            'contact', 'father_name', 'father_contact',
            'image', 'address', 'semester'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['name'].initial = self.instance.name

            self.fields['email'].initial = self.instance.user.email

    def clean_contact(self):
        contact = self.cleaned_data.get('contact')
        if not contact.isdigit() or len(contact) not in [11, 13]:
            raise forms.ValidationError("Contact must be 11 or 13 digits (e.g. 923XXXXXXXXX).")
        return contact

    def clean_father_contact(self):
        father_contact = self.cleaned_data.get('father_contact')
        if not father_contact.isdigit() or len(father_contact) not in [11, 13]:
            raise forms.ValidationError("Father's contact must be 11 or 13 digits (e.g. 923XXXXXXXXX).")
        return father_contact

    def save(self, commit=True):
        student = super().save(commit=False)
        if commit and student.user:
            student.user.first_name = self.cleaned_data['name']
            student.user.email = self.cleaned_data['email']
            student.user.save()
            student.save()
        return student


# 👨‍🏫 Teacher Form
class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'contact', 'email', 'qualification', 'experience', 'image', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter full name'}),
            'contact': forms.TextInput(attrs={'placeholder': '923XXXXXXXXX'}),
            'email': forms.EmailInput(attrs={'placeholder': 'example@email.com'}),
            'qualification': forms.TextInput(attrs={'placeholder': 'e.g. M.Sc. Physics'}),
            'experience': forms.NumberInput(attrs={'placeholder': 'Years of experience'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name and not re.fullmatch(r"[A-Za-z\s]{2,}", name):
            raise ValidationError("Name must contain only letters and at least 2 characters.")
        return name

    def clean_contact(self):
        contact = self.cleaned_data.get('contact')
        if not re.fullmatch(r"\d{13}", contact):
            raise ValidationError("Contact must be exactly 13 digits (e.g. 923XXXXXXXXX).")
        return contact

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Teacher.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("This email is already registered.")
        return email

    def clean_experience(self):
        exp = self.cleaned_data.get('experience')
        if exp is not None and exp < 0:
            raise ValidationError("Experience cannot be negative.")
        return exp


# 🔹 Update Teacher Form
class UpdateTeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'contact', 'email', 'qualification', 'experience', 'image', 'address' ]

    def clean_contact(self):
        contact = self.cleaned_data.get('contact')
        if not contact.isdigit() or len(contact) != 13:
            raise forms.ValidationError("Contact must be exactly 13 digits (e.g. 923XXXXXXXXX).")
        return contact

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Teacher.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("This email is already registered with another teacher.")
        return email

    def clean_experience(self):
        exp = self.cleaned_data.get('experience')
        if exp < 0:
            raise ValidationError("Experience cannot be negative.")
        return exp


# 📘 Semester Form
class SemesterForm(forms.ModelForm):
    SEMESTER_CHOICES = [("Semester " + str(i), "Semester " + str(i)) for i in range(1, 9)]

    title = forms.CharField(
        widget=forms.Select(
            choices=SEMESTER_CHOICES,
            attrs={'class': 'form-control'}
        )
    )

    class Meta:
        model = Semester
        fields = ['title', 'start_date', 'end_date', 'subjects']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'subjects': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
        error_messages = {
            'title': {
                'required': "Semester title is required.",
                'unique': "This semester title already exists.",
            },
            'start_date': {
                'required': "Start date is required.",
            },
            'end_date': {
                'required': "End date is required.",
            },
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("End date must be greater than start date.")

        title = cleaned_data.get("title")
        if title and Semester.objects.exclude(pk=self.instance.pk).filter(title__iexact=title).exists():
            raise forms.ValidationError("This semester title already exists.")

        return cleaned_data


# 🧑‍🎓 Assign Semester to Student
class AssignSemesterForm(forms.ModelForm):
    class Meta:
        model = StudentSemester
        fields = ['student', 'semester', 'teacher','start_date', 'end_date']


# 📩 Contact Us Form
class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']


# 📚 Assign Subject to Teacher
class AssignSubjectForm(forms.ModelForm):
    class Meta:
        model = AssignedSubject
        fields = ['semester', 'subject', 'teacher']


# 🔑 Login Form
class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'})
    )


# 🔹 User Registration Form
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'role']


# 📂 Material Upload Form
class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['subject', 'lecture_title', 'pdf_file', 'teacher', 'semester']

# 📝 Quiz Form
class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['semester', 'subject', 'title', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }


# ❓ Question Form
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'correct_answer']


# 📊 Performance Form
class PerformanceForm(forms.ModelForm):
    class Meta:
        model = Performance
        fields = ['student', 'semester', 'subject', 'assignment', 'quiz', 'midterm', 'final']


# 📢 Announcement Form
class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['teacher', 'semester', 'subject', 'type', 'title', 'description']

    def clean_message(self):
        message = self.cleaned_data.get("message")
        if len(message) < 5:
            raise ValidationError("Announcement must be at least 5 characters long.")
        return message


#  Assignment Form
# backend/forms.py

from django import forms
from .models import Assignment

# forms.py
from django import forms
from backend.models import Assignment

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ["subject", "title", "file", "description"]

    def __init__(self, *args, **kwargs):
        student = kwargs.pop("student", None)   # student pass karna hoga
        super().__init__(*args, **kwargs)

        if student:
            # 🔹 Student ka latest assigned semester nikaalna
            student_semester = student.studentsemester_set.order_by("-id").first()
            if student_semester and student_semester.semester:
                self.fields["subject"].queryset = student_semester.semester.subjects.all()
            else:
                self.fields["subject"].queryset = Subject.objects.none()

#  Subject Form
import re
from django import forms
from .models import Subject

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['title', 'code', 'teacher']

    def __init__(self, *args, **kwargs):
        self.semester = kwargs.pop("semester", None)
        super().__init__(*args, **kwargs)

    def clean_code(self):
        code = self.cleaned_data.get("code")
        if self.semester and self.semester.subjects.filter(code__iexact=code).exists():
            raise forms.ValidationError("This subject code already exists in this semester.")
        return code
def clean_title(self):
    title = self.cleaned_data.get('title')  # safer way to get value

    if not title:
        raise forms.ValidationError("Semester title is required.")

    # Now title is guaranteed to be a string
    if not re.match(r'^[A-Za-z0-9\-_ ]+$', title):
        raise forms.ValidationError("Title can only contain letters, numbers, spaces, dash and underscore.")

    return title

    def clean_title(self):
        title = self.cleaned_data.get("title")

        # ✅ Allow only alphabets, numbers, spaces, dash, underscore
        if not re.match(r'^[A-Za-z0-9\-_ ]+$', title):
            raise forms.ValidationError(
                "Title can only contain letters, numbers, spaces, hyphen (-), and underscore (_)."
            )

        # ✅ Duplicate check inside the same semester
        if self.semester and self.semester.subjects.filter(title__iexact=title).exists():
            raise forms.ValidationError("This subject title already exists in this semester.")

        return title






from django import forms
from .models import Student
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()


class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Student   # ya CustomUser agar profile pic CustomUser me hai
        fields = ['image']  # ya ['photo'] agar tum photo field use karna chahte ho


class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']


from django import forms



from django import forms
from .models import TeacherFeedback

from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['feedback_type', 'feedback_text', 'email']
        widgets = {
            'feedback_type': forms.Select(attrs={'class': 'form-control'}),
            'feedback_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }





class AssignmentSubmissionForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['file', 'description']

    def clean_description(self):
        description = self.cleaned_data.get('description', '')
        if len(description) < 5:
            raise forms.ValidationError("Description must be at least 5 characters long.")
        return description
    
from django.contrib.auth.forms import UserCreationForm
from .models import StudentPerformance

class StudentPerformanceForm(forms.ModelForm):
    class Meta:
        model = StudentPerformance
        fields = ['roll_no', 'subject', 'marks_obtained', 'total_marks', 'remarks']

    def clean(self):
        cleaned_data = super().clean()
        marks_obtained = cleaned_data.get("marks_obtained")
        total_marks = cleaned_data.get("total_marks")

        if marks_obtained and total_marks and marks_obtained > total_marks:
            raise forms.ValidationError("Marks obtained cannot be greater than total marks.")

        return cleaned_data


from django import forms
from .models import LectureFeedback

class LectureFeedbackForm(forms.ModelForm):
    class Meta:
        model = LectureFeedback
        fields = ["feedback_text", "rating"]
        widgets = {
            "feedback_text": forms.Textarea(attrs={"rows": 3, "placeholder": "Write your feedback..."}),
            "rating": forms.NumberInput(attrs={"min": 1, "max": 5}),
        }
