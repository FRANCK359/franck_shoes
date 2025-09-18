from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Order, ContactMessage

# ==========================
# Formulaire d'inscription
# ==========================
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=20, required=False)
    city = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre ville'
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'phone_number', 'city']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            # Crée le profil utilisateur
            UserProfile.objects.create(
                user=user,
                phone_number=self.cleaned_data.get('phone_number', ''),
                city=self.cleaned_data.get('city', '')
            )
        
        return user

# ==========================
# Formulaire de profil utilisateur
# ==========================
class UserProfileForm(forms.ModelForm):
    city = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre ville'
        })
    )

    class Meta:
        model = UserProfile
        fields = ['phone_number', 'city', 'address', 'date_of_birth', 'profile_picture']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

# ==========================
# Formulaire de commande
# ==========================
class OrderForm(forms.ModelForm):
    city = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre ville'
        })
    )
    
    class Meta:
        model = Order
        fields = [
            'shipping_address', 
            'city', 
            'phone_number', 
            'payment_method', 
            'notes',
            'payment_confirmation_message',
        ]
        widgets = {
            'shipping_address': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Votre adresse complète',
                'class': 'form-control'
            }),
            'notes': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Notes supplémentaires pour la livraison',
                'class': 'form-control'
            }),
            'payment_confirmation_message': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Copiez ici le message reçu après paiement MTN ou Orange',
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Appliquer la classe Bootstrap à tous les champs
        for field in self.fields:
            if 'class' not in self.fields[field].widget.attrs:
                self.fields[field].widget.attrs.update({'class': 'form-control'})

# ==========================
# Formulaire de contact / témoignage
# ==========================
class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'city', 'subject', 'message', 'is_testimonial']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre nom'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre email'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre ville'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sujet du message'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Écrivez votre message ici...',
                'rows': 5
            }),
            'is_testimonial': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
