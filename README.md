# Franck Shoes – Backend / Web App

## 📌 Description

**Franck Shoes** est une application web backend développée avec **Django** pour la gestion d’un site e-commerce de chaussures.  
Elle inclut la gestion des produits, des utilisateurs, des médias (Cloudinary) et utilise une base de données **SQLite** pour le développement.

---

## 🚀 Fonctionnalités principales

### 🛒 Gestion des Produits
- CRUD complet pour les chaussures
- Gestion des images via **Cloudinary**
- Catégorisation des produits

### 👤 Gestion Utilisateurs
- Inscription et connexion
- Profils utilisateurs

### 🌐 Frontend
- Pages HTML avec Django Templates
- Statics CSS / JS pour le style et le comportement
- Intégration des médias statiques et dynamiques

---

## 🛠️ Technologies utilisées

- Python 3.12
- Django 4.2
- SQLite (dev)
- Cloudinary (gestion des médias)
- Django Widget Tweaks
- HTML / CSS / JS pour templates
- Virtual environment (`venv`) pour isoler les dépendances

---

## 📁 Structure du projet

```text
franck_shoes/
├── static/          # Fichiers CSS, JS et images statiques
├── templates/       # Templates HTML
├── shoes/           # Application Django principale
├── venv/            # Virtual environment (ignoré)
├── db.sqlite3       # Base de données SQLite
├── manage.py        # Entrée principale Django
├── requirements.txt # Dépendances Python
├── runtime.txt      # Version Python pour déploiement
└── Procfile         # Pour déploiement Heroku / cloud
