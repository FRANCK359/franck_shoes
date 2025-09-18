// Gestion du thème
class ThemeManager {
  constructor() {
    this.themeToggle = document.getElementById('themeToggle');
    this.themeIcon = this.themeToggle.querySelector('i');
    this.init();
  }
  
  init() {
    // Appliquer le thème enregistré
    this.applySavedTheme();
    
    // Ajouter l'écouteur d'événements
    this.themeToggle.addEventListener('click', () => this.toggleTheme());
  }
  
  applySavedTheme() {
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    // Appliquer le thème sauvegardé ou le thème système
    if (savedTheme === 'light' || (!savedTheme && !prefersDark)) {
      this.enableLightTheme();
    } else {
      this.enableDarkTheme();
    }
  }
  
  toggleTheme() {
    if (document.body.classList.contains('light-theme')) {
      this.enableDarkTheme();
    } else {
      this.enableLightTheme();
    }
  }
  
  enableLightTheme() {
    document.body.classList.add('light-theme');
    this.themeIcon.classList.replace('fa-moon', 'fa-sun');
    localStorage.setItem('theme', 'light');
  }
  
  enableDarkTheme() {
    document.body.classList.remove('light-theme');
    this.themeIcon.classList.replace('fa-sun', 'fa-moon');
    localStorage.setItem('theme', 'dark');
  }
}

// Gestion de la navbar
class NavbarManager {
  constructor() {
    this.navbar = document.querySelector('.navbar');
    this.init();
  }
  
  init() {
    // Vérifier la position au chargement
    this.checkScrollPosition();
    
    // Ajouter l'écouteur d'événements de défilement
    window.addEventListener('scroll', () => this.checkScrollPosition());
  }
  
  checkScrollPosition() {
    if (window.scrollY > 50) {
      this.navbar.classList.add('scrolled');
    } else {
      this.navbar.classList.remove('scrolled');
    }
  }
}

// Initialisation lorsque le DOM est chargé
document.addEventListener('DOMContentLoaded', function() {
  // Vérifier si les éléments nécessaires existent avant d'initialiser
  if (document.getElementById('themeToggle')) {
    new ThemeManager();
  }
  
  if (document.querySelector('.navbar')) {
    new NavbarManager();
  }
  
  // Gestion des alertes
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(alert => {
    setTimeout(() => {
      const bsAlert = new bootstrap.Alert(alert);
      bsAlert.close();
    }, 5000);
  });
});

// Gestion des préférences de réduction de mouvement
if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  document.documentElement.style.setProperty('--transition', 'none');
}