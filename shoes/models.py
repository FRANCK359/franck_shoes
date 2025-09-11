from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True)
    
    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
    
    def __str__(self):
        return self.name

class Shoe(models.Model):
    COLORS = [
        ('RED', 'Rouge'),
        ('BLK', 'Noir'),
        ('WHT', 'Blanc'),
        ('BLU', 'Bleu'),
        ('GRN', 'Vert'),
        ('YLW', 'Jaune'),
        ('GRY', 'Gris'),
        ('BRW', 'Marron'),
        ('PNK', 'Rose'),
        ('PRP', 'Violet'),
        ('ORG', 'Orange'),
        ('MUL', 'Multicolor'),
    ]
    
    name = models.CharField(max_length=200, verbose_name="Nom")
    slug = models.SlugField(unique=True)
    description = models.TextField(verbose_name="Description")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Catégorie")
    main_color = models.CharField(max_length=3, choices=COLORS, verbose_name="Couleur principale")
    available_colors = models.CharField(max_length=100, help_text="Séparer les couleurs par des virgules", verbose_name="Couleurs disponibles")
    min_size = models.IntegerField(
        validators=[MinValueValidator(35), MaxValueValidator(50)], 
        verbose_name="Pointure minimale"
    )
    max_size = models.IntegerField(
        validators=[MinValueValidator(35), MaxValueValidator(50)], 
        verbose_name="Pointure maximale"
    )
    stock = models.PositiveIntegerField(default=0, verbose_name="Stock")
    image = models.ImageField(upload_to='shoes/', verbose_name="Image")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    featured = models.BooleanField(default=False, verbose_name="En vedette")
    
    class Meta:
        verbose_name = "Chaussure"
        verbose_name_plural = "Chaussures"
        ordering = ['-created_at']
    
    def get_available_sizes(self):
        return list(range(self.min_size, self.max_size + 1))
    
    def get_colors_list(self):
        return [color.strip() for color in self.available_colors.split(',')]
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('product_detail', kwargs={'shoe_id': self.id})

class UserProfile(models.Model):
    CITIES = [
        ('DOUALA', 'Douala'),
        ('YAOUNDE', 'Yaoundé'),
        ('GAROUA', 'Garoua'),
        ('BAMENDA', 'Bamenda'),
        ('MAROUA', 'Maroua'),
        ('NKOUNGSAMBA', 'Nkongsamba'),
        ('BAFOUSSAM', 'Bafoussam'),
        ('NGAOUNDERE', 'Ngaoundéré'),
        ('BERTOUA', 'Bertoua'),
        ('LIMBE', 'Limbé'),
        ('EDEA', 'Edéa'),
        ('KUMBA', 'Kumba'),
        ('MBALMAYO', 'Mbalmayo'),
        ('DSCHANG', 'Dschang'),
        ('FOUMBAN', 'Foumban'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True, verbose_name="Numéro de téléphone")
    city = models.CharField(max_length=50, choices=CITIES, blank=True, verbose_name="Ville")
    address = models.TextField(blank=True, verbose_name="Adresse")
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Date de naissance")
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True, verbose_name="Photo de profil")
    
    class Meta:
        verbose_name = "Profil utilisateur"
        verbose_name_plural = "Profils utilisateurs"
    
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()

class Order(models.Model):
    PAYMENT_METHODS = [
        ('MTN', 'MTN Mobile Money'),
        ('ORANGE', 'Orange Money'),
        ('CASH', 'Paiement à la Livraison'),
        ('SHOP', 'Paiement en Boutique'),
    ]
    
    ORDER_STATUS = [
        ('PENDING', 'En attente'),
        ('CONFIRMED', 'Confirmée'),
        ('PROCESSING', 'En traitement'),
        ('SHIPPED', 'Expédiée'),
        ('DELIVERED', 'Livrée'),
        ('CANCELLED', 'Annulée'),
    ]
    
    customer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Client")
    items = models.ManyToManyField(Shoe, through='OrderItem', verbose_name="Articles")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant total")
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS, verbose_name="Méthode de paiement")
    status = models.CharField(max_length=10, choices=ORDER_STATUS, default='PENDING', verbose_name="Statut")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    shipping_address = models.TextField(verbose_name="Adresse de livraison")
    city = models.CharField(max_length=100, verbose_name="Ville")
    phone_number = models.CharField(max_length=20, verbose_name="Numéro de téléphone")
    notes = models.TextField(blank=True, verbose_name="Notes")
    
    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Commande #{self.id} - {self.customer.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Commande")
    shoe = models.ForeignKey(Shoe, on_delete=models.CASCADE, verbose_name="Chaussure")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantité")
    size = models.IntegerField(verbose_name="Pointure")
    color = models.CharField(max_length=50, verbose_name="Couleur")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix")
    
    class Meta:
        verbose_name = "Article de commande"
        verbose_name_plural = "Articles de commande"
    
    def __str__(self):
        return f"{self.quantity} x {self.shoe.name} (Taille: {self.size}, Couleur: {self.color})"
    
    def get_total(self):
        return self.quantity * self.price
    
from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    city = models.CharField(max_length=100, blank=True, null=True) 
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)  # ✅ approuvé par admin
    is_testimonial = models.BooleanField(default=False)  # ✅ champ pour avis

    def __str__(self):
        return f"{self.name} - {self.subject}"
