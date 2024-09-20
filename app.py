import requests

def location(ip_address):
    url = f"http://ip-api.com/json/{ip_address}?fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,offset,currency,isp,org,as,asname,mobile,proxy,hosting"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if data.get('status') != 'success':
            return f"Не удалось определить информацию для IP {ip_address}. Сообщение: {data.get('message', 'Неизвестная ошибка')}"

        fields = [
            ('Континент', 'continent'),
            ('Код континента', 'continentCode'),
            ('Страна', 'country'),
            ('Код страны', 'countryCode'),
            ('Регион', 'region'),
            ('Название региона', 'regionName'),
            ('Город', 'city'),
            ('Район', 'district'),
            ('Почтовый индекс', 'zip'),
            ('Широта', 'lat'),
            ('Долгота', 'lon'),
            ('Часовой пояс', 'timezone'),
            ('Смещение', 'offset'),
            ('Валюта', 'currency'),
            ('ISP', 'isp'),
            ('Организация', 'org'),
            ('AS', 'as'),
            ('AS name', 'asname'),
            ('Мобильное соединение', 'mobile', lambda x: 'Да' if x else 'Нет'),
            ('Прокси', 'proxy', lambda x: 'Да' if x else 'Нет'),
            ('Хостинг', 'hosting', lambda x: 'Да' if x else 'Нет'),
        ]

        # Формируем результат
        result = f"Информация о IP {ip_address}:\n"
        for label, key, *formatter in fields:
            value = data.get(key, 'Н/Д')
            if formatter:
                value = formatter[0](value)
            result += f"{label}: {value}\n"
        return result

    except requests.RequestException as e:
        return f"Ошибка при выполнении запроса: {e}"


# Валидация ввода IP-адреса
def is_valid_ip(ip):
    ip = ip.strip()
    parts = ip.split(".")
    return len(parts) == 4 and all(item.isdigit() and 0 <= int(item) <= 255 for item in parts)


if __name__ == "__main__":
    while True:
        ip_address = input("Введите IP-адрес (или 'q' для завершения): ").strip()

        if ip_address.lower() == 'q':
            print("Программа завершена.")
            break

        if not is_valid_ip(ip_address):
            print("Некорректный IP-адрес. Попробуйте снова.")
            continue

        print(location(ip_address))
