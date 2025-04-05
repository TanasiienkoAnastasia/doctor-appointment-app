# 🏥 Doctor Appointment App

Мікросервісний додаток для запису до лікаря, створений на основі Flask, PostgreSQL і Docker. Реалізовано окремі сервіси для авторизації, користувачів, записів, медичних карток, розкладу, сповіщень та єдиний API Gateway.

---

## ⚙️ Технології
- Python + Flask
- PostgreSQL
- Docker + Docker Compose
- REST API
- Microservices architecture

---

## 🧱 Структура мікросервісів

| Сервіс                  | Порт  | Призначення                             |
|--------------------------|-------|------------------------------------------|
| `auth-service`           | 8000  | Авторизація, реєстрація, JWT токени     |
| `user-service`           | 8001  | Дані користувачів                        |
| `appointment-service`    | 8002  | Створення та перегляд записів           |
| `medical-records-service`| 8003  | Медичні записи пацієнтів                |
| `schedule-service`       | 8004  | Розклад лікарів                         |
| `notification-service`   | 8005  | Надсилання повідомлень (імітація)       |
| `gateway-service`        | 8080  | API шлюз — маршрути до всіх сервісів    |

---

## 🗄️ Бази даних (PostgreSQL)

Кожен сервіс має свою окрему базу:

- `authdb`, `userdb`, `appointmentdb`, `medicaldb`, `scheduledb`

---

## 🚀 Запуск проєкту

1. Клонування:
```bash
git clone https://github.com/your-username/doctor-appointment-app.git
cd doctor-appointment-app
