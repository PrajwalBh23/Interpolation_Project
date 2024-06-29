import folium

districts = [
    {"name": "Nagpur", "lat": 21.1458, "lon": 79.0882, "temp": 32},
    {"name": "Wardha", "lat": 20.7453, "lon": 78.6022, "temp": 34},
    {"name": "Chandrapur", "lat": 19.9600, "lon": 79.2961, "temp": 36},
    # Add other districts here
]

def create_map(districts):
    # Create a folium map centered around Vidarbha region
    m = folium.Map(location=[20.5, 79.5], zoom_start=8)
    
    # Add markers for each district
    for district in districts:
        folium.Marker(
            location=[district["lat"], district["lon"]],
            popup=f"{district['name']}: {district['temp']}°C",
            icon=folium.Icon(color="blue")
        ).add_to(m)
    
    # Add click event to interpolate temperature
    m.add_child(folium.LatLngPopup())
    
    # Add custom JavaScript to handle click events
    click_js = """
    function onMapClick(e) {
        var lat = e.latlng.lat;
        var lon = e.latlng.lng;
        
        fetch(`/interpolate?lat=${lat}&lon=${lon}`)
            .then(response => response.json())
            .then(data => {
                L.popup()
                 .setLatLng(e.latlng)
                 .setContent('Interpolated Temperature: ' + data.temp.toFixed(2) + '°C')
                 .openOn(this);
            });
    }

    var map = document.querySelector('.folium-map')._leaflet_map;
    map.on('click', onMapClick);
    """
    
    m.get_root().html.add_child(folium.Element(f"<script>{click_js}</script>"))
    
    return m

# Example usage
map_object = create_map(districts)
map_object.save('vidarbha_map.html')
