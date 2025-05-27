from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Get API key from environment variable
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    logger.error("No API_KEY environment variable set")
    raise ValueError("No API_KEY environment variable set. Please set it in Vercel dashboard.")

# Map weather conditions to background colors
weather_bg_colors = {
    "Clear": "skyblue",   # Sunny
    "Rain": "grey",       # Rainy
    "Clouds": "lightgray", # Cloudy
    "Snow": "lightblue",  # Snowy
    "Thunderstorm": "darkgray", # Stormy
}

@app.route("/", methods=["GET", "POST"])
def index():
    try:
        weather = None
        bg_color = "skyblue"  # Default background color (sunny)

        if request.method == "POST":
            city = request.form.get("city")
            if not city:
                return render_template("index.html", weather={"error": "Please enter a city name"}, bg_color=bg_color)

            logger.info(f"Fetching weather data for city: {city}")
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()  # Raise an exception for bad status codes
                data = response.json()

                if data.get("cod") == 200:
                    condition = data["weather"][0]["main"]
                    bg_color = weather_bg_colors.get(condition, "skyblue")
                    
                    weather = {
                        "city": data["name"],
                        "temperature": data["main"]["temp"],
                        "description": data["weather"][0]["description"].title(),
                        "humidity": data["main"]["humidity"],
                        "wind": data["wind"]["speed"],
                        "icon": data["weather"][0]["icon"],
                        "main": data["weather"][0]["main"],
                        "bg_color": bg_color,
                    }
                    logger.info(f"Successfully fetched weather data for {city}")
                else:
                    error_message = data.get("message", f"City '{city}' not found.")
                    logger.error(f"API Error: {error_message}")
                    weather = {"error": error_message}
            
            except requests.exceptions.RequestException as e:
                logger.error(f"Network error occurred: {str(e)}")
                weather = {"error": f"Network error occurred: {str(e)}"}
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
                weather = {"error": f"An unexpected error occurred: {str(e)}"}

        return render_template("index.html", weather=weather, bg_color=bg_color)
    
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.errorhandler(404)
def not_found_error(error):
    return render_template("index.html", weather={"error": "Page not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template("index.html", weather={"error": "Internal server error"}), 500

# Vercel requires the app to be named 'app'
app.debug = False

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
