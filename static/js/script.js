// Script principal pour Franck'K Shoes CM

document.addEventListener('DOMContentLoaded', function() {
    // Initialisation des tooltips Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialisation des popovers Bootstrap
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    const popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Gestion des messages flash automatiques
    const autoDismissAlerts = document.querySelectorAll('.alert-dismissible[data-auto-dismiss]');
    autoDismissAlerts.forEach(alert => {
        const delay = parseInt(alert.getAttribute('data-auto-dismiss')) || 5000;
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, delay);
    });

    // Fonction pour obtenir le token CSRF
    window.getCookie = function(name) {
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
    };

    // Fonction pour afficher des notifications toast
    window.showToast = function(message, type = 'info') {
        const toastContainer = document.getElementById('toast-container') || createToastContainer();
        
        const toastId = 'toast-' + Date.now();
        const toastHtml = `
            <div id="${toastId}" class="toast align-items-center text-white bg-${type} border-0" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="d-flex">
                    <div class="toast-body">
                        ${message}
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
            </div>
        `;
        
        toastContainer.insertAdjacentHTML('beforeend', toastHtml);
        
        const toastElement = document.getElementById(toastId);
        const toast = new bootstrap.Toast(toastElement, {
            autohide: true,
            delay: 5000
        });
        toast.show();
        
        // Nettoyer après la fermeture
        toastElement.addEventListener('hidden.bs.toast', function () {
            toastElement.remove();
        });
    };

    function createToastContainer() {
        const container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container position-fixed top-0 end-0 p-3';
        container.style.zIndex = '9999';
        document.body.appendChild(container);
        return container;
    }

    // Fonction pour afficher une alerte
    window.showAlert = function(message, type = 'info', position = 'fixed') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        
        if (position === 'fixed') {
            alertDiv.style.position = 'fixed';
            alertDiv.style.top = '20px';
            alertDiv.style.right = '20px';
            alertDiv.style.zIndex = '9999';
            alertDiv.style.minWidth = '300px';
        }
        
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        
        document.body.appendChild(alertDiv);
        
        // Supprimer l'alerte après 5 secondes
        setTimeout(() => {
            if (alertDiv.parentNode) {
                const bsAlert = new bootstrap.Alert(alertDiv);
                bsAlert.close();
            }
        }, 5000);
        
        // Nettoyer après la fermeture
        alertDiv.addEventListener('closed.bs.alert', function () {
            alertDiv.remove();
        });
    };

    // Gestion du compteur de panier
    function updateCartCount(count) {
        document.querySelectorAll('.cart-count').forEach(span => {
            span.textContent = count;
            span.classList.add('pulse');
            setTimeout(() => span.classList.remove('pulse'), 500);
        });
    }

    // Animation de pulse pour le compteur de panier
    const style = document.createElement('style');
    style.textContent = `
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.2); }
            100% { transform: scale(1); }
        }
        .pulse {
            animation: pulse 0.5s ease;
        }
    `;
    document.head.appendChild(style);

    // Gestion des formulaires avec validation
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Fonction pour ajouter au panier
    window.addToCart = function(shoeId, size, color, quantity = 1) {
        fetch(`/panier/ajouter/${shoeId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
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
                updateCartCount(data.cart_count);
                showToast('Produit ajouté au panier !', 'success');
            } else {
                showToast('Erreur lors de l\'ajout au panier', 'danger');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('Erreur de connexion', 'danger');
        });
    };

    // Fonction pour mettre à jour le panier
    window.updateCart = function(shoeId, size, color, quantity) {
        fetch(`/panier/mettre-a-jour/${shoeId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
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
                location.reload();
            } else {
                showToast('Erreur lors de la mise à jour', 'danger');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('Erreur de connexion', 'danger');
        });
    };

    // Fonction pour supprimer du panier
    window.removeFromCart = function(shoeId, size, color) {
        if (!confirm('Êtes-vous sûr de vouloir supprimer ce produit du panier ?')) {
            return;
        }
        
        fetch(`/panier/supprimer/${shoeId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                size: size,
                color: color
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateCartCount(data.cart_count);
                showToast('Produit supprimé du panier', 'success');
                // Recharger après un court délai pour voir la notification
                setTimeout(() => location.reload(), 1000);
            } else {
                showToast('Erreur lors de la suppression', 'danger');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('Erreur de connexion', 'danger');
        });
    };

    // Gestion des images de produits - lazy loading
    const productImages = document.querySelectorAll('img[data-src]');
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });

        productImages.forEach(img => {
            imageObserver.observe(img);
        });
    } else {
        // Fallback pour les navigateurs sans IntersectionObserver
        productImages.forEach(img => {
            img.src = img.dataset.src;
        });
    }

    // Animation au scroll
    const animateOnScroll = function() {
        const elements = document.querySelectorAll('.fade-in, .slide-in-left, .slide-in-right');
        
        elements.forEach(element => {
            const elementTop = element.getBoundingClientRect().top;
            const elementBottom = element.getBoundingClientRect().bottom;
            const isVisible = (elementTop < window.innerHeight - 100) && (elementBottom > 0);
            
            if (isVisible) {
                element.style.visibility = 'visible';
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
            }
        });
    };

    // Initialiser les éléments animés
    const animatedElements = document.querySelectorAll('.fade-in, .slide-in-left, .slide-in-right');
    animatedElements.forEach(element => {
        element.style.visibility = 'hidden';
        element.style.opacity = '0';
        element.style.transition = 'all 0.6s ease-out';
        
        if (element.classList.contains('slide-in-left')) {
            element.style.transform = 'translateX(-30px)';
        } else if (element.classList.contains('slide-in-right')) {
            element.style.transform = 'translateX(30px)';
        } else {
            element.style.transform = 'translateY(20px)';
        }
    });

    // Démarrer l'animation au scroll
    window.addEventListener('scroll', animateOnScroll);
    // Démarrer une fois au chargement
    setTimeout(animateOnScroll, 100);

    // Gestion de la recherche en temps réel
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                this.form.submit();
            }, 500);
        });
    }

    // Gestion des filtres de prix
    const priceInputs = document.querySelectorAll('input[name="min_price"], input[name="max_price"]');
    priceInputs.forEach(input => {
        input.addEventListener('change', function() {
            this.form.submit();
        });
    });

    // Smooth scrolling pour les ancres
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Gestion des modales de confirmation
    window.showConfirmationModal = function(title, message, confirmCallback, cancelCallback) {
        // Créer ou réutiliser une modale de confirmation
        let modal = document.getElementById('confirmationModal');
        
        if (!modal) {
            modal = document.createElement('div');
            modal.id = 'confirmationModal';
            modal.className = 'modal fade';
            modal.innerHTML = `
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title"></h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body"></div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Annuler</button>
                            <button type="button" class="btn btn-primary" id="confirmButton">Confirmer</button>
                        </div>
                    </div>
                </div>
            `;
            document.body.appendChild(modal);
        }

        modal.querySelector('.modal-title').textContent = title;
        modal.querySelector('.modal-body').textContent = message;

        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();

        // Gérer les événements
        const confirmButton = modal.querySelector('#confirmButton');
        const originalOnclick = confirmButton.onclick;
        
        confirmButton.onclick = function() {
            if (confirmCallback) confirmCallback();
            bsModal.hide();
        };

        modal.addEventListener('hidden.bs.modal', function () {
            if (cancelCallback) cancelCallback();
            confirmButton.onclick = originalOnclick;
        });
    };

    console.log('Franck\'K Shoes CM - Script initialisé');
});

// Fonction pour formater les prix
function formatPrice(price) {
    return new Intl.NumberFormat('fr-CM', {
        style: 'currency',
        currency: 'XAF'
    }).format(price).replace('XAF', 'FCFA');
}

// Fonction pour le débogage
function debug(message, data = null) {
    if (console && console.log) {
        console.log(`[DEBUG] ${message}`, data || '');
    }
}

// Export des fonctions pour une utilisation globale
window.FranckShoes = {
    showToast,
    showAlert,
    addToCart,
    updateCart,
    removeFromCart,
    formatPrice,
    debug
};