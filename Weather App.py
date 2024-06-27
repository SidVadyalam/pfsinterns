import json
import requests
from tkinter import *


weather_api_key = '1814607f6953f642d288090dfccd9a3c'
city, country_code, offset = '*', '~', '0'
weather_request = f'https://api.openweathermap.org/data/2.5/weather?q={city},{country_code}&appid={weather_api_key}'
countries_request = 'https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/countries-codes/records?select=label_en%2C%20iso2_code&limit=100&offset=' # 100

root = Tk()
root.title("Weather App")
root.geometry('500x500')

def format(city, country_code):
    weather_data = requests.get(weather_request.replace('~', country_code).replace('*', city))
    print(weather_data.json())
    if len(weather_data.json()) > 2:
        temp_label.config(text=f"Temperature: {weather_data.json()['main']['temp']} ˚K")
        feels_like_label.config(text=f"Feels Like: {weather_data.json()['main']['feels_like']} ˚K")
        pressure_label.config(text=f"Pressure: {weather_data.json()['main']['pressure']} hPa")
        humidity_label.config(text=f"Humidity: {weather_data.json()['main']['temp']} %")
        temp_min_label.config(text=f"Minimum Temperature: {weather_data.json()['main']['temp_max']} ˚K")
        temp_max_label.config(text=f"Maximum Temperature: {weather_data.json()['main']['temp_min']} ˚K")
        sea_level_label.config(text=f"Sea Level Pressure: {weather_data.json()['main']['sea_level']} hPa")

        wind_speed_label.config(text=f"Wind Speed: {weather_data.json()['wind']['speed']} m/s")
        wind_direction_label.config(text=f"Wind Direction: {weather_data.json()['wind']['deg']}˚")
        weather_type_label.config(text=f"Weather Type: {weather_data.json()['weather'][0]['description']} m/s")
        cloudiness_label.config(text=f"Cloudiness: {weather_data.json()['clouds']['all']} %")
        visibility_label.config(text=f"Visibility: {weather_data.json()['visibility']} Km")
        coordinates_label.config(text=f"Coordinates: ({weather_data.json()['coord']['lat']},{weather_data.json()['coord']['lon']})")
        ground_level_label.config(text=f"Ground Level Pressure: {weather_data.json()['main']['grnd_level']} hPa")
        
        
    else:
        message.config(text='Please enter valid country/city name', fg='red')
    
    


def submit():
    global city, country_code, offset, message
    
    if country_button.get() == '' or city_button.get() == '':
        return

    submit_button.config(state=DISABLED)
    root.after(3000, lambda: submit_button.config(state=NORMAL))

    message.config(text='Enter location to get weather', fg='black')
    
    country = (' '.join(country_button.get().split())).strip().lower().title()
    city = city_button.get().strip().lower().title()

    if country == 'Vietnam':
        country_code = 'VN'

    else:
        country_db = requests.get(countries_request + offset)
        country_db = country_db.json()['results']
        i = 0

        

        while i < len(country_db):

            if country_db[i]['label_en'][:len(country) + 1] == country:
                country_code = country_db[i]['iso2_code']
                break

            if i == 99 and offset == '0':
                offset = '100'
                country_db = requests.get(countries_request + offset)
                country_db = country_db.json()['results']
                i = 0
            elif i == 99 and offset == '100':
                offset = '200'
                country_db = requests.get(countries_request + offset)
                country_db = country_db.json()['results']
                i = 0

            
            i += 1
        
    if country_code == '~':
        message.config(text='Please enter valid country/city name', fg='red')
    else:
        format(city, country_code)

        country_code = '~'

    offset = '0'
    

frame_intro = LabelFrame(root)
frame_intro.grid(row=0, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
Label(frame_intro, text='Welcome to the Weather App!').pack()

frame_search = LabelFrame(root)
frame_search.grid(row=1, column=0, columnspan=2)
message = Label(frame_search, text='Enter location to get weather')
message.grid(row=0, column=0, columnspan=2)
Label(frame_search, text='Country:', anchor='w').grid(row=1, column=0, padx=10)
Label(frame_search, text='City:', anchor='w').grid(row=2, column=0, padx=10)
country_button = Entry(frame_search)
country_button.grid(row=1, column=1, pady=10)
city_button = Entry(frame_search)
city_button.grid(row=2, column=1, pady=10)
submit_button = Button(frame_search, text='Submit', comman=submit)
submit_button.grid(row=3, column=0, columnspan=2, ipadx=50)

frame_information = LabelFrame(root)
frame_information.grid(row=2, column=0, columnspan=2, pady=10, padx=10)
weather_description_label = Label(frame_information, text='Weather Description')
weather_description_label.grid(row=0, column=0, columnspan=2)

frame_temp_and_pressure = LabelFrame(frame_information)
frame_temp_and_pressure.grid(row=1, column=0, padx=10)
temp_label = Label(frame_temp_and_pressure, text='Temperature: ')
temp_label.grid(row=0, column=0)
feels_like_label = Label(frame_temp_and_pressure, text='Feels Like: ')
feels_like_label.grid(row=1, column=0)
pressure_label = Label(frame_temp_and_pressure, text='Pressure: ')
pressure_label.grid(row=2, column=0)
humidity_label = Label(frame_temp_and_pressure, text='Humidity: ')
humidity_label.grid(row=3, column=0)
temp_min_label = Label(frame_temp_and_pressure, text='Minimum Temperature: ')
temp_min_label.grid(row=4, column=0)
temp_max_label = Label(frame_temp_and_pressure, text='Maximum Temperature: ')
temp_max_label.grid(row=5, column=0)
sea_level_label = Label(frame_temp_and_pressure, text='Sea Level Pressure: ')
sea_level_label.grid(row=6, column=0)


frame_sky_information = LabelFrame(frame_information)
frame_sky_information.grid(row=1, column=1, padx=10)
wind_speed_label = Label(frame_sky_information, text='Wind Speed: ')
wind_speed_label.grid(row=0, column=0)
wind_direction_label = Label(frame_sky_information, text='Wind Direction: ')
wind_direction_label.grid(row=1, column=0)
weather_type_label = Label(frame_sky_information, text='Weather Type: ')
weather_type_label.grid(row=2, column=0)
cloudiness_label = Label(frame_sky_information, text='Cloudiness: ')
cloudiness_label.grid(row=3, column=0)
visibility_label = Label(frame_sky_information, text='Visisbility: ')
visibility_label.grid(row=4, column=0)
coordinates_label = Label(frame_sky_information, text='Coordinates: ')
coordinates_label.grid(row=5, column=0)
ground_level_label = Label(frame_sky_information, text='Ground Level Pressure: ')
ground_level_label.grid(row=6, column=0)

root.mainloop()
