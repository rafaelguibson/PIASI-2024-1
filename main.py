import geopandas as gpd
import folium

# Caminho fixo para o shapefile
shapefile_path = "resources/PERIMETRO.CORRIGIDO.shp"

# 1. Carregar o shapefile
gdf = gpd.read_file(shapefile_path)

# 2. Garantir que o shapefile tenha sistema de coordenadas
if gdf.crs is None:
    raise ValueError("O shapefile não tem um sistema de coordenadas definido.")

# Reprojetar para WGS 84 (necessário para Google Maps)
gdf = gdf.to_crs(epsg=4326)

# 3. Calcular o centro do shapefile para centralizar o mapa
centro = gdf.geometry.union_all().centroid  # Alterado de unary_union para union_all
latitude, longitude = centro.y, centro.x

# 4. Folium dependencia que disponibiliza os mapas do google maps
mapa = folium.Map(
    location=[latitude, longitude],
    zoom_start=13,
    tiles="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
    attr="Google",
    max_zoom=20,
    api_key="api_key"
)

# 5. Adicionar o shapefile ao mapa
for _, row in gdf.iterrows():
    geojson = folium.GeoJson(
        row.geometry,
        name="Shapefile",
        style_function=lambda x: {"color": "red", "weight": 2}
    )
    geojson.add_to(mapa)

# 6. Salvar o mapa em um arquivo HTML
mapa.save("mapa_georeferenciado.html")
print("Mapa gerado: mapa_georeferenciado.html")
