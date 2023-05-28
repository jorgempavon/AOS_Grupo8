FROM mysql:8.0.33


ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=aos


COPY init.sql /docker-entrypoint-initdb.d/


RUN chmod 644 /docker-entrypoint-initdb.d/init.sql
