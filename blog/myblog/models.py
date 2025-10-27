from django.db import models

# Create your models here.



class utilisateur(models.Model):

    nom_prenom=models.CharField(max_length=255)
    username=models.CharField(max_length=255)
    sexe=models.CharField(max_length=255)
    photo_user=models.ImageField(upload_to="image/", default= "image/default-avatar-icon-of-social-media-user-vector.jpg")

    mail=models.CharField(max_length=255)
    mdp=models.CharField(max_length=255)
  



class articles(models.Model):
    autheur=models.ForeignKey(utilisateur, on_delete=models.CASCADE,related_name="author")
    titre=models.CharField(max_length=255)
    photo=models.ImageField(upload_to="image/")

    details=models.CharField(max_length=255)
 
    date_pub=models.DateTimeField(auto_now_add=True)




class commentaires(models.Model):
    arti=models.ForeignKey(articles, on_delete=models.CASCADE,related_name="c")
    user_cmt=models.ForeignKey(utilisateur, on_delete=models.CASCADE,related_name="user_cmt")
    commantaire=models.CharField(max_length=255)
 
    date_cmt=models.DateTimeField(auto_now_add=True)


class like (models.Model)  :  
    article=models.ForeignKey(articles, on_delete=models.CASCADE,related_name="likes")
    likeur=models.ForeignKey(utilisateur, on_delete=models.CASCADE,related_name="likeur")

   




