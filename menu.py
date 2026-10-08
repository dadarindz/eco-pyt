import tkinter as tk
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import date, timedelta

from constants import *
from weather import *
from weather_queries import *
from plot import *

# ----------------------------------------------------------------------
# Variables globales
# ----------------------------------------------------------------------
# Ville actuelle
city = "Paris"
# city = "Bordeaux"

# Premier jour affiché dans l'écran des prévisions
start_day = date.today()

# ImageTk : ces variables globales permettent d'éviter que le garbage collector ne les efface
image_background = None
weather_icon = None
# Zone du graphique Matplotlib, gardée pour pouvoir la détruire au prochain affichage
zone_graphique = None

# ----------------------------------------------------------------------
# Canvas
# ----------------------------------------------------------------------

def load_background(canvas):
    """Charge "assets/blue_sky.jpg" (ou "assets/night_sky.jpg" la nuit), la redimensionne et la place sur le canvas."""
    global image_background

    if time_of_day() == "night":
        path = "assets/night_sky.jpg"
    else:
        path = "assets/blue_sky.jpg"

    image = Image.open(path).convert("RGBA")
    image = image.resize((WIDTH, HEIGHT))
    image_background = ImageTk.PhotoImage(image)
    # anchor = "nw" : le point (0, 0) correspond au coin en haut à gauche de l'image
    # Pas de tag "ecran" : le fond n'est jamais effacé
    canvas.create_image(0, 0, image = image_background, anchor = "nw")


def erase_screen(canvas):
    """Supprime tout ce qui a le tag 'ecran'."""
    canvas.delete("ecran")


# ----------------------------------------------------------------------
# Ecrans
# ----------------------------------------------------------------------

def change_city(window, canvas, new_city):
    """Appelée par le menu déroulant : change la ville et redessine l'accueil."""
    global city
    city = new_city
    draw_welcome_screen(window, canvas)


def draw_welcome_screen(window, canvas):
    """Écran 1 : Icône de la météo, température actuelle, températures min et max du jour."""
    global weather_icon

    erase_screen(canvas)
    temperature, code, t_min, t_max = get_current_weather(city)

    # Menu déroulant pour choisir la ville
    city_variable = tk.StringVar(window, value = city)
    city_menu = tk.OptionMenu(window, city_variable, *CITIES,
                              command = lambda new_city : change_city(window, canvas, new_city))
    city_menu.config(font = ("Helvetica", 20, "bold"))
    canvas.create_window(WIDTH / 2, 60, window = city_menu, tags = "ecran")

    # Icône de la météo actuelle (version de nuit si besoin)
    icon = icon_of_code(code)
    if time_of_day() == "night":
        icon = night_icon(icon)
    if icon != "unknown": # pas d'icône prévue pour un code inconnu
        image = Image.open("assets/icons/" + icon + ".png").convert("RGBA")
        image = image.resize((160, 160))
        weather_icon = ImageTk.PhotoImage(image)
        canvas.create_image(WIDTH / 2, 190, image = weather_icon, tags = "ecran")

    # Températures
    canvas.create_text(WIDTH / 2, 320, text = f"{round(temperature)} °C",
                       font = ("Helvetica", 40, "bold"), fill = "white", tags = "ecran")
    canvas.create_text(WIDTH / 2, 370, text = f"Min : {round(t_min)} °C      Max : {round(t_max)} °C",
                       font = ("Helvetica", 12), fill = "white", tags = "ecran")

    # Bouton vers l'écran des prévisions (on repart toujours d'aujourd'hui)
    button = tk.Button(window, text = "Prévisions 7 jours",
                       command = lambda : draw_forecast(window, canvas, date.today()))
    canvas.create_window(WIDTH / 2, 450, window = button, tags = "ecran")


def draw_forecast(window, canvas, new_start_day = None):
    """Écran 2 : graphique des températures sur 7 jours"""
    global start_day, zone_graphique

    erase_screen(canvas)
    if new_start_day is not None:
        start_day = new_start_day
    dates, t_mins, t_maxs = get_forecast(city, start_day)
    end_day = start_day + timedelta(days = 6)

    # Titre, ville et période
    canvas.create_text(WIDTH / 2, 30, text = f"Prévisions sur 7 jours - {city}",
                       font = ("Helvetica", 16, "bold"), fill = "white", tags = "ecran")
    canvas.create_text(WIDTH / 2, 55, text = f"Du  {start_day.isoformat()}  au  {end_day.isoformat()}",
                       font = ("Helvetica", 10), fill = "white", tags = "ecran")

    # On détruit l'ancien graphique pour ne pas les accumuler en mémoire
    if zone_graphique is not None:
        zone_graphique.get_tk_widget().destroy()
        zone_graphique = None

    if len(dates) > 0:
        figure = create_plot(dates, t_mins, t_maxs)
        zone_graphique = FigureCanvasTkAgg(figure, master = window)
        zone_graphique.draw()
        canvas.create_window(WIDTH / 2, 245, window = zone_graphique.get_tk_widget(), tags = "ecran")
    else:
        canvas.create_text(WIDTH / 2, 245, text = "Pas de prévisions disponibles\npour cette période",
                           font = ("Helvetica", 14), fill = "white", justify = "center", tags = "ecran")

    # Boutons : reculer de 7 jours, retour à l'accueil, avancer de 7 jours
    button_previous = tk.Button(window, text = "◄", width = 4,
                                command = lambda : draw_forecast(window, canvas, start_day - timedelta(days = 7)))
    button_home = tk.Button(window, text = "Accueil",
                            command = lambda : draw_welcome_screen(window, canvas))
    button_next = tk.Button(window, text = "►", width = 4,
                            command = lambda : draw_forecast(window, canvas, start_day + timedelta(days = 7)))
    canvas.create_window(80, 450, window = button_previous, tags = "ecran")
    canvas.create_window(WIDTH / 2, 450, window = button_home, tags = "ecran")
    canvas.create_window(WIDTH - 80, 450, window = button_next, tags = "ecran")
