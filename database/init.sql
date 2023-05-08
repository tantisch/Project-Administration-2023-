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
----------------------------------------------------------------





-- USERS
create table trolleybus_site_database.users
(
    user_id       integer               not null
        primary key,
    role_id       integer     default 4 not null
        constraint users_roles_null_fk
            references trolleybus_site_database.roles,
    user_email    varchar(64)           not null,
    user_password varchar(256)          not null,
    name          varchar(64) default '',
    surname       varchar(64) default '',
    surname2      varchar(64) default ''
);

create sequence trolleybus_site_database.users_seq
    increment 1
    start 1;

alter sequence trolleybus_site_database.users_seq cache 1;
----------------------------------------------------------------





-- OWNERS
create table trolleybus_site_database.owners
(
    owner_id  integer not null
        primary key,
    user_id   integer not null
        constraint owners_users_user_id_fk
            references trolleybus_site_database.users,
    is_active boolean default false

);

-- OWNERS SEQUENCE
drop sequence if exists trolleybus_site_database.owners_seq;

create sequence trolleybus_site_database.owners_seq
    increment 1
    start 1;

alter sequence trolleybus_site_database.owners_seq cache 1;


-- SET OWNER ROLE FUNCTION
create or replace function trolleybus_site_database.set_owner_role()
    returns trigger
    language plpgsql
as
$$
BEGIN
    -- set owner role
    if exists(SELECT * FROM trolleybus_site_database.owners WHERE user_id = new.user_id)
    then
        update trolleybus_site_database.owners set is_active = true where user_id = new.user_id;
    else
        insert into trolleybus_site_database.owners (owner_id, user_id, is_active)
        values (nextval('trolleybus_site_database.owners_seq'), new.user_id, true);
    end if;

    return new;
END;
$$;


-- UNSET OWNER ROLE FUNCTION
create or replace function trolleybus_site_database.unset_owner_role()
    returns trigger
    language plpgsql
as
$$
BEGIN
    --  unset owner role
    if exists(SELECT * FROM trolleybus_site_database.owners WHERE user_id = old.user_id)
    then
        update trolleybus_site_database.owners set is_active = false where user_id = old.user_id;
    end if;

    return new;
END;
$$;


-- TRIGGERS FOR USERS TO UPDATE ROLE TO owner
drop trigger if exists set_owner_role_trigger on trolleybus_site_database.users;

drop trigger if exists unset_owner_role_trigger on trolleybus_site_database.users;

create trigger set_owner_role_trigger
    after update
    on trolleybus_site_database.users
    for each row
    when (new.role_id = 1 and new.role_id != old.role_id)
execute procedure trolleybus_site_database.set_owner_role();

create trigger unset_owner_role_trigger
    after update
    on trolleybus_site_database.users
    for each row
    when (old.role_id = 1 and new.role_id != old.role_id)
execute procedure trolleybus_site_database.unset_owner_role();
----------------------------------------------------------------





-- DIRECTORS
create table trolleybus_site_database.directors
(
    director_id integer not null
        primary key,
    user_id     integer
        constraint directors_users_user_id_fk
            references trolleybus_site_database.users,
    is_active   boolean default false
);


-- DIRECTORS SEQUENCE
drop sequence if exists trolleybus_site_database.directors_seq;

create sequence trolleybus_site_database.directors_seq
    increment 1
    start 1;

alter sequence trolleybus_site_database.directors_seq cache 1;


-- SET DIRECTOR ROLE FUNCTION
create or replace function trolleybus_site_database.set_director_role()
    returns trigger
    language plpgsql
as
$$
BEGIN
    -- set director role
    if exists(SELECT * FROM trolleybus_site_database.directors WHERE user_id = new.user_id)
    then
        update trolleybus_site_database.directors set is_active = true where user_id = new.user_id;
    else
        insert into trolleybus_site_database.directors (director_id, user_id, is_active)
        values (nextval('trolleybus_site_database.directors_seq'), new.user_id, true);
    end if;

    return new;
