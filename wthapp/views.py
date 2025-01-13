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
            # Dictionary to store forecasts by date
            forecasts_by_date = {}
            
            for forecast_entry in data['list']:
                # Convert timestamp to datetime
                date_time = datetime.datetime.strptime(forecast_entry['dt_txt'], '%Y-%m-%d %H:%M:%S')
                date = date_time.date()
                hour = date_time.hour

                # Categorize time periods
                if 5 <= hour <= 11:
                    time_period = 'morning'
                elif 12 <= hour <= 17:
                    time_period = 'midday'
                elif 18 <= hour <= 23:
                    time_period = 'night'
                else:
                    continue  # Skip other hours

                # Store only one forecast per time period per day
                if date not in forecasts_by_date:
                    forecasts_by_date[date] = {}
                
                if time_period not in forecasts_by_date[date]:
                    forecasts_by_date[date][time_period] = {
                        'date': date,
                        'time_period': time_period,
                        'temp': forecast_entry['main']['temp'],
                        'description': forecast_entry['weather'][0]['description'],
                        'icon': forecast_entry['weather'][0]['icon']
                    }

            # Convert dictionary to list and sort by date
            forecast = []
            for date in sorted(forecasts_by_date.keys())[:5]:  # Limit to 5 days
                day_forecasts = forecasts_by_date[date]
                for period in ['morning', 'midday', 'night']:
                    if period in day_forecasts:
                        forecast.append(day_forecasts[period])

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