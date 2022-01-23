import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror
from configparser import ConfigParser
import requests

# extract key from the configuration file

config_file = "config.ini"
config = ConfigParser()
config.read(config_file)

API_KEY = config['gfg']['api']
BASE_URL = "http://api.openweathermap.org/data/2.5/weather" 
LANG_SETTING = "lang=es"

def fetch_weather():       
    city = city_var.get()
    request_url = f"{BASE_URL}?appid={API_KEY}&{LANG_SETTING}&q={city}"
    response = requests.get(request_url)
    
    try:
        if response.status_code == 200:
            data = response.json()
            weather = data['weather'][0]['description']
            temperature = round(data['main']['temp'] - 273.15, 2)
            
            weather_result = f"El clima es : {weather}"
            weather_result_label.config(text=weather_result)
            
            temp_result = f"La temperatura es : {temperature} °C"
            temp_result_label.config(text=temp_result)
        else:
            showerror(title= 'Error', message='Ocurrió un error. Por favor, intentar mas tarde.')
        
    except ConnectionError as error:
        showerror(title='Error', message=error)

# root window
root = tk.Tk()
root.title('Real Time Weather')
root.geometry('400x100')
root.resizable(False, False)

#frame
frame = ttk.Frame(root)

# field options
options = {'padx': 5, 'pady': 2}

# city label
city_label = ttk.Label(frame, text='Ingrese nombre de ciudad:')
city_label.grid(column=0, row=0, sticky='W', **options)

# city entry

city_var = tk.StringVar()
city_entry = ttk.Entry(frame, textvariable=city_var)
city_entry.grid(column=1, row=0, **options)
city_entry.focus()

# Search Button

search_button = ttk.Button(frame, text='Buscar')
search_button.grid(column=2, row=0, sticky='W', **options)
search_button.configure(command=fetch_weather)

# result label
weather_result_label = ttk.Label(frame)
weather_result_label.grid(row=1, columnspan=3, **options)

temp_result_label = ttk.Label(frame)
temp_result_label.grid(row=2, columnspan=3, **options)

# add padding to the frame and show it
frame.grid(padx=10, pady=10)


# start the app
root.mainloop()

