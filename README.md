Doctor Appointment App
Проєкт реалізований у вигляді мікросервісної архітектури, що дозволяє ефективно управляти пацієнтами, лікарями, записами, медичними даними та сповіщеннями.

Архітектура
Проєкт складається з таких мікросервісів:

(auth-service, 8000, Реєстрація, логін, JWT авторизація),
(user-service, 8001, Дані про користувачів (пацієнти, лікарі)), 
(appointment-service, 8002, Створення та управління записами), 
(medical-records-service, 8003, Зберігання медичних карток), 
(schedule-service, 8004, Розклади лікарів), 
(notification-service, 8005, Виведення повідомлень, імітація сповіщень), 
(gateway-service, 8080, Центральна точка доступу до всіх API)

user-service
Створення, оновлення, перегляд користувачів

Ролі: лікар, пацієнт, адміністратор

appointment-service
Створення записів на прийом

Фільтрація за статусами: scheduled, completed, cancelled

medical-records-service
Медичні записи та історія

Прив’язка до patient_id, doctor_id

schedule-service
Розклад прийомів лікарів по днях

Інтервали часу: start_time, end_time

notification-service
Імітація надсилання повідомлень (email/SMS)

Приймає POST-запити через /notify

gateway-service
Проксі маршрути до всіх сервісів

Єдина точка входу на фронтенді
