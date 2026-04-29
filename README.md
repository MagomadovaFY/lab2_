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
