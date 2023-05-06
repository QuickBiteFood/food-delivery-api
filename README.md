![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
## Простая Restfull API для системы доставки еды

> API создан для небольшого проекта и не создан для работы в реальных проектах

### :arrow_forward: Запуск

#### :triangular_flag_on_post: Зависимости
Перед запуском API необходимо установить все зависимости через `pip install -r requirements.txt`
> psycopg2 -> psycopg2-binary - linux
---

#### :arrow_lower_right: Миграции
Для миграции моделей в базу данных используется библиотека [Flask-Migrate](https://pypi.org/project/Flask-Migrate/).
> Если API запускается впервые в проекте не должно быть папки migrations

Инициализация миграции
```bash
flask db init
flask db migrate -m "init migrate"
flask db upgrade
```
---

#### :arrow_forward: Запуск Flask проекта
Несколько вариантов запуска ↓
```bash
flask run
flask run --host=0.0.0.0
flask run --host=0.0.0.0 --debug
```
---

### Планы
- [x] Рутинг еды
- [x] Рутинг сотрудников
- [x] Рутинг заказов
- [x] Полноценная система JWT токенов
