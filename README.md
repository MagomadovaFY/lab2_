# Лабораторная работа №2

**Тема:** Проектирование и реализация клиент-серверной системы. HTTP, веб-серверы и RESTful веб-сервисы

**Вариант №11**

**Студент:** Фирюза Магомадова

---

## Цель работы

Изучить методы отправки и анализа HTTP-запросов, освоить базовую настройку HTTP-сервера nginx в качестве обратного прокси, изучить и применить на практике концепции REST для создания веб-сервисов (API) на языке Python.

---

## Часть 1. HTTP-анализ (t.me)

### Задание
Проанализировать ответ сервера t.me, проверить редирект.

### Команда
```bash
curl -v http://t.me

```
### Вывод
```bash
* Host t.me:80 was resolved.
* Connected to t.me (149.154.167.99) port 80
> GET / HTTP/1.1
> Host: t.me
> User-Agent: curl/8.6.0
> Accept: */*
>
< HTTP/1.1 301 Moved Permanently
< Server: nginx/1.18.0
< Date: Wed, 29 Apr 2026 01:20:49 GMT
< Content-Type: text/html
< Content-Length: 169
< Connection: keep-alive
< Location: https://t.me/
<
<html>
<head><title>301 Moved Permanently</title></head>

```
### Анализ
Сервер t.me вернул код состояния 301 Moved Permanently и заголовок Location: https://t.me/. Это означает, что ресурс постоянно перемещен на защищенную версию (HTTPS). Браузер или клиент должен автоматически выполнить перенаправление по новому адресу.

### Часть 2. Разработка REST API "Пользователи системы"

### Сущность
```bash
{
  "id": 1,
  "username": "ivanov",
  "email": "ivanov@example.com"
}
```
### Эндпоинты
Метод	Эндпоинт	Описание
GET	/api/users	Получить список всех пользователей
GET	/api/users/{id}	Получить одного пользователя по ID
POST	/api/users	Создать нового пользователя

### Листинг кода (app.py)
```bash
from flask import Flask, jsonify, request

app = Flask(__name__)

users = [
    {"id": 1, "username": "ivanov", "email": "ivanov@example.com"},
    {"id": 2, "username": "petrova", "email": "petrova@example.com"}
]
next_id = 3

@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify({"users": users})

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((u for u in users if u["id"] == user_id), None)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)

@app.route('/api/users', methods=['POST'])
def create_user():
    global next_id
    data = request.json
    if not data or not data.get("username") or not data.get("email"):
        return jsonify({"error": "username and email are required"}), 400
    new_user = {
        "id": next_id,
        "username": data["username"],
        "email": data["email"]
    }
    users.append(new_user)
    next_id += 1
    return jsonify(new_user), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
```
### Запуск приложения
```bash
cd ~/lab_02/users_api
source venv/bin/activate
python3 app.py
```
### Результат
* Running on http://127.0.0.1:5002

### Часть 3. Настройка Nginx
## Конфигурация Nginx (файл nginx.conf)
```bash
server {
    listen 8080;
    server_name localhost;

    location /api/ {
        proxy_pass http://127.0.0.1:5002;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```
***Примечание по выполнению***
В ходе работы на macOS возникли технические сложности с запуском Nginx в качестве обратного прокси (конфликт портов с системным сервисом AirPlay Receiver). Представленная выше конфигурация является рабочей и была бы применена при развертывании на сервере под управлением Linux. Тестирование API выполнялось напрямую через Flask.

### Часть 4. Тестирование API
## Тест 1. GET /api/users (список пользователей)

```bash
curl -s http://127.0.0.1:5002/api/users | jq
```
## Результат
```bash
{
  "users": [
    {
      "id": 1,
      "username": "ivanov",
      "email": "ivanov@example.com"
    },
    {
      "id": 2,
      "username": "petrova",
      "email": "petrova@example.com"
    }
  ]
}
```
## Тест 2. GET /api/users/1 (один пользователь)
```bash
curl -s http://127.0.0.1:5002/api/users/1 | jq
```
## Результат:
```bash
{
  "id": 1,
  "username": "ivanov",
  "email": "ivanov@example.com"
}
```
## Тест 3. POST /api/users (создание пользователя)
```bash
curl -X POST http://127.0.0.1:5002/api/users \
  -H "Content-Type: application/json" \
  -d '{"username": "sidorov", "email": "sidorov@mail.ru"}' | jq
```
## Результат:
```bash
{
  "id": 3,
  "username": "sidorov",
  "email": "sidorov@mail.ru"
}
```
### Тест 4. Проверка, что пользователь добавился
```bash
curl -s http://127.0.0.1:5002/api/users | jq

```
### Результат
```bash
{
  "users": [
    {
      "id": 1,
      "username": "ivanov",
      "email": "ivanov@example.com"
    },
    {
      "id": 2,
      "username": "petrova",
      "email": "petrova@example.com"
    },
    {
      "id": 3,
      "username": "sidorov",
      "email": "sidorov@mail.ru"
    }
  ]
}
```
### Тест 5. GET /api/users/999 (ошибка 404)
```bash
curl -s http://127.0.0.1:5002/api/users/999 | jq

```
## Результат
```bash
{
  "error": "User not found"
}

```
***Выводы***
В ходе выполнения лабораторной работы:

Проанализирован HTTP-трафик с помощью утилиты curl. На примере сайта t.me изучен механизм редиректа с HTTP на HTTPS (код 301).

Создан RESTful API на Python с использованием фреймворка Flask. Реализованы основные операции: получение списка, получение одного элемента, создание нового элемента.

Составлена конфигурация Nginx для проксирования запросов к Flask-приложению.

Проведено тестирование всех эндпоинтов API, результаты проверены с помощью утилиты jq.

### Полученные навыки:
Работа с сетевыми утилитами curl, jq

Анализ HTTP-заголовков и кодов состояния

Разработка REST API на Flask

Настройка виртуального окружения Python

Конфигурирование Nginx в качестве обратного прокси

Документирование выполненной работы в формате README

