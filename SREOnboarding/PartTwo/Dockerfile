FROM mysql/mysql-server:latest
ENV MYSQL_ROOT_HOST=%
ENV MYSQL_ROOT_PASSWORD=password
RUN mkdir /work
WORKDIR /work
COPY init_db.sql /docker-entrypoint-initdb.d
