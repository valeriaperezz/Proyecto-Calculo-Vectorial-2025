import folium
from branca.element import Element

# 1. Configuración Inicial
# Definimos las coordenadas centrales para la vista inicial (Guayaquil)
latitud_guayaquil = -2.1894
longitud_guayaquil = -79.8891

# 2. Generación del Objeto Mapa
# Creamos el mapa base usando Folium.
mapa = folium.Map(
    location=[latitud_guayaquil, longitud_guayaquil],
    zoom_start=13,
    control_scale=True  # Añade una escala de distancia en la esquina
)

# 3. Cálculo y Visualización

script_calculo = """
<script>
    function initClickEvent() {
        var mapInstance = null;
        for (var key in window) {
            if (key.startsWith('map_')) {
                mapInstance = window[key];
                break;
            }
        }

        if (mapInstance) {
            mapInstance.on('click', function(e) {
                var lat = e.latlng.lat;
                var lng = e.latlng.lng;
                var R = 6371; 

                // --- CÁLCULOS ---
                var phi = lat * (Math.PI / 180);
                var lam = lng * (Math.PI / 180);

                var cos_phi = Math.cos(phi);
                var sin_phi = Math.sin(phi);
                var cos_lam = Math.cos(lam);
                var sin_lam = Math.sin(lam);

                // Cartesianas
                var x = R * cos_phi * cos_lam;
                var y = R * cos_phi * sin_lam;
                var z = R * sin_phi;

                // Sensibilidad
                var dx_dphi = -R * sin_phi * cos_lam;
                var dy_dphi = -R * sin_phi * sin_lam;
                var dz_dphi = R * cos_phi;

                // Popup Final
                var content = '<div style="font-family: Arial; font-size: 11px; width: 340px; line-height: 1.4;">' +

                              // SECCIÓN 1
                              '<h4 style="margin:0 0 5px 0; color:#2980b9; border-bottom: 1px solid #ccc; padding-bottom:3px; font-weight:900;">' + 
                              '1. Conversión de (' + lat.toFixed(3) + '°, ' + lng.toFixed(3) + '°)</h4>' +

                              '<b>a) Radianes:</b><br>' +
                              '&phi; = ' + phi.toFixed(4) + ' rad | &lambda; = ' + lam.toFixed(4) + ' rad<br><br>' +

                              '<b>b) Cartesianas:</b><br>' + 
                              '<i>X = ' + R + ' · ' + cos_phi.toFixed(3) + ' · ' + cos_lam.toFixed(3) + '</i> = <b style="color:#c0392b; font-size:12px;">' + x.toFixed(1) + ' km</b><br>' +
                              '<i>Y = ' + R + ' · ' + cos_phi.toFixed(3) + ' · ' + sin_lam.toFixed(3) + '</i> = <b style="color:#c0392b; font-size:12px;">' + y.toFixed(1) + ' km</b><br>' +
                              '<i>Z = ' + R + ' · ' + sin_phi.toFixed(3) + '</i> = <b style="color:#c0392b; font-size:12px;">' + z.toFixed(1) + ' km</b><br><br>' +

                              // SECCIÓN 2
                              '<h4 style="margin:0 0 5px 0; color:#e67e22; border-bottom: 1px solid #ccc; padding-bottom:3px; font-weight:900;">' + 
                              '2. Sensibilidad de (' + lat.toFixed(3) + '°, ' + lng.toFixed(3) + '°)</h4>' +

                              '<span style="background-color:#fcf3cf; padding:2px;"><b>Constante:</b> Longitud (&lambda; = ' + lng.toFixed(3) + '°)</span><br>' +
                              '<i style="color:#555;">(Cambio por cada radián al moverse al Norte)</i><br>' +

                              '<b>&part;x/&part;&phi;:</b> -' + R + ' · ' + sin_phi.toFixed(3) + ' · ' + cos_lam.toFixed(3) + ' = <b style="color:#c0392b;">' + dx_dphi.toFixed(1) + ' km/rad</b><br>' +
                              '<b>&part;y/&part;&phi;:</b> -' + R + ' · ' + sin_phi.toFixed(3) + ' · ' + sin_lam.toFixed(3) + ' = <b style="color:#c0392b;">' + dy_dphi.toFixed(1) + ' km/rad</b><br>' +
                              '<b>&part;z/&part;&phi;:</b> ' + R + ' · ' + cos_phi.toFixed(3) + ' = <b style="color:#c0392b;">' + dz_dphi.toFixed(1) + ' km/rad</b>' +

                              '</div>';

                L.popup()
                    .setLatLng(e.latlng)
                    .setContent(content)
                    .openOn(mapInstance);
            });
        }
    }
    window.onload = initClickEvent;
</script>
"""

# Inyectamos el script en el mapa
mapa.get_root().html.add_child(Element(script_calculo))

# Guardado Final
nombre_archivo = "mapa_proyecto_final.html"
mapa.save(nombre_archivo)

print(f"¡Listo! Abrir el archivo '{nombre_archivo}'.")
