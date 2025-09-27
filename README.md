# 📦 Base de Datos – Primac  

Este repo contiene la definición de la **base de datos PostgreSQL**, junto con los scripts de inicialización (`schemas.sql`, `seed.sql`) y configuración de Docker para correr tanto en **entorno local** como en **AWS**.  

---

## 📂 Estructura del repo

```
├── init/ # Archivos de inicialización para PostgreSQL
│ ├── schemas.sql # Definición de tablas
│ ├── seed.sql # Datos de ejemplo (generados con Faker)
│ └── generate_seed.py # Script para generar seed.sql automáticamente
├── Dockerfile # Imagen personalizada de Postgres (si aplica)
├── docker-compose.dev.yml
├── docker-compose.prod.yml
└── README.md
```
---

## 🚀 Correr en Local

### 1️⃣ Generar `seed.sql` (opcional)
Si quieres poblar la DB con datos falsos usando **Faker**, ejecuta:

```
python3 init/generate_seed.py
```
Esto creará o sobrescribirá `init/seed.sql` con inserciones agrupadas.

### 2️⃣ Levantar contenedor en local

Usa el ``docker-compose.dev.yml``:
```
docker compose -f docker-compose.dev.yml up -d --build
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
python3 init/generate_seed.py
```
Sube tu imagen de DB a ECR:
```
docker build -t mydb -f Dockerfile .
docker tag mydb:latest <aws_account_id>.dkr.ecr.<region>.amazonaws.com/mydb:latest
docker push <aws_account_id>.dkr.ecr.<region>.amazonaws.com/mydb:latest
```
Configura el servicio en ECS/EC2 usando ``docker-compose.prod.yml`` o directamente en la Task Definition.

### 2. Opción B: DB en RDS
Crea una instancia PostgreSQL en RDS.

Desde tu máquina local o un pipeline CI/CD, corre los scripts:
```
psql -h <rds-endpoint> -U <user> -d <dbname> -f init/schemas.sql
psql -h <rds-endpoint> -U <user> -d <dbname> -f init/seed.sql
```
No necesitas contenedor en AWS, solo tu RDS + ejecución de scripts.

## ⚙️ Archivos importantes
``docker-compose.dev.yml``
```
version: "3.9"

services:
  db:
    image: postgres:15
    container_name: db_dev
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: mydb
    volumes:
      - ./init:/docker-entrypoint-initdb.d
    ports:
      - "5432:5432"
```

``docker-compose.prod.yml``
```
version: "3.9"

services:
  db:
    image: <aws_account_id>.dkr.ecr.<region>.amazonaws.com/mydb:latest
    container_name: db_prod
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    ports:
      - "5432:5432"
```
## 🛠 Tips importantes
Todo archivo dentro de ``/init/`` se ejecuta automáticamente al crear el contenedor (solo si la DB está vacía).

Si corres varias veces los scripts, podrías duplicar datos → por eso el seed.sql se genera limpio cada vez.

Para performance, las inserciones se agrupan en un único ``INSERT ... VALUES (...), (...), ....``

- En local → usas docker-compose.dev.yml.
- En AWS → decides:
    - usar RDS y correr scripts, o
    - subir la imagen con DB inicializada a ECS/EC2.