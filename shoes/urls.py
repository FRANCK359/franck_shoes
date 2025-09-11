from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('boutique/', views.product_list, name='product_list'),
    path('produit/<int:shoe_id>/', views.product_detail, name='product_detail'),
    path('panier/', views.cart_detail, name='cart_detail'),
    path('panier/ajouter/<int:shoe_id>/', views.cart_add, name='cart_add'),
    path('panier/supprimer/<int:shoe_id>/', views.cart_remove, name='cart_remove'),
    path('panier/mettre-a-jour/<int:shoe_id>/', views.cart_update, name='cart_update'),
    path('commander/', views.checkout, name='checkout'),
    path('contact/', views.contact, name='contact'),
    path('dashboard-vendeur/', views.vendor_dashboard, name='vendor_dashboard'),
    path('recherche/', views.search, name='search'),
    path('a-propos/', views.about, name='about'),
    path('conditions-generales/', views.terms, name='terms'),
    path('partager/<int:shoe_id>/', views.share_product, name='share_product'),
    
    # URLs d'authentification
    path('compte/inscription/', views.register, name='register'),
    path('compte/connexion/', views.user_login, name='login'),
    path('compte/deconnexion/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('compte/profil/', views.profile, name='profile'),
    path('compte/commande/<int:order_id>/', views.order_detail, name='order_detail'),
    
    # URLs de réinitialisation de mot de passe
    path('compte/reinitialisation-mot-de-passe/', 
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset.html',
             email_template_name='registration/password_reset_email.html',
             subject_template_name='registration/password_reset_subject.txt',
             success_url='/compte/reinitialisation-mot-de-passe/envoye/'
         ), 
         name='password_reset'),
    path('compte/reinitialisation-mot-de-passe/envoye/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
         ), 
         name='password_reset_done'),
    path('compte/reinitialisation-mot-de-passe/confirmation/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html',
             success_url='/compte/reinitialisation-mot-de-passe/complete/'
         ), 
         name='password_reset_confirm'),
    path('compte/reinitialisation-mot-de-passe/complete/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ), 
         name='password_reset_complete'),

    path(
        'compte/reinitialisation-mot-de-passe/',
        auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset.html',
            email_template_name='registration/password_reset_email.html',
            subject_template_name='registration/password_reset_subject.txt',
            success_url='/compte/reinitialisation-mot-de-passe/envoye/'
        ),
        name='password_reset'
    ),
    path(
        'compte/reinitialisation-mot-de-passe/envoye/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    path(
        'compte/reinitialisation-mot-de-passe/confirmation/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html',
            success_url='/compte/reinitialisation-mot-de-passe/complete/'
        ),
        name='password_reset_confirm'
    ),
    path(
        'compte/reinitialisation-mot-de-passe/complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
]