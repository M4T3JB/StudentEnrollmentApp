from django.shortcuts import render, redirect
from django.http import HttpResponse
from .decorators import admin_required, professor_required, admin_professor_required, admin_student_required, student_required
from projekt.authentication import SettingsBackend
from .forms import PredmetiForma, AddUserForm
from .models import Korisnik, Predmeti, Upisi
from django.contrib.auth import login, logout
from django.core.paginator import Paginator
from django import forms  
from django.db.models import Count, Q
# Create your views here.
def check_logged_in_user(request):
    korisnikId = request.user.pk
    ulogirani_korisnik = Korisnik.objects.get(id=korisnikId)
    if ulogirani_korisnik.role == 'adm':
        return 'adminpage.html'
    elif ulogirani_korisnik.role == 'prof':
        return 'professorpage.html'
    else:
        return 'studentpage.html'

def checkUser(request, update=None):
    set = SettingsBackend()
    name = set.check_user_name(request.POST['username'])
    if(name is None):
        user = Korisnik(username=request.POST['username'], status=request.POST['status'], role=request.POST['role'])
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        set.checkPasswords(user, password1, password2)
        user.save()
    else:
        Korisnik.objects.filter(name=name).update(username=request.POST['username'], status=request.POST['status'], role=request.POST['role'], password=user.password)
    

########################## ADMIN PAGE SUBJECT FUNCTIONS #########################################
@admin_required
def detail_predmet(request, predmetId):
    predmet = Predmeti.objects.get(pk=predmetId)
    return render(request, 'detailpredmeta.html', {'predmet': predmet})

@admin_required
def edit_subject(request, predmetId):
    predmet = Predmeti.objects.get(pk=predmetId)
    if request.method == "GET":
        forma = PredmetiForma(instance=predmet)
        return render(request, 'editsubject.html', {'form': forma, 'values': {'DA': 'da', 'NE': 'ne'}, 'selvalue': predmet.izborni} )
    elif "update" in request.POST:
        forma = PredmetiForma( request.POST, instance=predmet)
        if forma.is_valid():
            print("forma je validna", forma)
            forma.save()
            return redirect('adminpage')
    elif "delete" in request.POST:
        return render(request, 'confirmdeletion.html',{'data': predmetId, 'name_obj': 'predmet'})

@admin_required
def add_subject(request):
    if request.method == "GET":
        forma = PredmetiForma()
        return render(request, 'addtemplate.html', {'form': forma})
    elif request.method == "POST":
        forma = PredmetiForma(request.POST)
        if forma.is_valid():
            forma.save()
        return redirect('adminpage')

########################## ADMIN PAGE STUDENT FUNCTIONS #########################################

@admin_required
def dodaj_studenta(request, status):
    if request.method == "GET":
        if(status == 'izv'):
            form = AddUserForm(initial={'role': 'stu', 'status': 'izv'})
            form.fields['status'].widget = forms.HiddenInput()
        elif(status == 'red'):
            form = AddUserForm(initial={'role': 'stu', 'status': 'red'})
            form.fields['status'].widget = forms.HiddenInput()
        return render(request, 'addtemplate.html', {'form': form})
    elif request.method == "POST":
            checkUser(request)
            return redirect('adminpage')

@admin_required
def delete_confirmed(request, id, name_obj):
    if 'yes' in request.POST:
        if name_obj == 'predmet':
            predmet = Predmeti.objects.get(id=id)
            predmet.delete()
        elif name_obj == 'student':
            student = Korisnik.objects.get(id=id)
            student.delete()
    return redirect('adminpage')

@admin_required
def edit_user(request, studentId):
    student = Korisnik.objects.get(pk=studentId)
    if request.method == "GET":
        forma = AddUserForm(instance=student)
        forma.fields['status'].widget = forms.HiddenInput()
        return render(request, 'edituser.html', {'form': forma})
    elif 'update' in request.POST:
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        set = SettingsBackend()
        student = set.checkPasswords(student, password1, password2)
        Korisnik.objects.filter(pk=studentId).update(username=student.username, status=request.POST['status'], role=request.POST['role'], password=student.password)
        return redirect('adminpage')

