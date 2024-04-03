# models.py
from django.db import models
from django.contrib.auth.models import User


class Departement(models.Model):
    nom = models.CharField(max_length=255)

class Employer(models.Model):
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    contact = models.CharField(max_length=255)
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE)
    montant_journalier = models.IntegerField(null=True)

class Salaire(models.Model):
    employer = models.ForeignKey('Employer', on_delete=models.CASCADE)
    montant = models.IntegerField(null=True)

