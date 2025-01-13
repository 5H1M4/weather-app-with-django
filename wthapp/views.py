from django.shortcuts import render
import requests
import datetime
from collections import defaultdict

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
            forecasts_by_date = defaultdict(dict)
            
            # Get the first forecast's date as reference for Monday
            first_forecast_date = None
            if data['list']:
                first_forecast_date = datetime.datetime.strptime(data['list'][0]['dt_txt'], '%Y-%m-%d %H:%M:%S').date()
            
            for forecast_entry in data['list']:
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
                    continue

                # For Monday (first day), store all time periods regardless of current time
                if date == first_forecast_date or date > datetime.date.today():
                    if time_period not in forecasts_by_date[date]:
                        forecasts_by_date[date][time_period] = {
                            'date': date,
                            'time_period': time_period,
                            'temp': forecast_entry['main']['temp'],
                            'description': forecast_entry['weather'][0]['description'],
                            'icon': forecast_entry['weather'][0]['icon']
                        }

            # If Monday morning is missing, use the first available forecast
            if first_forecast_date and 'morning' not in forecasts_by_date[first_forecast_date]:
                first_forecast = data['list'][0]
                forecasts_by_date[first_forecast_date]['morning'] = {
                    'date': first_forecast_date,
                    'time_period': 'morning',
                    'temp': first_forecast['main']['temp'],
                    'description': first_forecast['weather'][0]['description'],
                    'icon': first_forecast['weather'][0]['icon']
                }

            # Convert to sorted list of days with their forecasts
            forecast_days = []
            for date in sorted(forecasts_by_date.keys())[:5]:  # Limit to 5 days
                day_data = {
                    'date': date,
                    'morning': forecasts_by_date[date].get('morning'),
                    'midday': forecasts_by_date[date].get('midday'),
                    'night': forecasts_by_date[date].get('night')
                }
                forecast_days.append(day_data)

            context = {
                'forecast_days': forecast_days,
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
            context = {
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
                'temp': data['main']['temp'],
                'day': datetime.date.today(),
                'city': city
            }
        else:
            context = {
                'error': "City not found, please enter a valid city name.",
                'city': city
            }

    return render(request, 'index.html', context)