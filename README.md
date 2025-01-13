🌤️ Weather App
A simple weather forecast application that allows users to check the current weather and a 5-day forecast for any city worldwide.

🚀 Features
Current Weather: Displays the current temperature, weather description, and an icon representing the weather conditions.
5-Day Forecast: Provides a detailed 5-day weather forecast, including temperature, description, and weather icons for each day.
City Search: Users can search for weather information by entering the name of the city.
🛠️ How It Works
Backend:

Uses the OpenWeatherMap API to fetch weather data.
Two endpoints are used:
/weather for current weather.
/forecast for 5-day forecasts.
Data is processed and passed to the frontend using Django templates.
Frontend:

Built with Django templating.
Displays weather information in a user-friendly format.
Includes dynamic elements like search functionality and forecast cards.

🧑‍💻 Tech Stack
Backend: Django, Python
Frontend: HTML, CSS
API: OpenWeatherMap API

🔧 Setup and Usage
Clone the repository:
bash
Copy code
git clone <your-repo-url>
cd weather-app
Install dependencies:
bash
Copy code
pip install -r requirements.txt
Set up environment variables:
Create a .env file in the root directory.
Add your OpenWeatherMap API key:
makefile
Copy code
OPENWEATHER_API_KEY=your_api_key
Run the development server:
bash
Copy code
python manage.py runserver
Open the app in your browser at http://127.0.0.1:8000/.

🌟 How to Use
Enter the city name in the input field.
Click "Search city" to get the current weather.
Click "5-Day Forecast" to view the 5-day forecast for the city.
If the city is not found, an error message will be displayed.

📂 File Structure
views.py: Handles the logic for fetching weather data from the API and rendering templates.
index.html: Displays the current weather or forecast data to the user.
static/: Contains the CSS file for styling the app.
