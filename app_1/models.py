from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Korisnik(AbstractUser):
    ROLES = (('adm', 'admin'),('prof', 'profesor'), ('stu', 'student'))
    STATUS = (('none', 'None'), ('izv', 'izvanredni student'), ('red', 'redovni student'))
    role = models.CharField(max_length=50, choices=ROLES)
    status = models.CharField(max_length=50, choices=STATUS)
    
class Predmeti(models.Model):
    IZBORNI = (('DA', 'da'), ('NE', 'ne'))
    name = models.CharField(max_length=50)
    kod = models.CharField(max_length=50)
    program = models.CharField(max_length=50)
    ects = models.IntegerField()
    sem_red = models.IntegerField()
    sem_izv = models.IntegerField()
    izborni = models.CharField(max_length=50, choices=IZBORNI)
    nositelj = models.ForeignKey(Korisnik, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
       return '%s %s %s %s %s %s %s %s' % (self.name, self.kod, self.program, self.ects, self.sem_red, self.sem_izv, self.izborni, self.nositelj)

class Upisi(models.Model):
    status = models.CharField(max_length=64)
    korisnik = models.ForeignKey(Korisnik, on_delete=models.CASCADE, blank=True, null=True)
    predmet = models.ForeignKey(Predmeti, on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
       return '%s %s %s' % (self.status, self.korisnik, self.predmet)
