from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Employer
from django.contrib.auth.models import User,Group
from .models import Departement
from .forms import EmployerForm,DepartementForm




@login_required
def home(request):
    user = request.user
    # Vérifier si l'utilisateur appartient au groupe "Administrateur"
    if user.groups.filter(name='Administrateur').exists():
        # Si l'utilisateur est administrateur, afficher la page d'accueil de l'administrateur
        return render(request, 'admin_home.html')
    else:
        # Sinon, afficher la page d'accueil des employés
        return render(request, 'user_home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin_home')
            else:
                return redirect('user_home')
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

@login_required
def admin_home(request):
    if request.user.is_superuser:
        total_employers = Employer.objects.count()
        total_departements = Departement.objects.count()
        total_admins = User.objects.filter(is_superuser=True).count()
        context = {
            'total_employers': total_employers,
            'total_departements': total_departements,
            'total_admins': total_admins,
        }
        return render(request, 'admin_home.html', context)
    else:
        return redirect('user_home')



def user_home(request):
    if not request.user.is_superuser:
        return render(request, 'user_home.html')
    else:
        return redirect('admin_home')
    
@login_required
def liste_employer(request):
    employers = Employer.objects.all()  # Récupère tous les employés
    return render(request, 'liste_employer.html', {'employers': employers})

@login_required
def ajout_employer(request):
    if request.method == 'POST':
        form = EmployerForm(request.POST)
        if form.is_valid():
            # Vérifier si l'e-mail existe déjà dans la base de données
            email = form.cleaned_data['email']
            if Employer.objects.filter(email=email).exists():
                # Afficher un message d'erreur si l'e-mail existe déjà
                form.add_error('email', 'Cet e-mail existe déjà. Veuillez en choisir un autre.')
        if form.is_valid():
            # Vérifier si le contact existe déjà dans la base de données
            contact = form.cleaned_data['contact']
            if Employer.objects.filter(contact=contact).exists():
                # Afficher un message d'erreur si le contact existe déjà
                form.add_error('contact', 'Ce numéro de contact existe déjà. Veuillez en choisir un autre.')
            else:
                # Enregistrer l'employé s'il n'existe pas déjà dans la base de données
                form.save()
                return redirect('liste_employer')
    else:
        form = EmployerForm()
    return render(request, 'ajout_employer.html', {'form': form})


@login_required
def modifier_employer(request, employer_id):
    employer = get_object_or_404(Employer, id=employer_id)
    departements = Departement.objects.all()
    if request.method == 'POST':
        form = EmployerForm(request.POST, instance=employer)
        if form.is_valid():
            form.save()
            return redirect('liste_employer')
    else:
        form = EmployerForm(instance=employer)
    return render(request, 'modifier_employer.html', {'form': form, 'departements': departements})

@login_required
def supprimer_employer(request, employer_id):
    employer = get_object_or_404(Employer, id=employer_id)
    employer.delete()
    return redirect('liste_employer')

@login_required
def liste_departement(request):
    departements = Departement.objects.all()[:10]  # Récupère les 10 premiers départements
    return render(request, 'liste_departement.html', {'departements': departements})

@login_required
def ajout_departement(request):
    if request.method == 'POST':
        form = DepartementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_departement')
    else:
        form = DepartementForm()
    return render(request, 'ajout_departement.html', {'form': form})

@login_required
def modifier_departement(request, departement_id):
    departement = Departement.objects.get(id=departement_id)
    if request.method == 'POST':
        form = DepartementForm(request.POST, instance=departement)
        if form.is_valid():
            form.save()
            return redirect('liste_departement')
    else:
        form = DepartementForm(instance=departement)
    return render(request, 'modifier_departement.html', {'form': form})


@login_required
def supprimer_departement(request, departement_id):
    departement = Departement.objects.get(id=departement_id)
    departement.delete()
    return redirect('liste_departement')



