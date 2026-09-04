# Configuración para Google Cloud / PostgreSQL

## 1) Variables de entorno
Crea un archivo `.env` con este contenido:

```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=bodega_db
DB_USER=postgres
DB_PASSWORD=tu_password_real
DB_HOST=localhost
DB_PORT=5432
USE_SQLITE=0
```

Si usas Cloud SQL, cambia `DB_HOST` por la IP privada o socket correspondiente, no por `localhost`.

## 2) Cargar variables al iniciar la app
En Google Cloud, puedes definir estas variables en la configuración del servicio.

## 3) Migraciones
```bash
python manage.py migrate
```

## 4) Crear usuario admin
```bash
python manage.py createsuperuser
```

## 5) Probar login
Usa el usuario creado y su contraseña.
