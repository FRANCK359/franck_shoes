from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings
from django.core.paginator import Paginator
from .models import Shoe, Category, Order, OrderItem, UserProfile, ContactMessage
from .forms import OrderForm, ContactForm, UserRegistrationForm, UserProfileForm
from .cart import Cart
import json

# --- Dictionnaire des frais d'expédition par ville ---
CITY_SHIPPING_COSTS = {
    "Douala": 2000,
    "Yaoundé": 2500,
    "Bafoussam": 3000,
    "Garoua": 4000,
    "Maroua": 4500,
    "Autres": 5000,  # valeur par défaut
}

def index(request):
    featured_shoes = Shoe.objects.filter(featured=True)[:8]
    categories = Category.objects.all()
    messages_clients = ContactMessage.objects.filter(approved=True).order_by('-created_at')[:3]
    
    return render(request, 'index.html', {
        'featured_shoes': featured_shoes,
        'categories': categories,
        'messages_clients': messages_clients
    })

def product_list(request):
    category_id = request.GET.get('category')
    search_query = request.GET.get('q')
    
    shoes = Shoe.objects.all()
    
    if category_id:
        shoes = shoes.filter(category_id=category_id)
    
    if search_query:
        shoes = shoes.filter(name__icontains=search_query)
    
    paginator = Paginator(shoes, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    return render(request, 'product_list.html', {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': category_id,
        'search_query': search_query or ''
    })

def product_detail(request, shoe_id):
    shoe = get_object_or_404(Shoe, id=shoe_id)
    images = shoe.shoe_images.all()  # ✅ images secondaires
    related_shoes = Shoe.objects.filter(category=shoe.category).exclude(id=shoe.id)[:4]
    
    return render(request, 'product_detail.html', {
        'shoe': shoe,
        'images': images,
        'related_shoes': related_shoes
    })


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart.html', {'cart': cart})

@require_POST
def cart_add(request, shoe_id):
    cart = Cart(request)
    shoe = get_object_or_404(Shoe, id=shoe_id)
    
    data = json.loads(request.body)
    size = data.get('size')
    color = data.get('color')
    quantity = int(data.get('quantity', 1))
    
    cart.add(shoe, quantity, size, color)
    
    return JsonResponse({'success': True, 'cart_count': cart.__len__()})

@require_POST
def cart_remove(request, shoe_id):
    cart = Cart(request)
    shoe = get_object_or_404(Shoe, id=shoe_id)
    
    data = json.loads(request.body)
    size = data.get('size')
    color = data.get('color')
    
    cart.remove(shoe, size, color)
    
    return JsonResponse({'success': True, 'cart_count': cart.__len__()})

@require_POST
def cart_update(request, shoe_id):
    cart = Cart(request)
    shoe = get_object_or_404(Shoe, id=shoe_id)
    
    data = json.loads(request.body)
    size = data.get('size')
    color = data.get('color')
    quantity = int(data.get('quantity', 1))
    
    cart.update(shoe, quantity, size, color)
    
    return JsonResponse({'success': True})

@login_required
def checkout(request):
    cart = Cart(request)
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = request.user

            # ✅ Frais d'expédition selon la ville
            city = form.cleaned_data.get('city', 'Autres')
            shipping_cost = CITY_SHIPPING_COSTS.get(city, CITY_SHIPPING_COSTS["Autres"])

            order.total_amount = cart.get_total_price() + shipping_cost
            order.shipping_cost = shipping_cost  # il faut que ton modèle Order ait ce champ
            order.save()
            
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    shoe=item['shoe'],
                    quantity=item['quantity'],
                    size=item['size'],
                    color=item['color'],
                    price=item['price']
                )
            
            cart.clear()
            
            messages.success(request, f'Votre commande #{order.id} a été passée avec succès!')
            return render(request, 'order_confirmation.html', {'order': order})
    else:
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'phone_number': request.user.userprofile.phone_number if hasattr(request.user, 'userprofile') else '',
                'city': request.user.userprofile.city if hasattr(request.user, 'userprofile') else '',
            }
        form = OrderForm(initial=initial_data)
    
    return render(request, 'checkout.html', {'cart': cart, 'form': form})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save(commit=False)
            contact_message.approved = False
            contact_message.save()
            messages.success(request, 'Votre message a été envoyé avec succès! Il sera publié après validation.')
            return redirect('contact')
    else:
        form = ContactForm()
    
    testimonials = ContactMessage.objects.filter(approved=True, is_testimonial=True).order_by('-created_at')[:5]

    return render(request, 'contact.html', {'form': form, 'testimonials': testimonials})

