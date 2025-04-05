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
```

2. Запуск усіх мікросервісів:
```bash
docker-compose up --build
```

3. Перевірка статусу:
```bash
docker ps
```

4. Веб-доступ:
- API Gateway: [http://localhost:8080](http://localhost:8080)
- Кожен сервіс також доступний на своїх портах

---

## 🧪 Тестування

Приклади запитів (curl/Postman):
```bash
curl http://localhost:8001/users
curl -X POST http://localhost:8000/login -d '{"username": "...", "password": "..."}'
```

---

## 📂 Структура проєкту

```
doctor-appointment-app/
├── auth-service/
├── user-service/
├── appointment-service/
├── medical-records-service/
├── schedule-service/
├── notification-service/
├── gateway/
├── docker-compose.yml
└── README.md
```

---

## 🔧 Наступні кроки

- [ ] Додати CI/CD (наприклад, GitHub Actions)
- [ ] Реалізувати логування (ELK, Grafana)
- [ ] Розділити frontend на мікрофронтенди (опційно)
- [ ] Додати Swagger-документацію

---

## 🔗 Посилання

- [GPTOnline.ai/ru](https://gptonline.ai/ru/) — AI-помічник для Python, Docker, мікросервісів (українською)
