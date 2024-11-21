from BaseDeDatos import BaseDeDatos
from GeolocalizacionAPI import GeolocalizacionAPI
from InterfazGrafica import InterfazGrafica
import tkinter as tk

db = BaseDeDatos(host="localhost", database="inventario", user="postgres", password="ul1se3ol4")
db.crear_tablas()
maps_api = GeolocalizacionAPI()

root = tk.Tk()
app = InterfazGrafica(root, db, maps_api)

root.mainloop()