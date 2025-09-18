from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django import forms
from .models import Category, Shoe, Order, OrderItem, UserProfile, ContactMessage

# --- Formulaire personnalisé pour Shoe ---
class ShoeAdminForm(forms.ModelForm):
    class Meta:
        model = Shoe
        fields = '__all__'
        widgets = {
            'available_colors': forms.TextInput(attrs={'placeholder': 'Rouge, Noir, Blanc, Bleu...'}),
        }

# --- Admin pour Category ---
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

# --- Inline pour OrderItem ---
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('shoe', 'quantity', 'size', 'color', 'price')
    can_delete = False

# --- Admin pour Order ---
# --- Admin pour Order ---
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'customer',
        'total_amount',
        'payment_method',
        'status',
        'created_at',
        'city',
        'order_links'
    )
    list_filter = ('status', 'payment_method', 'city', 'created_at')
    search_fields = ('customer__username', 'phone_number', 'id')
    inlines = [OrderItemInline]
    readonly_fields = ('created_at', 'updated_at')
    actions = [
        'mark_as_confirmed',
        'mark_as_processing',
        'mark_as_shipped',
        'mark_as_delivered',
        'mark_as_cancelled'
    ]

    def order_links(self, obj):
        # Génère l'URL admin de manière dynamique, robuste
        url = reverse(f'admin:{obj._meta.app_label}_{obj._meta.model_name}_change', args=[obj.id])
        return format_html(
            '<a class="button" href="{}" style="margin-right:5px;">Voir</a>'
            '<a class="button" href="{}">Modifier</a>',
            url,
            url
        )
    order_links.short_description = 'Actions'

    # --- Actions personnalisées ---
    def mark_as_confirmed(self, request, queryset):
        updated = queryset.update(status='CONFIRMED')
        self.message_user(request, f"{updated} commande(s) ont été confirmées.")
    mark_as_confirmed.short_description = "Marquer comme confirmé"

    def mark_as_processing(self, request, queryset):
        updated = queryset.update(status='PROCESSING')
        self.message_user(request, f"{updated} commande(s) sont en traitement.")
    mark_as_processing.short_description = "Marquer comme en traitement"

    def mark_as_shipped(self, request, queryset):
        updated = queryset.update(status='SHIPPED')
        self.message_user(request, f"{updated} commande(s) ont été expédiées.")
    mark_as_shipped.short_description = "Marquer comme expédié"

    def mark_as_delivered(self, request, queryset):
        updated = queryset.update(status='DELIVERED')
        self.message_user(request, f"{updated} commande(s) ont été livrées.")
    mark_as_delivered.short_description = "Marquer comme livré"

    def mark_as_cancelled(self, request, queryset):
        updated = queryset.update(status='CANCELLED')
        self.message_user(request, f"{updated} commande(s) ont été annulées.")
    mark_as_cancelled.short_description = "Marquer comme annulé"

# --- Admin pour Shoe ---
@admin.register(Shoe)
class ShoeAdmin(admin.ModelAdmin):
    form = ShoeAdminForm
    list_display = ('name', 'category', 'price', 'main_color', 'stock', 'featured', 'image_preview')
    list_filter = ('category', 'main_color', 'featured', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('price', 'stock', 'featured')
    readonly_fields = ('created_at', 'updated_at', 'image_preview')
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description', 'category', 'price')
        }),
        ('Détails', {
            'fields': ('main_color', 'available_colors', 'min_size', 'max_size', 'stock', 'image', 'image_preview')
        }),
        ('Options', {
            'fields': ('featured',)
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
        return "Aucune image"
    image_preview.short_description = 'Aperçu'

# --- Admin pour UserProfile ---
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'city')
    list_filter = ('city',)
    search_fields = ('user__username', 'phone_number')

# --- Admin pour ContactMessage ---
@admin.register(ContactMessage)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'approved')
    list_filter = ('approved', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    list_editable = ('approved',)  # Approuver directement depuis la liste
