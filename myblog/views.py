from django.shortcuts import render , redirect, get_object_or_404

from django.contrib.auth.hashers import make_password , check_password


from django.contrib import messages


# Create your views here.
from.models import utilisateur,articles,commentaires,like
from django.http import HttpResponse, JsonResponse

from django.views.decorators.cache import never_cache


@never_cache
def conexion(request):

    return render(request,"conexion.html")











# -------------------ROUTE POUR GERER LINSCRIPTION

@never_cache
def inscription(request):

    if request.method=="POST":
        nom_prenom=request.POST.get("nom",'').strip()
        username=request.POST.get("username",'').strip()
        sexe=request.POST.get("sexe",'').strip()
        mail=request.POST.get("mail",'').strip()
        mdp=request.POST.get("mdp",'').strip()

        mdp_hash= make_password(mdp)

        if utilisateur.objects.filter(username=username).exists() :
         
              return render(request,'inscriptions.html', {"messages0":True , 'username':username})
        else: 


         user=utilisateur.objects.create(nom_prenom = nom_prenom,username=username,mail=mail, sexe=sexe,mdp=mdp_hash)

         request.session['user_id']=user.id
         request.session.set_expiry(0)

        return redirect("acceuils")


    return render(request, "inscriptions.html")






# -------------------ROUTE POUR GERER LA CONEXION
@never_cache
def conexion(request):
       if request.method=="POST":
           nom=request.POST.get("nom", '' ).strip()
           mdpe=request.POST.get("mdp",'' ).strip()

        

           user=utilisateur.objects.filter(username=nom).first()

           if user:
                if check_password(mdpe,user.mdp):
                             request.session['user_id']=user.id
                             request.session.set_expiry(0)
                             return redirect("acceuils")
                
                else:
                     
                     return render (request,"conexion.html" , {"message1":True})
                

           else:   
            return render (request,"conexion.html", {"message2":True})    
                

                    

       return render(request, "conexion.html")


# ----------------------------------

@never_cache
def publier(request):
    user_id=request.session.get("user_id")
    user= utilisateur.objects.get(id=user_id)




    if request.method=="POST":
     
         
         title=request.POST.get('titre')
         tof=request.FILES.get('photo')
         detail=request.POST.get('details')
         title=request.POST.get('titre')

         articles.objects.create(titre=title,photo=tof,details=detail, autheur=user)

         user=articles.objects.all().order_by("-id")
       
         messages.success(request, " ✅ Votre article a été ajouté avec succès.")
         return redirect('acceuils')
    
   

    return render(request, 'menus_publier.html')





    # -------------------ROUTE POUR GERER LACCEUIL AVEC AFFICHAGE DE CHAQUE ARTICLE


@never_cache
def acceuils(request):
    if "user_id" not in request.session:
        return redirect('conexion')
    else:
        user = articles.objects.all().order_by("-id")

        user_id = request.session.get("user_id")

    if request.method == 'POST':
        btne = request.POST.get('btn')
        userr = utilisateur.objects.get(id=user_id)
        publication = articles.objects.get(id=btne)

        if like.objects.filter(article=publication, likeur=userr).exists():
            like.objects.filter(article=publication, likeur=userr).delete()
            liked = False
        else:
            like.objects.create(article=publication, likeur=userr)
            liked = True

        # Si c'est fetch(), renvoyer JSON correct
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            count = like.objects.filter(article=publication).count()
            return JsonResponse({'liked': liked, 'count': count})

    return render(request, "acceuils.html", {"user": user})
     

     
#  ------------------------------PAGE ARTICLE DETAILS ET commentaires    
     
@never_cache
def article(request,id_article):
     
     request.session["id_article"]=id_article  #id_article stocké en session

     if "user_id" not in request.session:
          return redirect('conexion')
     
     user_id=request.session.get("user_id")    # recuperation de lid en session 
    
     
     
     publication = articles.objects.get(id=id_article)   # recuperation de larticle de puis lid en url
     cmt = commentaires.objects.filter(arti=id_article).order_by("-id")  # recuperation des commentaire  qui ont en lien avec larticle
     
    
     # recuperation du nombre total de comentaire en fonction de l'article

     

     # -------------------------------------------
   

     if request.method=="POST":
          user_id=request.session.get("user_id")
          user=utilisateur.objects.get(id=user_id)
        
          
          commentairess=request.POST.get('commentaire')
          commentaires.objects.create(commantaire=commentairess , arti=publication ,  user_cmt=user)
          return redirect('article',id_article=id_article)
   
     
          


     return render (request,'article.html', {'u':publication ,"cmt":cmt,   "id": user_id,"id_article":id_article} )

     #----------------------LIKE ALINTERIEUR DE LARTICLE
