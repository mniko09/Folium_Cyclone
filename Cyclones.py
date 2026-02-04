"""
🌀 CARTE INTERACTIVE COMPLETE - CYCLONES LA REUNION

FONCTIONNALITES :
✅ 8 Cyclones historiques animes (1980-2022) donné meteo-france ajouter à la main, n'a pas pus avoir tous les données
✅ Hopitaux et refuges reels (OSMnx)
✅ J'ai fait appel à l'API OSRM pour tracer l'itinéraire routier optimal
✅ CLIC INTERACTIF : Trouver refuge le plus proche
✅ Marqueur vert + Ligne rouge + Distance
✅ Organisation par decennies (1980-2020)
✅ Legende interactive 
✅ Plugins(Fullscreen, MiniMap,)
 
 Prérequis 
 IL FAUT INSTALLER LA DEPENDENCE:
    pip install osmnx
 
DURÉE PREMIERE EXECUTION : 60-120 secondes (téléchargement données OSM)

Auteur: Maminiaina Nicolas
Date: 2025
"""

import folium
from folium import plugins
import osmnx as ox
import json
import webbrowser  # AJOUTE CETTE LIGNE
import os 


# ============================================================
# CONFIGURATION OSMNX
# ============================================================

ox.settings.use_cache = True
ox.settings.log_console = False


# ============================================================
# DONNEES CYCLONES HISTORIQUES COMPLETS
# ============================================================

cyclones_data = [
    {
        'nom': 'Cyclone Hyacinthe',
        'annee': 1980,
        'date': '15-27 janvier 1980',
        'categorie': 4,
        'vents_max': 220,
        'precipitations_max': 6083,
        'deces': 25,
        'trajectoire': [
            [-18.5, 58.0], [-19.0, 57.5], [-19.5, 57.0],
            [-20.0, 56.5], [-20.5, 56.0], [-21.0, 55.5],
            [-21.5, 55.0], [-22.0, 54.5]
        ],
        'couleur': "#718B00",
        'description': 'Record mondial de precipitations. Glissements de terrain majeurs.'
    },
    {
        'nom': 'Cyclone Firinga',
        'annee': 1989,
        'date': '26-29 janvier 1989',
        'categorie': 4,
        'vents_max': 216,
        'precipitations_max': 1500,
        'deces': 0,
        'trajectoire': [
            [-17.0, 60.0], [-17.5, 59.0], [-18.0, 58.0],
            [-19.0, 57.0], [-20.0, 56.0], [-21.0, 55.5],
            [-22.0, 55.0], [-23.0, 54.5]
        ],
        'couleur': "#DC8514",
        'description': 'Vents violents, destructions importantes dans ouest.'
    },
    {
        'nom': 'Cyclone Dina',
        'annee': 2002,
        'date': '20-22 janvier 2002',
        'categorie': 4,
        'vents_max': 230,
        'precipitations_max': 800,
        'deces': 0,
        'trajectoire': [
            [-16.0, 61.0], [-17.0, 60.0], [-18.0, 58.5],
            [-19.5, 57.0], [-20.5, 56.0], [-21.2, 55.3],
            [-22.0, 54.5], [-23.0, 53.5]
        ],
        'couleur': "#FF9900",
        'description': 'Rafales a 287 km/h au Maido. Coupures electricite generalisees.'
    },
    {
        'nom': 'Cyclone Gamede',
        'annee': 2007,
        'date': '24 fevrier - 1er mars 2007',
        'categorie': 4,
        'vents_max': 230,
        'precipitations_max': 5510,
        'deces': 2,
        'trajectoire': [
            [-16.5, 62.0], [-17.5, 60.5], [-18.5, 59.0],
            [-19.5, 57.5], [-20.5, 56.5], [-21.0, 55.8],
            [-21.5, 55.3], [-22.5, 54.5]
        ],
        'couleur': '#B22222',
        'description': 'Inondations majeures, glissements de terrain. Route du littoral coupee.'
    },
    {
        'nom': 'Cyclone Dumile',
        'annee': 2013,
        'date': '2-4 janvier 2013',
        'categorie': 2,
        'vents_max': 150,
        'precipitations_max': 600,
        'deces': 0,
        'trajectoire': [
            [-18.0, 59.0], [-19.0, 58.0], [-20.0, 57.0],
            [-21.0, 56.0], [-22.0, 55.0], [-23.0, 54.0]
        ],
        'couleur': '#FF6347',
        'description': 'Passage au large. Houle cyclonique importante.'
    },
    {
        'nom': 'Cyclone Fakir',
        'annee': 2018,
        'date': '23-24 avril 2018',
        'categorie': 3,
        'vents_max': 170,
        'precipitations_max': 400,
        'deces': 0,
        'trajectoire': [
            [-17.5, 60.0], [-18.5, 58.5], [-19.5, 57.5],
            [-20.5, 56.5], [-21.5, 55.5], [-22.5, 54.5]
        ],
        'couleur': '#FF7F50',
        'description': 'Passage rapide. Degats sur le reseau electrique.'
    },
    {
        'nom': 'Cyclone Batsirai',
        'annee': 2022,
        'date': '2-3 fevrier 2022',
        'categorie': 4,
        'vents_max': 220,
        'precipitations_max': 350,
        'deces': 0,
        'trajectoire': [
            [-17.0, 61.0], [-18.0, 59.5], [-19.0, 58.0],
            [-20.0, 57.0], [-21.0, 56.5], [-22.0, 56.0]
        ],
        'couleur': '#FFA07A',
        'description': 'Passage au large. Alerte orange levee rapidement.'
    },
    {
        'nom': 'Cyclone Belna',
        'annee': 2019,
        'date': '7-9 decembre 2019',
        'categorie': 3,
        'vents_max': 185,
        'precipitations_max': 300,
        'deces': 0,
        'trajectoire': [
            [-16.0, 62.0], [-17.0, 60.5], [-18.0, 59.0],
            [-19.0, 57.5], [-20.0, 56.5], [-21.0, 56.0]
        ],
        'couleur': '#FFB6C1',
        'description': 'Passage tres au large. Impact minimal.'
    }
]