@admin_required
def delete_student(request, studentId):
    return render(request, 'confirmdeletion.html',{'data': studentId, 'name_obj': 'student'})

@admin_required
def redovni(request):
    studenti = Korisnik.objects.all().filter(role='stu', status='red')
    print(studenti[0].username)
    return render(request, 'redovni.html', {'studenti': studenti}) 

@admin_required
def izvanredni(request):
    studenti = Korisnik.objects.all().filter(role='stu', status='izv')
    return render(request, 'izvanredni.html', {'studenti': studenti}) 

@admin_professor_required
def students_on_subject(request, subjectId):
    page = check_logged_in_user(request)
    predmet = Predmeti.objects.get(pk=subjectId)
    upisi = Upisi.objects.all().filter(predmet=predmet)
    return render(request, 'studentsonsubject.html', {'upisi': upisi, 'page': page}) 

########################## ADMIN PAGE PROFESSOR FUNCTIONS #########################################
@admin_required
def add_professor(request):
    if request.method == "GET":
        form = AddUserForm(initial={'role': 'prof', 'status': 'none'})
        form.fields['status'].widget = forms.HiddenInput()
        return render(request, 'addtemplate.html', {'form': form})
    if request.method == 'POST':
        checkUser(request)
        return redirect('adminpage')
    
########################## ADMIN PAGE NAVBAR FUNCTIONS #########################################
@admin_required
def courses(request):
    queryset = Predmeti.objects.all()
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'courses.html', {'page_obj': page_obj})

@admin_required
def professors(request):
    profesori = Korisnik.objects.all().filter(role='prof')
    return render(request, 'professors.html', {'profesori': profesori})

@admin_required
def students(request):
    studenti = Korisnik.objects.all().filter(role='stu')
    return render(request, 'students.html', {'studenti': studenti})

@admin_required
def admin_page(request):
    return render(request, 'adminpage.html')

########################## PROFESSOR NAVBAR FUNCTIONS #########################################
@professor_required
def students_on_subject_prof(request, subjectId):
    predmet = Predmeti.objects.get(pk=subjectId)
    polozeni = Upisi.objects.all().filter(predmet=predmet, status='polozen')
    upisani = Upisi.objects.all().filter(predmet=predmet, status='upisan')
    if request.method == "POST":
        for list in upisani:
            if list.korisnik.username in request.POST:
                student = Korisnik.objects.get(username=list.korisnik.username)
                ul = Upisi.objects.filter(korisnik=student, predmet=predmet)
                ul.update(status="polozen", korisnik=student, predmet=predmet)
                polozeni = Upisi.objects.all().filter(predmet=predmet, status='polozen')
                upisani = Upisi.objects.all().filter(predmet=predmet, status='upisan')

    return render(request, 'studentsonsubjectprof.html', {'polozeni': polozeni, 'upisani': upisani}) 

@professor_required
def courses_professor(request):
    predmeti = Predmeti.objects.all().filter(nositelj=request.user.pk)
    return render(request, 'coursesprofessor.html', {'predmeti': predmeti})

@professor_required
def professor_page(request):
    return render(request, 'professorpage.html')

