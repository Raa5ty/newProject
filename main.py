import requests
import json
from flask import Flask, Response

app = Flask(__name__)


def get_valutes_list():
    url = 'https://www.cbr-xml-daily.ru/daily_json.js'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверяем успешность запроса
        data = response.json()  # Используем встроенный метод json()
        valutes = list(data['Valute'].values())
        return valutes
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе данных: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"Ошибка при парсинге JSON: {e}")
        return []


def create_html(valutes):
    if not valutes:
        return "<h1>Нет данных о валютах</h1>"

    # Сортируем валюты по значению 'Value' в обратном порядке
    valutes_sorted = sorted(valutes, key=lambda x: x['Value'], reverse=True)

    text = '<h1>Курс валют</h1>'
    text += '<table>'
    text += '<tr>'
    for key in valutes_sorted[0].keys():
        text += f'<th>{key}</th>'
    text += '</tr>'
    for valute in valutes_sorted:
        text += '<tr>'
        for v in valute.values():
            text += f'<td>{v}</td>'
        text += '</tr>'
    text += '</table>'
    return text


@app.route("/")
def index():
    valutes = get_valutes_list()
    if not valutes:
        return Response("<h1>Не удалось получить данные о валютах</h1>", content_type='text/html')
    html = create_html(valutes)
    return Response(html, content_type='text/html; charset=utf-8')


if __name__ == "__main__":
    app.run(debug=True)