# ============================================================
# LIEUX D'URGENCE (Hopitaux + Refuges)
# ============================================================

lieux_urgence = [
    {
        'nom': 'CHU Felix Guyon (Saint-Denis)',
        'coords': [-20.8855, 55.4478],
        'type': 'hopital',
        'capacite': '2000 pers',
        'description': 'Hopital principal nord'
    },
    {
        'nom': 'Hopital Saint-Pierre',
        'coords': [-21.3410, 55.4754],
        'type': 'hopital',
        'capacite': '1500 pers',
        'description': 'Hopital principal sud'
    },
    {
        'nom': 'Hopital Saint-Benoit',
        'coords': [-21.0389, 55.7171],
        'type': 'hopital',
        'capacite': '800 pers',
        'description': 'Hopital est'
    },
     {
        'nom': 'Hopital Saint-Gilles',
        'coords': [-21.0389, 55.7171],
        'type': 'hopital',
        'capacite': '800 pers',
        'description': 'Hopital ouest'
    },
     {
        'nom': 'Hopital Saint-Louis',
        'coords': [-21.28, 55.40],
        'type': 'hopital',
        'capacite': '800 pers',
        'description': 'Hopital est'
    },
     {
        'nom': 'Hopital OSM-CHU',
        'coords': [-21.0389, 55.7171],
        'type': 'hopital',
        'capacite': '800 pers',
        'description': 'Hopital est'
    },
    {
        'nom': 'Refuge Saint-Joseph',
        'coords': [-21.37, 55.60],
        'type': 'refuge',
        'capacite': '1000 pers',
        'description': 'Refuge Saint-Joseph'
    },
    {
        'nom': 'Refuge Saint-Philipe',
        'coords': [-21.35, 55.76],
        'type': 'refuge',
        'capacite': '1000 pers',
        'description': 'Refuge Saint-Philipe'
    },
    {
        'nom': 'Refuge Saint-Paul',
        'coords': [-21.0095, 55.2695],
        'type': 'refuge',
        'capacite': '1000 pers',
        'description': 'Refuge ouest'
    },
    {
        'nom': 'Refuge Le Port',
        'coords': [-20.9444, 55.2917],
        'type': 'refuge',
        'capacite': '600 pers',
        'description': 'Refuge nord-ouest'
    },
    {
        'nom': 'Refuge Sainte-Marie',
        'coords': [-20.8900, 55.5400],
        'type': 'refuge',
        'capacite': '500 pers',
        'description': 'Refuge nord-est'
    }
]