########################## STUDENT/ADMIN FUNCTION #########################################
@admin_student_required
def upisni_list(request, studentId):
    page = check_logged_in_user(request)
    predmeti = Predmeti.objects.all()
    student = Korisnik.objects.get(id=studentId)
    upisni = Upisi.objects.filter(korisnik=student)
    semestar = {1: 'Prvi', 2: 'Drugi', 3: 'Treci', 4: 'Cetvrti', 5: 'Peti', 6: 'Sesti'}

    polozeni = Upisi.objects.annotate()
    if student.status == 'red':
        prvi = polozeni.filter(predmet__sem_red=1, korisnik__username=student.username, status='polozen').count()
        drugi = polozeni.filter(predmet__sem_red=2, korisnik__username=student.username, status='polozen').count()
        
    else:
        prvi = polozeni.filter(predmet__sem_izv=1, korisnik__username=student.username, status='polozen').count()
        drugi = polozeni.filter(predmet__sem_izv=2, korisnik__username=student.username, status='polozen').count()
    
    ukupno = prvi + drugi

    if request.method == "POST":
        for predmet in predmeti:
            ul = Upisi.objects.filter(korisnik=student, predmet=predmet)
            if predmet.name in request.POST:
                if request.POST[predmet.name] == 'Dodaj': 
                    if ukupno > 9 or predmet.sem_red < 3 or predmet.sem_izv < 3:
                        if ul:
                            ul.update(status="upisan", korisnik=student, predmet=predmet)
                        else:
                            ul = Upisi(status="upisan", korisnik=student, predmet=predmet)
                            ul.save()
                elif request.POST[predmet.name] == 'Potvrdi':
                    ul.update(status="polozen", korisnik=student, predmet=predmet)
                elif request.POST[predmet.name] == 'Izbriši':
                    ul.delete()

    if student.status == 'red':
        return render(request, 'upisnilistredovni.html', {'predmeti': predmeti, 'upisni': upisni, 'semestar': semestar, 'page': page})
    
    semestar.update({7: 'Sedmi', 8: 'Osmi'})
    return render(request, 'upisnilistizvanredni.html', {'predmeti': predmeti, 'upisni': upisni, 'semestar': semestar, 'page': page})

########################## STUDENT NAVBAR FUNCTION ######################################### 
@student_required
def student_page(request):
    return upisni_list(request, request.user.pk)

################ LOGIN/LOGOUT FUNCTION ############

def auth_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = None
        set = SettingsBackend()
        user = set.authenticate(username=username, password=password)
        if user is not None:
            login(request, user)

            user = Korisnik.objects.values().filter(username=username)
            rola = user[0]['role']
            if(rola == 'adm'):
                return redirect('adminpage')
            elif(rola == 'prof'):
                return redirect('professorpage')
            elif(rola == 'stu'):
                return redirect('studentpage')
        else:             
            message = {"message": "Invalid credentials! Please enter valid data"}
            return render(request, 'login.html', message) 
    return render(request, 'login.html') 

def auth_logout(request):
    logout(request)
    return render(request, 'logout.html')

@student_required
def obrana(request):
    user_input = request.GET.get('input')
    sortirani = []  

    if user_input is not None and user_input.isdigit():
        input_value = int(user_input)
        all_subjects = Predmeti.objects.all()
        sortirani = [subject for subject in all_subjects if subject.ects > input_value]

    predm = {'subjects': sortirani}
    return render(request, 'obrana.html', predm)

@student_required
def filtriraj_po_semestru(request):
    user_input = request.GET.get('semestar')

    if user_input:
        predmeti = Predmeti.objects.filter(sem_red=user_input)
    else:
        predmeti = Predmeti.objects.all()  

    predm = {'predmeti': predmeti, 'semestar': user_input}
    return render(request, 'filtriraj_po_semestru.html', predm)


@student_required
def filtracija(request):
    user_input_ects = request.GET.get('ects')
    user_input_semestar = request.GET.get('semestar')

    predmeti = Predmeti.objects.all()

    if user_input_ects and user_input_ects.isdigit():
        input_value = int(user_input_ects)
        predmeti = predmeti.filter(ects__gt=input_value)

    if user_input_semestar:
        predmeti = predmeti.filter(sem_red=user_input_semestar)

    context = {
        'predmeti': predmeti,
        'ects_input': user_input_ects,
        'semestar_input': user_input_semestar,
    }
    return render(request, 'filtracija.html', context)