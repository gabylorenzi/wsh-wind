import requests
import tweepy
from secrets import access_secret, access_token, secret, key, weather_key
from datetime import datetime

city_name = 'New York City'
url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={weather_key}&units=imperial"
response = requests.get(url)

now = datetime.now()
print(now.month,now.day)

def get_time():
    if 12 <= now.hour < 16:
        return "afternoon"
    elif now.hour >= 16:
        return "evening"
    else:
        return "morning"


class Weather():
    def __init__(self, city_name, response):
        self.city = city_name
        self.wind_speed = response.json()['wind']['speed']
        self.wind_deg = response.json()['wind']['deg']

        if 0 <= self.wind_deg <= 56.25:
            self.wind_dir = 'north'
        elif 300 <= self.wind_deg <= 348:
            self.wind_dir = 'north'
        elif 123 <= self.wind_deg <= 236:
            self.wind_dir = 'south'
        elif 236 < self.wind_deg < 300:
            self.wind_dir = 'west'
        else:
            self.wind_dir = 'east'


print(response.json())
nyc_weather = Weather(city_name, response)
print(nyc_weather.wind_speed)


def tweet_text(weather):
    time = get_time()

    if weather.wind_dir == 'north' and weather.wind_speed > 7:
        return f"{now.month}/{now.day}, {now.hour}:00. good {time}! {weather.wind_speed}mph wind currently, coming from the {weather.wind_dir}. you'll have more fun ripping it south on the WSH. (BETA)"
    elif weather.wind_dir == 'south' and weather.wind_speed > 7:
        return f"{now.month}/{now.day}, {now.hour}:00. good {time}! {weather.wind_speed}mph wind currently, coming from the {weather.wind_dir}. you'll have more fun ripping it north on the WSH. (BETA)"
    elif weather.wind_speed >= 7:
        return f"{now.month}/{now.day}, {now.hour}:00. good {time}! {weather.wind_speed}mph wind currently, coming from the {weather.wind_dir}, so no better direction to run, just generally windy. (BETA)"
    else:
        return f"{now.month}/{now.day}, {now.hour}:00. good {time}! {weather.wind_speed}mph wind currently, coming from the {weather.wind_dir}. the wind shouldn't impact your run. run wherever ur freakin heart desires (BETA)"


# Authenticate to Twitter
auth = tweepy.OAuthHandler(key, secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

tweet = tweet_text(nyc_weather)
api.update_status(tweet)
