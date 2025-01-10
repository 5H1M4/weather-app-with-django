from django.shortcuts import render
import requests
import datetime

def index(request):
    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'tirana'

    if 'forecast_type' in request.POST and request.POST['forecast_type'] == '5_day':
        url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid=0a2cb1caa02e515749dada0c93077da1'
        PARAMS = {'units': 'metric'}
        data = requests.get(url, params=PARAMS).json()

        if 'list' in data:
            forecast = []
            for forecast_entry in data['list']:
                forecast.append({
                    'date': forecast_entry['dt_txt'],
                    'temp': forecast_entry['main']['temp'],
                    'description': forecast_entry['weather'][0]['description'],
                    'icon': forecast_entry['weather'][0]['icon']
                })
            
            # Sort the forecast by date (and time)
            forecast.sort(key=lambda x: x['date'])

            context = {
                'forecast': forecast,
                'city': city
            }
        else:
            context = {
                'error': "City not found, please enter a valid city name.",
                'city': city
            }
    else:
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=0a2cb1caa02e515749dada0c93077da1'
        PARAMS = {'units': 'metric'}
        data = requests.get(url, params=PARAMS).json()

        if 'weather' in data:
            description = data['weather'][0]['description']
            icon = data['weather'][0]['icon']
            temp = data['main']['temp']
            day = datetime.date.today()
            context = {
                'description': description,
                'icon': icon,
                'temp': temp,
                'day': day,
                'city': city
            }
        else:
            context = {
                'error': "City not found, please enter a valid city name.",
                'city': city
            }

    return render(request, 'index.html', context)
