// Gestion du diaporama
class Slideshow {
  constructor() {
    this.currentSlide = 0;
    this.slides = document.querySelectorAll('.slide');
    this.indicators = document.querySelectorAll('.slide-indicator');
    this.slideCount = this.slides.length;
    this.interval = null;
    
    this.init();
  }
  
  init() {
    // Ajouter les écouteurs d'événements pour les indicateurs
    this.indicators.forEach((indicator, index) => {
      indicator.addEventListener('click', () => {
        this.showSlide(index);
        this.resetInterval();
      });
    });
    
    // Démarrer le diaporama automatique
    this.startSlideshow();
    
    // Pause au survol
    const slideshowContainer = document.querySelector('.slideshow-container');
    slideshowContainer.addEventListener('mouseenter', () => this.stopSlideshow());
    slideshowContainer.addEventListener('mouseleave', () => this.startSlideshow());
  }
  
  showSlide(n) {
    // Mettre à jour l'index courant
    this.currentSlide = n;
    
    // Mettre à jour les slides
    this.slides.forEach((slide, index) => {
      const isActive = index === n;
      slide.classList.toggle('active', isActive);
      slide.setAttribute('aria-hidden', !isActive);
    });
    
    // Mettre à jour les indicateurs
    this.indicators.forEach((indicator, index) => {
      indicator.classList.toggle('active', index === n);
      indicator.setAttribute('aria-current', index === n ? 'true' : 'false');
    });
  }
  
  nextSlide() {
    this.currentSlide = (this.currentSlide + 1) % this.slideCount;
    this.showSlide(this.currentSlide);
  }
  
  startSlideshow() {
    this.interval = setInterval(() => this.nextSlide(), 5000);
  }
  
  stopSlideshow() {
    if (this.interval) {
      clearInterval(this.interval);
      this.interval = null;
    }
  }
  
  resetInterval() {
    this.stopSlideshow();
    this.startSlideshow();
  }
}

// Gestion du panier
class CartManager {
  constructor() {
    this.addToCartButtons = document.querySelectorAll('.add-to-cart');
    this.init();
  }
  
  init() {
    this.addToCartButtons.forEach(button => {
      button.addEventListener('click', (e) => {
        e.preventDefault();
        const shoeId = button.getAttribute('data-shoe-id');
        this.addToCart(shoeId, 38, 'Noir', 1);
      });
    });
  }
  
  addToCart(shoeId, size, color, quantity) {
    fetch(`/panier/ajouter/${shoeId}/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': this.getCookie('csrftoken')
      },
      body: JSON.stringify({
        size: size,
        color: color,
        quantity: quantity
      })
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        this.updateCartCount(data.cart_count);
        this.showAlert('Produit ajouté au panier!', 'success');
      }
    })
    .catch(error => {
      console.error('Error:', error);
      this.showAlert('Erreur lors de l\'ajout au panier', 'danger');
    });
  }
  
  updateCartCount(count) {
    document.querySelectorAll('.cart-count').forEach(span => {
      span.textContent = count;
    });
  }
  
  getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  
  showAlert(message, type) {
    // Vérifier s'il existe déjà une alerte
    const existingAlert = document.querySelector('.alert.position-fixed');
    if (existingAlert) {
      existingAlert.remove();
    }
    
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.top = '20px';
    alertDiv.style.right = '20px';
    alertDiv.style.zIndex = '9999';
    alertDiv.innerHTML = `
      ${message}
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Fermer"></button>
    `;
    document.body.appendChild(alertDiv);
    
    // Supprimer l'alerte après 3 secondes
    setTimeout(() => {
      if (alertDiv.parentNode) {
        alertDiv.remove();
      }
    }, 3000);
  }
}

// Initialisation lorsque le DOM est chargé
document.addEventListener('DOMContentLoaded', function() {
  // Vérifier si les éléments nécessaires existent avant d'initialiser
  if (document.querySelector('.slideshow-container')) {
    new Slideshow();
  }
  
  if (document.querySelector('.add-to-cart')) {
    new CartManager();
  }
});