# ============================================================
# EXTRACTION des Lieux OSMNX
# ============================================================


def extraire_lieux_osmnx():
    """Telecharge lieux reels (hopitaux, ecoles)"""
    print("📍 Telechargement lieux OSM...")

    try:
        hopitaux = ox.features_from_place(
            "La Reunion, France",
            tags={'amenity': 'hospital'}
        )

        ecoles = ox.features_from_place(
            "La Reunion, France",
            tags={'amenity': 'school'}
        )

        print(f"   ✓ {len(hopitaux)} hopitaux, {len(ecoles)} ecoles")
        return hopitaux, ecoles
    except Exception as e:
        print(f"   ⚠️ Erreur lieux : {e}")
        return None, None


# ============================================================
# FONCTIONS UTILITAIRES
# ============================================================

def creer_popup_cyclone(cyclone):
    """Popup HTML pour cyclone"""
    html = f"""
    <div style="width: 300px; font-family: Arial;">
        <h3 style="color: {cyclone['couleur']};">🌀 {cyclone['nom']}</h3>
        <table style="width: 100%; font-size: 12px;">
            <tr><td><b>Date:</b></td><td>{cyclone['date']}</td></tr>
            <tr><td><b>Categorie:</b></td><td>{cyclone['categorie']} / 5</td></tr>
            <tr><td><b>Vents:</b></td><td>{cyclone['vents_max']} km/h</td></tr>
            <tr><td><b>Pluies:</b></td><td>{cyclone['precipitations_max']} mm</td></tr>
            <tr><td><b>Deces:</b></td><td>{cyclone['deces']}</td></tr>
        </table>
        <p style="margin-top: 10px; font-size: 11px; font-style: italic;">
            {cyclone['description']}
        </p>
    </div>
    """
    return folium.Popup(html, max_width=350)


def trouver_point_plus_proche(trajectoire):
    """Trouve point plus proche de La Reunion"""
    reunion = [-21.1151, 55.5364]
    distances = [(((p[0] - reunion[0])**2 + (p[1] - reunion[1])**2)**0.5) for p in trajectoire]
    return trajectoire[distances.index(min(distances))]


# ============================================================
# CREATION CARTE COMPLETE
# ============================================================

