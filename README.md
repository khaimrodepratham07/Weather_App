# Weather App

A simple weather application built with Flask that shows current weather conditions for any city. The app uses the OpenWeatherMap API to fetch weather data and displays it with a dynamic background that changes based on weather conditions.

## Features

- Real-time weather information
- Dynamic background colors based on weather conditions
- Displays temperature, humidity, wind speed, and weather description
- Responsive design

## Setup

1. Clone the repository:
```bash
git clone <your-repository-url>
cd weather-app
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenWeatherMap API key:
- Get your API key from [OpenWeatherMap](https://openweathermap.org/api)
- Replace the `API_KEY` variable in `app.py` with your key

4. Run the application:
```bash
python app.py
```

## Environment Variables

Create a `.env` file in the root directory and add:
```
API_KEY=your_openweathermap_api_key
```

## Deployment

This app is configured for deployment on Vercel. To deploy:

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Deploy to Vercel:
```bash
vercel
```

## Technologies Used

- Python
- Flask
- OpenWeatherMap API
- HTML/CSS
- Vercel for deployment 