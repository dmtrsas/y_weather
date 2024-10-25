import requests
import csv
from datetime import datetime

locations = {"Msk": ["55.7512", "37.6184"], "Spb": ["59.9375", "30.3086"], "Kaz": ["55.7963", "49.1088"],
             "Tul": ["54.2048", "37.6184"], "Nsb": ["55.0188", "82.9339"]}  
header_key = {'X-Yandex-API-Key': '3288cf45-30c6-4dd0-8425-778dabf102ce'}  

with open('Weather_forecast_result.csv', 'w', newline='') as wfr:
    writer = csv.writer(wfr)
    header = ['city', 'date', 'hour', 'temperature_c', 'pressure_mm', 'is_rainy']
    writer.writerow(header)  

    for loc in locations:
        rsp = requests.get(
            f"https://api.weather.yandex.ru/v2/forecast?lat={locations[loc][0]}&lon={locations[loc][1]}&lang=ru_RU&limit=7&hours=true&extra=true",
            headers=header_key).json()  

        city = rsp['geo_object']['locality']['name']  
        for dt in rsp['forecasts']:  
            res_row = []
            if dt['hours']:  
                for hour in dt['hours']:  
                    res_row.append(city)  
                    res_row.append(datetime.strptime(dt['date'], "%Y-%m-%d").strftime(
                        "%d.%m.%Y"))  
                    res_row.append(hour['hour'])  
                    res_row.append(hour['temp'])  
                    res_row.append(hour['pressure_mm'])  
                    if hour['prec_type'] == 1 and hour['prec_strength'] > 0:  
                        res_row.append(1)  
                    else:
                        res_row.append(0)  
                    writer.writerow(res_row)  
                    res_row = []
            else:  
                continue
