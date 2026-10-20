import os
import requests
import datetime
from dotenv import load_dotenv

# 1. Загрузка секретного API-ключа из файла .env 
load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")

def log_request(endpoint, status_code):
    """Реализация логирования всех запросов (дата, эндпоинт, статус-код)."""
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{current_time}] LOG: Запрос к {endpoint} | Статус: {status_code}")

def get_weather(city: str) -> str:
    """Функция получения текущей погоды."""
    # Официальный эндпоинт OpenWeatherMap
    url = "https://api.openweathermap.org/data/2.5/weather"
    
    #Параметры запроса (город, ключ, метрическая система, русский язык)
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "ru"
    }
    
    try:
        # Отправляем GET-запрос к серверу
        response = requests.get(url, params=params, timeout=10)
        
        # Записываем лог запроса
        log_request("api.openweathermap.org/data/2.5/weather", response.status_code)
        
        # Если ответ успешный (Код 200)
        if response.status_code == 200:
            # JSON (превращаем текст из интернета в словарь)
            data = response.json()
            
            #  Извлекаем вложенные данные строго по названиям из методички
            temp = data["main"]["temp"]                       # извлекаем main.temp
            feels_like = data["main"]["feels_like"]           # извлекаем main.feels_like
            description = data["weather"][0]["description"]   # извлекаем weather[0].description
            wind_speed = data["wind"]["speed"]                # извлекаем wind.speed
            
            #  Красиво форматируем отображение знака плюс или минус для градусов
            temp_str = f"+{round(temp)}" if temp > 0 else str(round(temp))
            feels_str = f"+{round(feels_like)}" if feels_like > 0 else str(round(feels_like))
            
            # формирование итогового сообщения
            return f"В городе {city.capitalize()} сейчас {temp_str}°C, ощущается как {feels_str}°C. {description.capitalize()}. Ветер {wind_speed} м/с."
        
        # Если город не найден (Код 404)
        elif response.status_code == 404:
            return "Город не найден. Проверьте правильность написания."
        else:
            return f"Ошибка сервера погоды. Код ответа: {response.status_code}"
            
    except requests.exceptions.RequestException:
        # 3. Базовый try-except с выводом понятного сообщения пользователю
        return "Произошла ошибка при подключении к серверу погоды. Пожалуйста, попробуйте позже."

def main():
    print("=== Тестирование интеграции с погодным API ===")
    user_city = input("Введите название города: ").strip()
    
    if user_city:
        result = get_weather(user_city)
        print("\nОтвет бота:")
        print(result)

if __name__ == "__main__":
    main()