def lik(request):
    id_article=request.session.get("id_article")  
    user_id = request.session.get("user_id")

    if request.method == 'POST':
        btne = request.POST.get('btn')
        userr = utilisateur.objects.get(id=user_id)
        publication = articles.objects.get(id=btne)

        if like.objects.filter(article=publication, likeur=userr).exists():
            like.objects.filter(article=publication, likeur=userr).delete()
            liked = False
        else:
            like.objects.create(article=publication, likeur=userr)
            liked = True

        # Si c'est fetch(), renvoyer JSON correct
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            count = like.objects.filter(article=publication).count()
            return JsonResponse({'liked': liked, 'count': count})
        
    return redirect('article',id_article=id_article)




     #----------------------LIKE ALINTERIEUR DE LARTICLE
def lik_my(request):
 
    user_id = request.session.get("user_id")

    if request.method == 'POST':
        btne = request.POST.get('btn')
        userr = utilisateur.objects.get(id=user_id)
        publication = articles.objects.get(id=btne)

        if like.objects.filter(article=publication, likeur=userr).exists():
            like.objects.filter(article=publication, likeur=userr).delete()
            liked = False
        else:
            like.objects.create(article=publication, likeur=userr)
            liked = True

        # Si c'est fetch(), renvoyer JSON correct
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            count = like.objects.filter(article=publication).count()
            return JsonResponse({'liked': liked, 'count': count})
        
    return redirect('myarticle')




#  ------------------------GESTION DES COMMENTAIRES--- 

#Suppression dun commentaire par le comentataire lui meme
def supprimer(request,id_cmt):
     id_article=request.session.get("id_article")  #rcuperation de lid de lartticle pour le faire passer dans le redirect 
     
     commentaires.objects.filter(id=id_cmt).delete()

     return redirect("article", id_article=id_article)




  
#modification dun commentaire par le comentataire lui meme
@never_cache
def modifier (request,id_cmt):
     id_article=request.session.get("id_article")
     
#CETTE PARTIE EST POUR RECEVOIR LE CMT POUR LA MODIFIER
     if request.method=="POST":
         commentairs=request.POST.get('commentaire')
      
         commentaires.objects.filter(id=id_cmt).update(commantaire=commentairs)

         return redirect("article", id_article=id_article)

#APRES AVOUR CLIQUER SUR MODIFIER VOILA LA PARTIE QUI SEXECUTE

     id_article=request.session.get("id_article")  #rcuperation de lid de lartticle pour le faire passer dans le redirect 
     cmt= commentaires.objects.get(id=id_cmt)
     messages.info(request,  cmt.commantaire )
     request.session["d"]=id_cmt

     return redirect("article", id_article=id_article)

 
 









#Route pour voir ses proppores article publier
@never_cache
def myarticle(request):
      
     user_id=request.session.get("user_id")  


     user=articles.objects.filter(autheur=user_id).order_by("-id")

     return render( request, "myarticles.html",{"user":user })




     
     
     
     
# -------------------ROUTE POUR GERER LE PROFILS DE TOUTS ceux qui POSTE 
@never_cache
def profils(request,id):
    user_id=request.session.get("user_id")
    user= utilisateur.objects.get(id=id)


    return render(request, 'profil.html',{"user":user  ,"myid":user_id})
     
# -------------------ROUTE POUR GERER LE PROFILS user
@never_cache
def profils_user(request):
    user_id=request.session.get("user_id")
    user= utilisateur.objects.get(id=user_id)


    return render(request, 'profil.html',{"user":user  ,"myid":user_id})




#------------------------ GESTION DES POST PAR LES POSTEURS SUPPRESSION ET MODIFICATION 
@never_cache
def supprimer_article(request,id_article):
     articles.objects.filter(id=id_article).delete()
     messages.info(request, " ✅Votre article a été supprimer avec succès")
     return redirect('myarticle')


def modifier_tof(request, id_p):
     user_id=request.session.get("user_id")
 
 
     user= utilisateur.objects.get(id=id_p)

# --------------------APRES AVOIR CLIQUER SUR MODIFIER
     if request.method=="POST":
          new_tofs=request.FILES.get('new_tof')

          p= utilisateur.objects.get(id=id_p)
          p.photo_user = new_tofs
          p.save()
          return redirect('profils', id=id_p)
#  ---------------------------------------------       
         

     return render(request, 'profil.html',{"user":user  ,"myid":user_id, 'pht':True})

     





#----------------------------- GESTION DES LIKES ET NO LIKE

@never_cache
def Deconexion(request):
     request.session.flush()

     return redirect ( 'conexion')