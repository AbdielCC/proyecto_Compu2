import requests

class GeolocalizacionAPI:
    def __init__(self):
        self.base_url = "https://static-maps.yandex.ru/1.x/"

    def obtener_mapa(self, ubicaciones, centro, zoom=12, tamaño="600,400"):
        """
        Genera una URL para un mapa estático con marcadores utilizando OpenStreetMap.
        :return: URL de la imagen del mapa.
        """
        markers = []
        for ubicacion in ubicaciones:
            markers.append(f"pt={ubicacion['lng']},{ubicacion['lat']},pm2rdl")

        params = {
            "l": "map",
            "size": tamaño,
            "z": zoom,
            "ll": f"{centro['lng']},{centro['lat']}",
        }
        markers_param = "&".join(markers)
        url = f"{self.base_url}?{markers_param}&" + "&".join(f"{k}={v}" for k, v in params.items())
        return url