def creer_carte_complete_finale():
    """Cree carte avec TOUTES les fonctionnalites"""

    print("\n" + "="*70)
    print("🌀 CARTE INTERACTIVE COMPLETE - CYCLONES LA REUNION")
    print("="*70 + "\n")

    # Carte base
    carte = folium.Map(
        location=[-21.1151, 55.5364],
        zoom_start=10,
        tiles='OpenStreetMap',
        control_scale=True
    )


    groupe_1980 = folium.FeatureGroup(name='🌀 Annees 1980', show=True)
    groupe_1990_2000 = folium.FeatureGroup(name='🌀 Annees 1990-2000', show=True)
    groupe_2010 = folium.FeatureGroup(name='🌀 Annees 2010', show=True)
    groupe_2020 = folium.FeatureGroup(name='🌀 Annees 2020', show=True)

    for cyclone in cyclones_data:
        # Determiner groupe
        if cyclone['annee'] < 1990:
            groupe = groupe_1980
        elif cyclone['annee'] < 2010:
            groupe = groupe_1990_2000
        elif cyclone['annee'] < 2020:
            groupe = groupe_2010
        else:
            groupe = groupe_2020

        # Ligne animee
        plugins.AntPath(
            locations=cyclone['trajectoire'],
            color=cyclone['couleur'],
            weight=5,
            opacity=0.8,
            delay=1000,
            dash_array=[15, 10],
            pulse_color='white',
            popup=creer_popup_cyclone(cyclone),
            tooltip=f"🌀 {cyclone['nom']} ({cyclone['annee']})"
        ).add_to(groupe)



        point_proche = trouver_point_plus_proche(cyclone['trajectoire'])
        folium.Marker(
            location=point_proche,
            icon=folium.Icon(color='purple', icon='exclamation-triangle', prefix='fa'),
            tooltip='Impact max'
        ).add_to(groupe)

        folium.Marker(
            location=cyclone['trajectoire'][-1],
            icon=folium.Icon(color='darkred', icon='stop', prefix='fa'),
            tooltip='Fin'
        ).add_to(groupe)

    groupe_1980.add_to(carte)
    groupe_1990_2000.add_to(carte)
    groupe_2010.add_to(carte)
    groupe_2020.add_to(carte)

  
    # =============== LIEUX URGENCE ===============
    print("🏥 Lieux urgence...")
    groupe_urgence = folium.FeatureGroup(name='🏥 Hopitaux & Refuges', show=True)

    for lieu in lieux_urgence:
        couleur = 'red' if lieu['type'] == 'hopital' else 'blue'
        icone = 'plus' if lieu['type'] == 'hopital' else 'shield'

        folium.Marker(
            location=lieu['coords'],
            popup=f"<b>{lieu['nom']}</b><br>Capacite: {lieu['capacite']}<br>{lieu['description']}",
            icon=folium.Icon(color=couleur, icon=icone, prefix='fa'),
            tooltip=lieu['nom']
        ).add_to(groupe_urgence)

    groupe_urgence.add_to(carte)

   
        # =============== HOPITAUX OSM ===============
    hopitaux, ecoles = extraire_lieux_osmnx()
    
    # Liste pour stocker tous les lieux (manuels + OSM)
    tous_lieux_urgence = list(lieux_urgence)  # Copie des lieux manuels

    if hopitaux is not None and len(hopitaux) > 0:
        groupe_osm = folium.FeatureGroup(name='🏥 Hopitaux OSM ', show=True)

        for idx, row in hopitaux.iterrows():
            if row.geometry.geom_type == 'Point':
                nom_hopital = row.get('name', 'Hôpital OSM')
                
                # Popup détaillé pour les hôpitaux OSM
                popup_html = f"""
                <div style="font-family: Arial; font-size: 12px;">
                    <h4 style="margin: 0; color: darkred;">🏥 {nom_hopital}</h4>
                    <hr style="margin: 5px 0;">
                    <p style="margin: 3px 0;"><b>Type:</b> Hôpital OSM</p>
                    <p style="margin: 3px 0;"><b>Source:</b> OpenStreetMap</p>
                    <p style="margin: 3px 0;"><b>Coordonnées:</b> {row.geometry.y:.4f}, {row.geometry.x:.4f}</p>
                </div>
                """
                
                folium.Marker(
                    location=[row.geometry.y, row.geometry.x],
                    popup=folium.Popup(popup_html, max_width=300),
                    icon=folium.Icon(color='darkred', icon='plus-square', prefix='fa'),
                    tooltip=f"🏥 {nom_hopital}"
                ).add_to(groupe_osm)
                
                # Ajouter à la liste globale pour le calcul de distance
                tous_lieux_urgence.append({
                    'nom': nom_hopital,
                    'coords': [row.geometry.y, row.geometry.x],
                    'type': 'hopital_osm',
                    'capacite': 'N/A',
                    'description': 'Hôpital réel OSM'
                })

        groupe_osm.add_to(carte)
    
    print(f"   ℹ️ Total lieux d'urgence: {len(tous_lieux_urgence)} (manuels + OSM)")

    # Marqueur centre
    folium.Marker(
        location=[-21.1151, 55.5364],
        popup='<b>La Reunion</b>',
        icon=folium.Icon(color='black', icon='home', prefix='fa')
    ).add_to(carte)

    # =============== JAVASCRIPT INTERACTIF ===============
    print("🖱️ Ajout interactivite clic...")

    # Utiliser TOUS les lieux (manuels + OSM)
    refuges_json = json.dumps([{
        'nom': l['nom'],
        'lat': l['coords'][0],
        'lon': l['coords'][1],
        'type': l['type']
    } for l in tous_lieux_urgence])

    map_id = carte.get_name()

    js_code = f"""
    <script>
        console.log("🚀 Script interactif charge avec OSM routing");

        var refuges = {refuges_json};
        console.log("📍 Nombre total de lieux d'urgence:", refuges.length);
        
        var markerUser = null;
        var routeLayer = null;

        function calculerDistance(lat1, lon1, lat2, lon2) {{
            return Math.sqrt(Math.pow(lat2 - lat1, 2) + Math.pow(lon2 - lon1, 2));
        }}

        function trouverRefugeProche(lat, lon) {{
            var plusProche = refuges[0];
            var distMin = calculerDistance(lat, lon, plusProche.lat, plusProche.lon);

            for (var i = 1; i < refuges.length; i++) {{
                var dist = calculerDistance(lat, lon, refuges[i].lat, refuges[i].lon);
                if (dist < distMin) {{
                    distMin = dist;
                    plusProche = refuges[i];
                }}
            }}

            return plusProche;
        }}

        var iconeVerte = L.icon({{
            iconUrl: 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNSIgaGVpZ2h0PSI0MSIgdmlld0JveD0iMCAwIDI1IDQxIj48cGF0aCBmaWxsPSIjMDBBQTAwIiBkPSJNMTIuNSAwQzUuNiAwIDAgNS42IDAgMTIuNWMwIDguNSAxMi41IDI4LjUgMTIuNSAyOC41czEyLjUtMjAgMTIuNS0yOC41QzI1IDUuNiAxOS40IDAgMTIuNSAweiIvPjxjaXJjbGUgZmlsbD0id2hpdGUiIGN4PSIxMi41IiBjeT0iMTIuNSIgcj0iNSIvPjwvc3ZnPg==',
            iconSize: [25, 41],
            iconAnchor: [12, 41]
        }});

        window.addEventListener('load', function() {{
            setTimeout(function() {{
                try {{
                    var map = window["{map_id}"];

                    if (!map) {{
                        console.error("❌ Carte non trouvee");
                        return;
                    }}

                    console.log("✅ Carte trouvee avec routing OSRM");

                    map.on('click', function(e) {{
                        console.log("🖱️ Clic:", e.latlng);

                        var lat = e.latlng.lat;
                        var lon = e.latlng.lng;

                        if (markerUser) map.removeLayer(markerUser);
                        if (routeLayer) map.removeLayer(routeLayer);

                        markerUser = L.marker([lat, lon], {{icon: iconeVerte}}).addTo(map);
                        console.log("✅ Marqueur vert ajoute");

                        var refuge = trouverRefugeProche(lat, lon);
                        console.log("🏥 Refuge le plus proche:", refuge.nom, "Type:", refuge.type);

                        // Type d'icône selon le type de lieu
                        var refugeIcon = refuge.type === 'hopital' || refuge.type === 'hopital_osm' ? '🏥' : '🛡️';

                        // Appel OSRM pour itinéraire routier
                        var osrmUrl = 'https://router.project-osrm.org/route/v1/driving/' + 
                                      lon + ',' + lat + ';' + 
                                      refuge.lon + ',' + refuge.lat + 
                                      '?overview=full&geometries=geojson';

                        console.log("🔍 Appel OSRM...");

                        fetch(osrmUrl)
                            .then(response => response.json())
                            .then(data => {{
                                if (data.routes && data.routes.length > 0) {{
                                    var route = data.routes[0];
                                    var routeCoords = route.geometry.coordinates.map(coord => [coord[1], coord[0]]);

                                    routeLayer = L.polyline(routeCoords, {{
                                        color: 'red',
                                        weight: 4,
                                        opacity: 0.8
                                    }}).addTo(map);

                                    var distKm = (route.distance / 1000).toFixed(1);
                                    var dureeMin = Math.round(route.duration / 60);

                                    L.popup()
                                        .setLatLng([lat, lon])
                                        .setContent(
                                            '<div style="font-family: Arial; font-size: 12px;">' +
                                            '<h4 style="margin: 0; color: red;">' + refugeIcon + ' ITINERAIRE ROUTIER</h4>' +
                                            '<hr style="margin: 5px 0;">' +
                                            '<p style="margin: 5px 0;"><b>Lieu le plus proche :</b></p>' +
                                            '<p style="margin: 5px 0;"><b>' + refuge.nom + '</b></p>' +
                                            '<p style="margin: 3px 0; font-size: 11px; color: #666;">Type: ' + (refuge.type === 'hopital_osm' ? 'Hôpital OSM réel' : refuge.type.toUpperCase()) + '</p>' +
                                            '<hr style="margin: 5px 0;">' +
                                            '<p style="margin: 5px 0;">📍 Distance : <b>' + distKm + ' km</b></p>' +
                                            '<p style="margin: 5px 0;">⏱️ Durée : <b>' + dureeMin + ' min</b></p>' +
                                            '<p style="margin: 3px 0; font-size: 10px; color: #666;">Calculé par OSRM</p>' +
                                            '</div>'
                                        )
                                        .openOn(map);

                                    console.log("✅ Itinéraire tracé");
                                }} else {{
                                    throw new Error("Pas de route");
                                }}
                            }})
                            .catch(error => {{
                                console.error("❌ Erreur OSRM:", error);
                                
                                // Fallback: ligne droite
                                routeLayer = L.polyline([[lat, lon], [refuge.lat, refuge.lon]], {{
                                    color: 'orange',
                                    weight: 4,
                                    opacity: 0.7,
                                    dashArray: '10, 5'
                                }}).addTo(map);

                                var distKm = (calculerDistance(lat, lon, refuge.lat, refuge.lon) * 111).toFixed(1);

                                L.popup()
                                    .setLatLng([lat, lon])
                                    .setContent(
                                        '<div style="font-family: Arial; font-size: 12px;">' +
                                        '<h4 style="margin: 0; color: orange;">📏 DISTANCE DIRECTE</h4>' +
                                        '<hr style="margin: 5px 0;">' +
                                        '<p style="margin: 5px 0;"><b>Lieu proche :</b></p>' +
                                        '<p style="margin: 5px 0;"><b>' + refuge.nom + '</b></p>' +
                                        '<p style="margin: 3px 0; font-size: 11px; color: #666;">Type: ' + (refuge.type === 'hopital_osm' ? 'Hôpital OSM' : refuge.type.toUpperCase()) + '</p>' +
                                        '<hr style="margin: 5px 0;">' +
                                        '<p style="margin: 5px 0;">Distance : <b>~' + distKm + ' km</b></p>' +
                                        '<p style="margin: 3px 0; font-size: 10px; color: #666;">Itinéraire routier indisponible</p>' +
                                        '</div>'
                                    )
                                    .openOn(map);
                            }});
                    }});

                }} catch(error) {{
                    console.error("❌ Erreur:", error);
                }}
            }}, 2000);
        }});
    </script>
    """

    carte.get_root().html.add_child(folium.Element(js_code))


    # =============== LEGENDE ===============
        # =============== LEGENDE ===============
    legend_html = """
    <div style="position: fixed; bottom: 50px; right: 50px; width: 380px;
                background: white; border: 3px solid #FF0000; border-radius: 10px;
                box-shadow: 0 0 20px rgba(0,0,0,0.5); padding: 15px; font-size: 11px; z-index: 1000;">
        <h4 style="margin-top: 0; text-align: center; color: #FF0000;">
            🌀 CARTE CYCLONES LA RÉUNION
        </h4>
        <hr style="margin: 10px 0; border: 2px solid #FF0000;">

        <!-- INSTRUCTION PRINCIPALE EN ÉVIDENCE -->
        <div style="background: #FFE6E6; padding: 12px; border-radius: 5px; margin-bottom: 12px; border: 2px solid #FF0000;">
            <b style="color: #FF0000; font-size: 13px;">🖱️ MODE ITINÉRAIRE INTERACTIF</b><br>
            <span style="font-size: 12px; font-weight: bold; color: #000;">
            👉 CLIQUEZ N'IMPORTE OÙ sur la carte pour :
            </span>
            <ul style="margin: 5px 0 0 15px; padding: 0; font-size: 11px;">
                <li>Afficher le lieu d'urgence le plus proche</li>
                <li>Calculer l'itinéraire routier optimal</li>
                <li>Voir la distance (km) et durée (min)</li>
            </ul>
        </div>

        <!-- LÉGENDE DES ÉLÉMENTS -->
        <p style="margin: 5px 0;"><b>🌀 CYCLONES</b> : 8 trajectoires historiques (1980-2022)</p>
        <p style="margin: 5px 0;"><b>🟣 PANNEAU VIOLET</b> : Point d'impact maximal</p>
        <p style="margin: 5px 0;"><b>🏥 MARQUEURS ROUGES</b> : Hôpitaux</p>
        <p style="margin: 5px 0;"><b>🛡️ MARQUEURS BLEUS</b> : Refuges</p>
        <p style="margin: 5px 0;"><b>🟢 MARQUEUR VERT</b> : Votre position cliquée</p>
        <p style="margin: 5px 0;"><b>🔴 LIGNE ROUGE</b> : Itinéraire routier calculé</p>

        <hr style="margin: 8px 0;">

        <p style="font-size: 10px; color: #666; text-align: center; margin: 5px 0;">
            💡 Utilisez le menu des couches (haut-gauche) pour filtrer par décennie
        </p>
        <p style="font-size: 9px; color: #999; text-align: center; margin: 0;">
            ⚙️ Données : Météo-France + OpenStreetMap + OSRM
        </p>
    </div>
    """
    carte.get_root().html.add_child(folium.Element(legend_html))


    # Plugins
    plugins.Fullscreen(position='topright').add_to(carte)
    plugins.MiniMap(toggle_display=True).add_to(carte)
    plugins.MousePosition().add_to(carte)

    # Controle couches
    folium.LayerControl(position='topleft', collapsed=False).add_to(carte)

    print("\n✅ Carte complete creee !")
    return carte


# ============================================================
# EXECUTION
# ============================================================

if __name__ == "__main__":
    carte = creer_carte_complete_finale()
    fichier = "cyclones_reunion_.html"
    carte.save(fichier)

    print(f"\n✅ Carte sauvegardee : {fichier}")
    print("\n📊 RESUME COMPLET :")
    print(f"   - Cyclones : {len(cyclones_data)} (1980-2022)")
    print(f"   - Lieux urgence : {len(lieux_urgence)}")
    print("   - Hopitaux : OSMnx (reels)")
    print("   - Clic interactif : Refuge plus proche")


    
    # OUVRIR AUTOMATIQUEMENT DANS UNE VERSION WEB
    print("\n🌐 Ouverture automatique dans le navigateur...")
    chemin_fichier = 'file:///' + os.getcwd() + '/' + fichier
    webbrowser.open_new_tab(chemin_fichier)
    print("✅ Carte ouverte dans le navigateur !")

