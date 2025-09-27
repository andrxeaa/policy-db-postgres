FROM postgres:15

# Copias tus scripts SQL de inicialización
COPY init/ /docker-entrypoint-initdb.d/

EXPOSE 5432