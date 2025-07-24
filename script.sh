echo -e "\033[32m Начинаем запуск проекта...\033[0m"

# Сборка Docker-образов
echo -e "\033[34m Сборка образов...\033[0m"
docker-compose build

# Запуск контейнеров в фоновом режиме
echo -e "\033[34m Запуск контейнеров...\033[0m"
docker-compose up -d

sleep 10

# Выполнение миграций
echo -e "\033[34m Применение миграций...\033[0m"
docker-compose run --rm web-app sh -c "python manage.py migrate"

# Создание суперпользователя
echo -e "\033[34m Создание суперпользователя...\033[0m"
docker-compose run --rm web-app sh -c "python init_superuser.py"
