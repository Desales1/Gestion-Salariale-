# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('liste_employer/', views.liste_employer, name='liste_employer'),
    path('ajout_employer/', views.ajout_employer, name='ajout_employer'),
    path('modifier_employer/<int:employer_id>/', views.modifier_employer, name='modifier_employer'),
    path('supprimer_employer/<int:employer_id>/', views.supprimer_employer, name='supprimer_employer'),
    path('liste_departement/', views.liste_departement, name='liste_departement'),
    path('ajout_departement/', views.ajout_departement, name='ajout_departement'),
   path('modifier_departement/<int:departement_id>/', views.modifier_departement, name='modifier_departement'),
    path('supprimer_departement/<int:departement_id>/', views.supprimer_departement, name='supprimer_departement'),
    path('user_home/', views.user_home, name='user_home'),
    
    # autres routes nécessaires
]
