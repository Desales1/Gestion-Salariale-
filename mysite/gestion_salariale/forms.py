from django import forms
from .models import Employer,Departement
from django.core.exceptions import ValidationError

class EmployerForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ['departement','nom', 'prenom', 'email', 'contact', 'montant_journalier']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personnaliser les libellés du champ departement pour afficher le nom du département
        self.fields['departement'].label_from_instance = lambda obj: obj.nom
        self.fields['montant_journalier'].required = False

class DepartementForm(forms.ModelForm):
    class Meta:
        model = Departement
        fields = ['nom']

    def clean_nom(self):
        nom = self.cleaned_data['nom']
        # Vérifier si le nom du département existe déjà dans la base de données
        if Departement.objects.filter(nom=nom).exists():
            raise ValidationError("Ce département existe déjà. Veuillez en choisir un autre.")
        return nom