END;
$$;


-- UNSET director ROLE FUNCTION
create or replace function trolleybus_site_database.unset_director_role()
    returns trigger
    language plpgsql
as
$$
BEGIN
    --  unset director role
    if exists(SELECT * FROM trolleybus_site_database.directors WHERE user_id = old.user_id)
    then
        update trolleybus_site_database.directors set is_active = false where user_id = old.user_id;
    end if;

    return new;
END;
$$;


-- TRIGGERS FOR USERS TO UPDATE ROLE TO DIRECTOR
drop trigger if exists set_director_role_trigger on trolleybus_site_database.users;

drop trigger if exists unset_director_role_trigger on trolleybus_site_database.users;

create trigger set_director_role_trigger
    after update
    on trolleybus_site_database.users
    for each row
    when (new.role_id = 2 and new.role_id != old.role_id)
execute procedure trolleybus_site_database.set_director_role();

create trigger unset_director_role_trigger
    after update
    on trolleybus_site_database.users
    for each row
    when (old.role_id = 2 and new.role_id != old.role_id)
execute procedure trolleybus_site_database.unset_director_role();
----------------------------------------------------------------





-- ROUTES
create table trolleybus_site_database.routes
(
    route_id integer not null
        primary key,
    stations varchar
);

insert into trolleybus_site_database.routes (route_id, stations)
values (-1, '');

insert into trolleybus_site_database.routes (route_id, stations)
values (0, 'A-B-C-D-E-F-G-H-I-J-K-L-M-N-O-P');

insert into trolleybus_site_database.routes (route_id, stations)
values (1, 'L-E-N-I-G-J-M-B-O-F-K-C-H-D-A-P');

insert into trolleybus_site_database.routes (route_id, stations)
values (2, 'F-L-E-K-A-M-H-P-J-O-B-C-D-N-G-I');

insert into trolleybus_site_database.routes (route_id, stations)
values (3, 'B-C-K-F-A-O-N-E-H-P-D-L-I-G-M-J');

insert into trolleybus_site_database.routes (route_id, stations)
values (4, 'N-J-H-A-E-F-L-G-P-K-D-M-O-I-C-B');

----------------------------------------------------------------





-- DRIVERS
create table trolleybus_site_database.drivers
(
    driver_id    integer not null
        primary key,
    user_id      integer not null
        constraint drivers_users_null_fk
            references trolleybus_site_database.users,
    worked_hours float default 0.0,
    rest_hours   float default 0.0,
    route_id     integer default -1
        constraint drivers_routes_null_fk
            references trolleybus_site_database.routes,
    director_id  integer
        constraint drivers_directors_null_fk
            references trolleybus_site_database.directors,
    is_active    boolean default false
);


-- DRIVERS SEQUENCE
drop sequence if exists trolleybus_site_database.drivers_seq;

create sequence trolleybus_site_database.drivers_seq
    increment 1
    start 1;

alter sequence trolleybus_site_database.drivers_seq cache 1;


-- SET DRIVER ROLE FUNCTION
create or replace function trolleybus_site_database.set_driver_role()
    returns trigger
    language plpgsql
as
$$
BEGIN
    -- set driver role
    if exists(SELECT * FROM trolleybus_site_database.drivers WHERE user_id = new.user_id)
    then
        update trolleybus_site_database.drivers set is_active = true where user_id = new.user_id;
    else
        insert into trolleybus_site_database.drivers (driver_id, user_id, is_active)
        values (nextval('trolleybus_site_database.drivers_seq'), new.user_id, true);
    end if;

    return new;
END;
$$;


-- UNSET DRIVER ROLE FUNCTION
create or replace function trolleybus_site_database.unset_driver_role()
    returns trigger
    language plpgsql
as
$$
BEGIN
    --  unset driver role
    if exists(SELECT * FROM trolleybus_site_database.drivers WHERE user_id = old.user_id)
    then
        update trolleybus_site_database.drivers set is_active = false where user_id = old.user_id;
    end if;

    return new;
