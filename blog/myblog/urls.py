from django.urls import path
from . import views


urlpatterns=[


path('', views.conexion, name="conexion"),

path('inscription/', views.inscription, name="inscription"),

path('acceuils/', views.acceuils, name="acceuils"),

path('menus_publier/', views.publier, name="publier"),

path('articles/<int:id_article>/', views.article, name="article"),

path('supp/<int:id_cmt>/', views.supprimer, name="spp_cmt"),

path('mod/<int:id_cmt>/', views.modifier, name="modifier"),


path('myarticle/', views.myarticle, name="myarticle"),

#--------------- GESTION DES PROFILS- CONSULTATIONS
path('profils/<int:id>/', views.profils, name="profils"),

path('profils_user/', views.profils_user, name="profils_user"),
# ---------------------SUPPRESSION ARTICLE PAR LE POSTEUR
path('supp_article/<int:id_article>/', views.supprimer_article, name="supp_article"),

path('lik/', views.lik, name='lik'),
path('lik_my/', views.lik_my, name='lik_my'),

path('modifier_tof/<int:id_p>/', views.modifier_tof, name='modifier_tof'),
path("Deconexion/" ,  views.Deconexion , name="Deconexion")



# ------------GESTION DES LIKE


]