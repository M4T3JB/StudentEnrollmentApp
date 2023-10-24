"""projekt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from app_1 import views
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.auth_login, name='login'),
    path('logout/', views.auth_logout, name='logout'),
    path('adminpage/', views.admin_page, name='adminpage'),
    path('professorpage/', views.professor_page, name='professorpage'),
    path('studentpage/', views.student_page, name='studentpage'),
    path('courses/', views.courses, name='courses'),
    path('coursesprof/', views.courses_professor, name='courses_professor'),
    path('professors/', views.professors, name='professors'),
    path('students/', views.students, name='students'),
    path('detailpredmeta/<int:predmetId>', views.detail_predmet, name='detail_predmet'),
    path('editsubject/<int:predmetId>', views.edit_subject, name='edit_subject'),
    path('addsubject/', views.add_subject, name='add_subject'),
    path('redovni/', views.redovni, name='redovni'),
    path('izvanredni/', views.izvanredni, name='izvanredni'),
    path('dodajstudenta/<str:status>', views.dodaj_studenta, name='dodaj_studenta'),
    path('edituser/<int:studentId>', views.edit_user, name='edit_user'),
    path('deletestudent/<int:studentId>', views.delete_student, name='delete_student'),
    path('addprofessor/', views.add_professor, name='add_professor'),
    path('deleteconfirmed/<int:id>/<str:name_obj>/', views.delete_confirmed, name='delete_confirmed'),
    path('studentsonsubject/<int:subjectId>/', views.students_on_subject, name='students_on_subject'),
    path('studentsonsubjectprof/<int:subjectId>/', views.students_on_subject_prof, name='students_on_subject_prof'),
    path('upisnilistredovni/<int:studentId>/', views.upisni_list, name='upisni_list'),
    path('upisnilistizvanredni/<int:studentId>/', views.upisni_list, name='upisni_list'),
    path('obrana/',views.obrana, name='obrana'),
    path('filtriraj_po_semestru/', views.filtriraj_po_semestru, name='filtriraj_po_semestru'),
    path('filtracija/',views.filtracija,name='filtracija'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