def is_vendor(user):
    return user.groups.filter(name='Vendor').exists() or user.is_superuser

@user_passes_test(is_vendor)
@login_required
def vendor_dashboard(request):
    orders = Order.objects.all().order_by('-created_at')[:10]
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='PENDING').count()
    total_revenue = sum(order.total_amount for order in Order.objects.filter(status='DELIVERED'))
    
    return render(request, 'admin_dashboard.html', {
        'orders': orders,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'total_revenue': total_revenue
    })

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.save()

            user_profile, created = UserProfile.objects.get_or_create(user=user)
            user_profile.phone_number = form.cleaned_data.get("phone_number", "")
            user_profile.city = form.cleaned_data.get("city", "")
            user_profile.save()

            login(request, user)
            messages.success(request, f'Inscription réussie ! Bienvenue, {user.username} !')
            return redirect('index')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenue {username}!')
                return redirect('index')
        else:
            messages.error(request, 'Identifiants invalides.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'registration/login.html', {'form': form})

@login_required
def profile(request):
    if not hasattr(request.user, 'userprofile'):
        UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil mis à jour avec succès!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user.userprofile)
    
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    
    return render(request, 'registration/profile.html', {
        'form': form,
        'orders': orders
    })

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

def share_product(request, shoe_id):
    shoe = get_object_or_404(Shoe, id=shoe_id)
    platform = request.GET.get('platform', '')
    
    share_urls = {
        'facebook': f'https://www.facebook.com/sharer/sharer.php?u={request.build_absolute_uri(shoe.get_absolute_url())}',
        'whatsapp': f'https://api.whatsapp.com/send?text=Découvrez cette chaussure: {request.build_absolute_uri(shoe.get_absolute_url())}',
        'twitter': f'https://twitter.com/intent/tweet?text=Découvrez cette chaussure&url={request.build_absolute_uri(shoe.get_absolute_url())}',
    }
    
    if platform in share_urls:
        return redirect(share_urls[platform])
    
    return redirect(shoe.get_absolute_url())

def search(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    color = request.GET.get('color', '')
    
    shoes = Shoe.objects.all()
    
    if query:
        shoes = shoes.filter(name__icontains=query)
    
    if category_id:
        shoes = shoes.filter(category_id=category_id)
    
    if min_price:
        shoes = shoes.filter(price__gte=min_price)
    
    if max_price:
        shoes = shoes.filter(price__lte=max_price)
    
    if color:
        shoes = shoes.filter(main_color=color)
    
    categories = Category.objects.all()
    
    return render(request, 'search.html', {
        'shoes': shoes,
        'categories': categories,
        'query': query,
        'selected_category': category_id,
        'min_price': min_price,
        'max_price': max_price,
        'selected_color': color
    })

@login_required
def user_logout(request):
    logout(request)
    messages.info(request, "Vous êtes déconnecté(e) avec succès.")
    return redirect('index')

def about(request):
    return render(request, 'about.html')

def terms(request):
    return render(request, 'terms.html')
from django.http import JsonResponse

def set_cart_city(request):
    """
    Met à jour la ville sélectionnée dans la session pour calculer les frais de livraison
    """
    if request.method == "POST":
        city = request.POST.get("city")
        if city:
            request.session['ville'] = city
            return JsonResponse({'success': True, 'city': city})
    return JsonResponse({'success': False})
