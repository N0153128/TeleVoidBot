import python_weather

import asyncio
import os

async def getweather():
  # declare the client. the measuring unit used defaults to the metric system (celcius, km/h, etc.)
  async with python_weather.Client(unit=python_weather.METRIC) as client:
    # fetch a weather forecast from a city
    weather = await client.get('St Neots')
    
    # returns the current day's forecast temperature (int)
    print(f'temp: {weather.temperature}')
    print(f'date and time: {weather.datetime}')
    print(f'feels like: {weather.feels_like}')
    print(f'kind: {weather.kind}')
    print(f'unit: {weather.unit}')
    print(f'wind speed: {weather.wind_speed}')
    print(f'visibility: {weather.visibility}')
  

    # # get the weather forecast for a few days
    # for daily in weather.daily_forecasts:
    #   print(daily)
      
    #   # hourly forecasts
    #   for hourly in daily.hourly_forecasts:
    #     print(f' --> {hourly!r}')

if __name__ == '__main__':
  # see https://stackoverflow.com/questions/45600579/asyncio-event-loop-is-closed-when-getting-loop
  # for more details
  if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
  
  asyncio.run(getweather())