END;
$$;


-- TRIGGERS FOR USERS TO UPDATE ROLE TO DRIVER
drop trigger if exists set_driver_role_trigger on trolleybus_site_database.users;

drop trigger if exists unset_driver_role_trigger on trolleybus_site_database.users;

create trigger set_driver_role_trigger
    after update
    on trolleybus_site_database.users
    for each row
    when (new.role_id = 3 and new.role_id != old.role_id)
execute procedure trolleybus_site_database.set_driver_role();

create trigger unset_driver_role_trigger
    after update
    on trolleybus_site_database.users
    for each row
    when (old.role_id = 3 and new.role_id != old.role_id)
execute procedure trolleybus_site_database.unset_driver_role();
----------------------------------------------------------------





-- TEST USERS CREATION
insert into trolleybus_site_database.users (user_id, user_email, user_password, name, surname, surname2)
values (-1, 'chel1@gmail.com', '12345', 'chel1_name', 'chel1_surname', 'chel1_surname2');


insert into trolleybus_site_database.users (user_id, role_id, user_email, user_password, name, surname, surname2)
values (-2, 4, 'chel2@gmail.com', '12345', 'chel2_name', 'chel2_surname', 'chel2_surname2');
----------------------------------------------------------------





-- ADD OWNERS
insert into trolleybus_site_database.users (user_id, role_id, user_email, user_password, name, surname, surname2)
values (-3, 1, 'user', '123', 'user_name', 'user_surname', 'user_surname2');

insert into trolleybus_site_database.owners (owner_id, user_id, is_active)
values (-1, -3, true);


insert into trolleybus_site_database.users (user_id, role_id, user_email, user_password, name, surname, surname2)
values (-4, 1, 'judge', '123', 'judge_name', 'judge_surname',
        'judge_surname2');

insert into trolleybus_site_database.owners (owner_id, user_id, is_active)
values (-2, -4, true);
----------------------------------------------------------------





-- ADD DIRECTORS

insert into trolleybus_site_database.users (user_id, role_id, user_email, user_password, name, surname, surname2)
values (-5, 2, 'director1', '123', 'director1_name', 'director1_surname', 'director1_surname2');

insert into trolleybus_site_database.directors (director_id, user_id, is_active)
values (-1, -5, true);


insert into trolleybus_site_database.users (user_id, role_id, user_email, user_password, name, surname, surname2)
values (-6, 2, 'director2', '123', 'director2_name', 'director2_surname', 'director2_surname2');

insert into trolleybus_site_database.directors (director_id, user_id, is_active)
values (-2, -6, true);
----------------------------------------------------------------





-- ADD DRIVERS
do
$$
    declare
        director_id_ int;
    begin
        for i in 1..10
            loop
                if (i % 2) = 0
                then
                    director_id_ = -1;
                else
                    director_id_ = -2;
                end if;

                insert into trolleybus_site_database.users (user_id, role_id, user_email, user_password, name, surname, surname2)
                values (-6 - i, 3, 'driver' || i, '123',
                        'driver' || i || '_name',
                        'driver' || i || '_surname',
                        'driver' || i || '_surname2');

                insert into trolleybus_site_database.drivers (driver_id, route_id, user_id, worked_hours, rest_hours,
                                                              director_id, is_active)
                values (-i,
                        -1 + floor(5 * random()),
                        -6 - i,
                        round((8 * random())::numeric, 1),
                        round((4 * random())::numeric, 1),
                        director_id_,
                        true);
            end loop;
    end
$$;
----------------------------------------------------------------





-- ADD NO-ROLE ACCOUNTS
do
$$
    begin
        for i in 1..10
            loop
                insert into trolleybus_site_database.users (user_id, role_id, user_email, user_password, name, surname, surname2)
                values (-16 - i, 4, 'user' || i, '123',
                        'user' || i || '_name',
                        'user' || i || '_surname',
                        'user' || i || '_surname2');
            end loop;
    end
$$;
----------------------------------------------------------------


commit;