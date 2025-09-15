from django.urls import path
from django.contrib.auth import views as auth_views
from .views import CustomPasswordResetConfirmView
  
from . import views

urlpatterns = [
    # Public Pages
    path('', views.home, name='Home'),
     path('login/', views.SignIn, name='SignIn'),
    path('logout/', views.logout_view, name='logout'),
    path('contact/', views.contact_view, name='contact'),

    # Admin Dashboard

    path('admindashboard/', views.admin_dashboard, name='admindashboard'),
    path("admindashboard/messages/", views.open_messages, name="open_messages"),  # 👈 yeh add karo

    # Add these for sidebar links:
    path('admin/manage-students/', views.manage_students, name='managestudent'),
    path('admin/manage-teachers/', views.manage_teachers, name='manageaddteacher'),
    path('admin/manage-semesters/', views.manage_semesters, name='adminstudentsemester'),
    
    
    path('manage-students/', views.manage_students, name='managestudents'),

   
    path('students/delete/<int:student_id>/', views.delete_student, name='delete_student'),
    
    path('students/', views.manage_students, name='manage_students'),
    path('students/add/', views.add_student, name='add_student'),
    path('assign-semester/<int:student_id>/', views.assign_semester, name='assign_semester'),
    path('update-student/<int:student_id>/', views.update_student, name='update_student'),


    
    



    
    path('assign-subject/<int:teacher_id>/', views.assign_subject, name='assign_subject'),
  
    
      path('add-student/', views.add_student, name='manage_students'),
    path('view-students/', views.view_students, name='view_students'),

    
    
    
    path('manage-semesters/', views.manage_semesters, name='manage_semesters'),
    
    
    
    path('view-teachers/', views.view_teachers, name='view_teachers'),
    
     

      path('manage-teachers/', views.manage_teachers, name='manageaddteacher'),
          
    path('update-teacher/<int:teacher_id>/', views.update_teacher, name='update_teacher'),
    path('delete-teacher/<int:teacher_id>/', views.delete_teacher, name='delete_teacher'),
  # View ONE teacher's details
  
  
  
  
  
  path("teacher/<int:teacher_id>/subjects/", views.teacher_subjects, name="teacher_subjects"),
  path("assigned-subject/delete/<int:pk>/", views.delete_assigned_subject, name="delete_assigned_subject"),


    # Optional for assigning subjects:
    # path('assign-subject/<int:teacher_id>/', views.assign_subject, name='assign_subject'),
       path('ajax/get-subjects/', views.get_subjects_by_semester, name='get_subjects_by_semester'),
     path('ajax/get_students/<int:semester_id>/', views.get_students_by_semester, name='get_students_by_semester'),
    
    
    #teacher
    
   

    # Dashboards
     path('teacher/dashboard/', views.teacher_dashboard, name="teacher_dashboard"),
    path("teacher/feedback/read/<int:feedback_id>/", views.mark_feedback_as_read, name="mark_feedback_as_read"),
     path('mark-feedback-read/', views.mark_all_feedback_as_read, name='mark_feedback_read'),

    path('teacher/my_subjects/', views.teacher_my_subjects, name="teacher_my_subjects"),
    path('teacher/my_students/', views.tmy_students, name="tmy_students"),

    path('teacher/upload_material/', views.upload_material, name="upload_material"),

    path('teacher/quiz_creator/', views.quiz_creator, name="quiz_creator"),
    
    
    path('teacher/update_performance/', views.update_performance, name="update_performance"),
    path('teacher/announcement/', views.teacher_announcement, name="teacher_announcement"),
     path("delete-announcement/<int:ann_id>/", views.delete_announcement, name="delete_announcement"),

    path('teacher/upload_assignment/', views.upload_assignment, name="upload_assignment"),
      path("get-subjects/<int:semester_id>/", views.get_subjects, name="get_subjects"),
       path("delete-material/<int:material_id>/", views.delete_material, name="delete_material"),

   path("teacher/upload_material/", views.upload_material, name="upload_material"),
    
      path("teacher/profile/", views.teacher_profile, name="profile"),

    # Settings
    path("teacher/settings/", views.teacher_settings, name="teacher_settings"),

    # Logout (Django auth ka built-in view)

    
    #student dashboard
   
     path('student/student_dashboard/', views.student_dashboard, name='student_dashboard'),
     path('student/delete_note/<int:note_id>/', views.delete_note, name='delete_note'),
     path('student/save_note/', views.save_note, name='save_note'),
     path("notifications/mark-read/", views.mark_notifications_read, name="mark_notifications_read"),

   
    path('api/id-stats/', views.id_stats_api, name='api_id_stats'),
   
    path('my_quiz/', views.my_quiz, name='my_quiz'),
    
    path('my_sem/', views.my_sem, name='my_sem'),
      
    path('subjects/', views.subject_view, name='subjects'),
    path("save-feedback/", views.save_feedback, name="save_feedback"),
    path('upload-assignment/', views.upload_assignment, name='upload_assignment'),
    # urls.py
path('upload-assignment/<int:assignment_id>/', views.upload_assignment, name='upload_assignment'),

    path('performance/', views.teacher_performance_view, name='teacherperformance'),
   # urls.py
   path('feedback/', views.feedback_view, name='feedback'),
   


    path('announcements/', views. announcement_view, name='announcement'), # replace as needed
    path('profile/', views.profile_view, name='profile'),
    path('quizzes/', views.quiz_list_view, name='quiz_list'),
    path('profile/', views.profile_view, name='profile'),
    path('setting/', views.setting, name='setting'),

    
    # urls.py


    # ... existing urls

    # Password reset workflow
   
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='backend/login/password_reset_form.html'
        ),
        name='password_reset'
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='backend/login/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
   
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='backend/login/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),

 
    
    path(
    'reset/<uidb64>/<token>/',
    CustomPasswordResetConfirmView.as_view(),
    name='password_reset_confirm'
),
    
    
    
    
    
    
    
  

    # Add these too:
path('api/chart/students/', views.chart_data_students_by_semester, name='chart_students'),
path('api/chart/teachers/', views.chart_data_teachers_by_semester, name='chart_teachers'),
path('api/chart/activity/', views.chart_data_semester_activity, name='chart_activity'),
# Charts API
path('quiz/<int:quiz_id>/start/', views.start_quiz, name='start_quiz')




]


