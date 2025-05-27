from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

API_KEY = os.getenv("API_KEY", "020620cbefcece7fbd238337f8543d78")  # Use environment variable, fallback to existing key

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
    weather = None
    bg_color = "skyblue"  # Default background color (sunny)

    if request.method == "POST":
        city = request.form.get("city")
        if city:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            try:
                response = requests.get(url)
                data = response.json()

                if data["cod"] == 200:
                    condition = data["weather"][0]["main"]
                    bg_color = weather_bg_colors.get(condition, "skyblue")  # Default to skyblue if not found
                    
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
                else:
                    weather = {"error": f"City '{city}' not found."}
            except requests.exceptions.RequestException:
                weather = {"error": "Network error occurred. Please try again."}

    return render_template("index.html", weather=weather, bg_color=bg_color)


if __name__ == "__main__":
    app.run(debug=True)
