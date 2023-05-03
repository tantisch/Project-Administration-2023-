create schema trolleybus_site_database;


-- ROLES
create table trolleybus_site_database.roles
(
    role_id   int primary key,
    role_name varchar(64)
);

insert into trolleybus_site_database.roles(role_id, role_name)
values (1, 'owner');
insert into trolleybus_site_database.roles(role_id, role_name)
values (2, 'director');
insert into trolleybus_site_database.roles(role_id, role_name)
values (3, 'driver');
insert into trolleybus_site_database.roles(role_id, role_name)
values (4, 'no-role');

commit;

-- USERS
create table trolleybus_site_database.users
(
    user_id       integer               not null
        primary key,
    role_id       integer     default 4 not null
        constraint users_roles_null_fk
            references trolleybus_site_database.roles,
    user_email    varchar(64)           not null,
    user_password varchar(256)           not null,
    name          varchar(64) default '',
    surname       varchar(64) default '',
    surname2      varchar(64) default ''
);

create sequence trolleybus_site_database.users_seq
    increment 1
    start 1;

alter sequence trolleybus_site_database.users_seq cache 1;


insert into trolleybus_site_database.users (user_id, user_email, user_password)
values (nextval('trolleybus_site_database.users_seq'), 'chel2@gmail.com', '12345');


insert into trolleybus_site_database.users (user_id, role_id, user_email, user_password)
values (-1, 4, 'chel-1@gmail.com', '12345');

commit;


-- DRIVERS
create table trolleybus_site_database.drivers
(
    driver_id    integer not null
        primary key,
    user_id      integer not null
        constraint drivers_users_null_fk
            references trolleybus_site_database.users,
    worked_hours integer,
    rest_hours   integer
);



-- DIRECTORS
create table trolleybus_site_database.directors
(
    director_id            integer not null
        primary key,
    director_user_id       integer
        constraint directors_users_user_id_fk
            references trolleybus_site_database.users,
    subordinated_driver_id integer
        constraint directors_drivers_null_fk
            references trolleybus_site_database.drivers
);


-- OWNERS
create table trolleybus_site_database.owners
(
    owner_id                 integer not null
        primary key,
    owner_user_id            integer not null
        constraint owners_users_user_id_fk
            references trolleybus_site_database.users,
    subordinated_director_id integer
        constraint owners_directors_null_fk
            references trolleybus_site_database.directors
);

commit;