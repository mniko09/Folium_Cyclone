
================================================================================
🌀 CARTE INTERACTIVE - ANALYSE DES CYCLONES HISTORIQUES À LA RÉUNION
================================================================================
AUTEUR : RAFANOMEZANTSOA Maminiaina Nicolas
================================================================================
GUIDE D'INSTALLATION RAPIDE
================================================================================

PRÉREQUIS :
- Python 3.8 ou supérieur installé
- Connexion Internet active (pour OSMnx et API OSRM)

INSTALLATION DES DÉPENDANCES :
    pip install folium osmnx

EXÉCUTION DU PROGRAMME :
    python cyclones_reunion.py

RÉSULTAT :
    → Le fichier HTML sera généré automatiquement
    → Le navigateur s'ouvrira avec la carte interactive
    → En cas d'échec, ouvrir manuellement : cyclones_reunion_CARTE_COMPLETE_FINALE.html

UTILISATION :
    - Cliquer sur les trajectoires de cyclones pour voir les détails
    - Cliquer n'importe où sur la carte pour calculer un itinéraire d'évacuation
    - Utiliser le menu des couches (haut gauche) pour filtrer l'affichage

DURÉE PREMIÈRE EXÉCUTION : 30-60 secondes (téléchargement données OSM)

EN CAS DE PROBLÈME :
    - Vérifier la connexion Internet
    - Réinstaller : pip install --upgrade folium osmnx

================================================================================
TECHNOLOGIES UTILISÉES
================================================================================

LANGAGES ET FRAMEWORKS :
    - Python 3.x (langage principal)
    - JavaScript ES6 (interactivité côté client)
    - HTML5/CSS3 (interface utilisateur)

BIBLIOTHÈQUES PYTHON :
    - Folium (génération de cartes web interactives)
    - OSMnx (extraction de données géospatiales OpenStreetMap)

TECHNOLOGIES WEB :
    - Leaflet.js (moteur cartographique côté navigateur)
    - OSRM API (calcul d'itinéraires routiers optimaux)

RÔLE DU JAVASCRIPT :
    - Détection des clics utilisateur et capture des coordonnées GPS
    - Calcul automatique du lieu d'urgence le plus proche
    - Appel à l'API OSRM pour tracer l'itinéraire routier optimal
    - Affichage de la distance (km) et durée estimée (min)
    - Mode de secours (ligne droite) si l'API est indisponible

================================================================================
DESCRIPTION DU PROJET
================================================================================

    Application web interactive de visualisation et d'analyse des trajectoires
    cycloniques ayant impacté l'île de La Réunion entre 1980 et 2022.
    Intègre un système d'aide à l'évacuation en temps réel utilisant le routing
    routier OSRM.

FONCTIONNALITÉS PRINCIPALES :
     Visualisation de 8 cyclones historiques majeurs (catégories 2-4)
     Trajectoires animées avec données météorologiques détaillées
     Hôpitaux et refuges réels (données manuelles + OpenStreetMap)
    Calcul d'itinéraires d'évacuation routiers en temps réel (API OSRM)
    Détection automatique du lieu d'urgence le plus proche
    Organisation temporelle par décennies (1980-2020)
    Interface interactive avec clic sur carte
    Légende dynamique et contrôle des couches

SOURCES DES DONNÉES :
    - Cyclones : Météo-France Réunion (données historiques officielles)
    - Hôpitaux/Refuges : Saisie manuelle + OpenStreetMap
    - Réseau routier : OSRM (Open Source Routing Machine)
    - Fond de carte : OpenStreetMap

================================================================================
