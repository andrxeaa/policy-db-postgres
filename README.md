# 📦 Base de Datos – Primac  

Este repo contiene la definición de la **base de datos PostgreSQL**, junto con los scripts de inicialización (`schemas.sql`, `seed.sql`) y configuración de Docker para correr tanto en **entorno local** como en **AWS**.  

---

## 📂 Estructura del repo

```
├── init/ # Archivos de inicialización para PostgreSQL
│ ├── schemas.sql # Definición de tablas
│ └── seed.sql # Datos de ejemplo (generados con Faker)
├── Dockerfile # Imagen personalizada de Postgres (si aplica)
├── generate_seed.py # Script para generar seed.sql automáticamente
├── docker-compose.yml
├── requirements.txt
└── README.md
```
---

## 🚀 Correr en Local

### 1️⃣ Generar `seed.sql` (opcional)
Si quieres poblar la DB con datos falsos usando **Faker**, ejecuta:

```
python3 generate_seed.py
```
Esto creará o sobrescribirá `init/seed.sql` con inserciones agrupadas.

### 2️⃣ Levantar contenedor en local

Usa el ``docker-compose.yml``:
```
docker compose -f docker-compose.yml up -d --build
```
Esto:

- Crea un contenedor con PostgreSQL.
- Ejecuta automáticamente los archivos de init/ (``schemas.sql`` y ``seed.sql``).

### 📌 Para conectarte:
```
psql -h localhost -U postgres -d mydb
```
(la contraseña debe estar definida en un ``.env.dev``).

## 🌐 Deploy en AWS (Producción)
En AWS ECS / EC2 / RDS puedes usar dos enfoques:
### 1. Opción A: DB en contenedor (ECS o EC2)
Genera seed.sql localmente:
```
python3 generate_seed.py
```
Sube tu imagen de DB a ECR:
```
docker build -t mydb -f Dockerfile .
docker tag mydb:latest <aws_account_id>.dkr.ecr.<region>.amazonaws.com/mydb:latest
docker push <aws_account_id>.dkr.ecr.<region>.amazonaws.com/mydb:latest
```
Configura el servicio en ECS/EC2 usando ``docker-compose.yml`` o directamente en la Task Definition.

## ⚙️ Archivos importantes
``docker-compose.yml``
```
version: '3.8'
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
      POSTGRES_DB: policydb
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
      - ./init:/docker-entrypoint-initdb.d  # aquí metes schema.sql y seed.sql

volumes:
  pgdata:
```

## 🛠 Tips importantes
Todo archivo dentro de ``/init/`` se ejecuta automáticamente al crear el contenedor (solo si la DB está vacía).

Si corres varias veces los scripts, podrías duplicar datos → por eso el seed.sql se genera limpio cada vez.

Para performance, las inserciones se agrupan en un único ``INSERT ... VALUES (...), (...), ....``

- En local → usas docker-compose.dev.yml.
- En AWS → decides:
    - usar RDS y correr scripts, o
    - subir la imagen con DB inicializada a ECS/EC2.