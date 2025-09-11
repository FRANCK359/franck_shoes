from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Order

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=20, required=False)
    city = forms.ChoiceField(choices=UserProfile.CITIES, required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'phone_number', 'city']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            
            # ✅ Crée le profile explicitement
            UserProfile.objects.create(
                user=user,
                phone_number=self.cleaned_data.get('phone_number', ''),
                city=self.cleaned_data.get('city', '')
            )
        
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'city', 'address', 'date_of_birth', 'profile_picture']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class OrderForm(forms.ModelForm):
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
    
    city = forms.ChoiceField(choices=CITIES, required=True)
    
    class Meta:
        model = Order
        fields = ['shipping_address', 'city', 'phone_number', 'payment_method', 'notes']
        widgets = {
            'shipping_address': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Votre adresse complète'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Notes supplémentaires pour la livraison'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


from .models import ContactMessage

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