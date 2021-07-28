FROM mysql/mysql-server:latest
EXPOSE 3306
ENV MYSQL_ROOT_HOST=%
ENV MYSQL_ROOT_PASSWORD=password
RUN mkdir /work
WORKDIR /work
COPY init_db.sql /docker-entrypoint-initdb.d
