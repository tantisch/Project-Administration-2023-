# Project-Administration-2023-
Управління проектами (2023)

## Docker
### Website
To build docker image use command: "docker build -t trolleybus_site ."

To run docker image use command: "docker run --name trolleybus_site -it -p 5000:5000 trolleybus_site"

### Database
To run docker image use command: "docker run -p 5433:5433 --name vertica vertica/vertica-ce"

Then switch to different console to succeed with further steps.

To access database inside docker container use command: "docker exec -it vertica /opt/vertica/bin/vsql"

To create schema inside database use command: "create schema trolleybus_site_database;"

To create table inside schema use command: 
"create table trolleybus_site_database.users
(
    user_id int primary key,
    user_email    varchar(64),
    user_password varchar(64)
);"

To create sequence inside schema use command: "create sequence trolleybus_site_database.users_seq;"
