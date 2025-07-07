#!/bin/bash

# Wait for database
echo "Waiting for database..."
while ! pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER; do
  sleep 1
done
echo "Database ready!"

# Run migrations
echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser if it doesn't exist
echo "Creating superuser..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
# O valor do USERNAME_FIELD (cpf) deve ser o primeiro argumento posicional
if not User.objects.filter(cpf='00000000000').exists():
    User.objects.create_superuser(
        '00000000000', # <--- Adicione o CPF aqui como o primeiro argumento posicional
        email='admin@example.com', # email é um campo adicional que você pode querer no futuro
        name='Admin',
        password='admin123'
    )
    print('Superuser created')
else:
    print('Superuser already exists')
EOF

# Start server
echo "Starting server..."
python manage.py runserver 0.0.0.0:8000