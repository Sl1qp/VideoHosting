# VideoHosting

## Запуск
### Создание контейнера:
```docker-compose build```
### Миграции: 
```docker-compose run --rm web-app sh -c "python manage.py makemigrations"``` 
и
```docker-compose run --rm web-app sh -c "python manage.py migrate"```
### Создание суперпользователя:
```docker-compose run --rm web-app sh -c "python manage.py createsuperuser"```
### Создание тестовых данных:
```docker-compose run --rm web-app sh -c "python create_test_data.py"```

## Админ панель:
```http://127.0.0.1:8000/admin/```

## Аутентификация

#### Отправить Post-запрос на ```http://127.0.0.1:8000/token/``` со следующим боди (JSON):
```{"username": "ваш_логин", "password": "ваш_пароль"}```
### При следующих обращениях к api указывать в headers: 
```Key: Authorization```
```Value: Token ваш_токен```
