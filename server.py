from flask import Flask, render_template
import public_ip as ip
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
WeatherApiKey = os.getenv("WEATHER_API_KEY")
api_key = os.getenv("API_KEY")


@app.route('/')
def hello_world():
    params = {
       'api_key': api_key,
       'ip_address': ip.get()
   }
    try:
        response = requests.get(f"https://ipgeolocation.abstractapi.com/v1/?api_key={api_key}&ip_address={ip.get()}")
        City = json.loads(response.content.decode('utf-8'))['city']

    except requests.exceptions.RequestException as api_error:
        print(f"There was an error contacting the Geolocation API: {api_error}")
        raise SystemExit(api_error)
    try:
        response = requests.get(f"http://dataservice.accuweather.com/locations/v1/cities/ipaddress?apikey={WeatherApiKey}&q={ip.get()}")
        my_dict = json.loads(response.content.decode('utf-8'))
        weather = requests.get(f"http://dataservice.accuweather.com/forecasts/v1/daily/5day/{my_dict['Key']}?apikey={WeatherApiKey}&metric=true")
        data = json.loads(weather.content.decode('utf-8'))
        x=""
        Date=[]
        Minimum=[]
        Maximum=[]
        IconPhrase=[]
        for key1 in data["DailyForecasts"]:
            Date.append(key1['Date'])
            Minimum.append(key1['Temperature']['Minimum']['Value'])
            Maximum.append(key1['Temperature']['Maximum']['Value'])
            IconPhrase.append(key1['Day']['IconPhrase'])
        return render_template('index.html',Date=Date,Minimum=Minimum,Maximum=Maximum,IconPhrase=IconPhrase,City=City)
    except requests.exceptions.RequestException as api_error:
        print(f"There was an error contacting the Accuweather API: {api_error}")
        raise SystemExit(api_error)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
