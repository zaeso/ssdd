import sqlite3
from config import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

class DB_Map():
    def __init__(self, database):
        self.database = database
        self.marker_colors = {}

    def create_user_table(self):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS users_cities (
                                user_id INTEGER,
                                city_id TEXT,
                                FOREIGN KEY(city_id) REFERENCES cities(id)
                            )''')
            conn.commit()

    def add_city(self, user_id, city_name):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM cities WHERE city=?", (city_name,))
            city_data = cursor.fetchone()
            if city_data:
                city_id = city_data[0]
                conn.execute('INSERT INTO users_cities VALUES (?, ?)', (user_id, city_id))
                conn.commit()
                return 1
            else:
                return 0

    def select_cities(self, user_id):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT cities.city FROM users_cities
                            JOIN cities ON users_cities.city_id = cities.id
                            WHERE users_cities.user_id = ?''', (user_id,))
            cities = [row[0] for row in cursor.fetchall()]
            return cities

    def get_coordinates(self, city_name):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT lat, lng FROM cities WHERE city = ?''', (city_name,))
            coordinates = cursor.fetchone()
            return coordinates

    def get_marker_color(self, user_id):
        if user_id in self.marker_colors:
            return self.marker_colors[user_id]
        else:
            return 'red'  # Default marker color

    def set_marker_color(self, user_id, color):
        self.marker_colors[user_id] = color

    def create_graph(self, cities=None, countries=False, continents=False, oceans=False, marker_color='red'):
        plt.figure(figsize=(10, 6))
        ax = plt.axes(projection=ccrs.PlateCarree())

        
        if continents:
            ax.add_feature(cfeature.LAND, facecolor=cfeature.COLORS['land'])
        
        
        if countries:
            ax.add_feature(cfeature.BORDERS, edgecolor='black')

        
        if oceans:
            ax.add_feature(cfeature.OCEAN, facecolor=cfeature.COLORS['water'])

        if cities:
            if isinstance(cities, str):
                coordinates = self.get_coordinates(cities)
                if coordinates:
                    ax.plot(coordinates[1], coordinates[0], marker='o', color=marker_color, markersize=8, transform=ccrs.PlateCarree())
            elif isinstance(cities, list):
                for city in cities:
                    coordinates = self.get_coordinates(city)
                    if coordinates:
                        ax.plot(coordinates[1], coordinates[0], marker='o', color=marker_color, markersize=8, transform=ccrs.PlateCarree())

        plt.title("Карта")
        plt.savefig('map.png')
        plt.close()

