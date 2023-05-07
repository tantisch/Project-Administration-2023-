# DRIVER ----
from typing import List

from flask_login import UserMixin

from src import cursor


class Owner:
    def __init__(self, owner_id: int = -1, name: str = "", surname: str = "", surname2: str = ""):
        self.id = owner_id
        self.name = name
        self.surname = surname
        self.surname2 = surname2


class OwnerDatabase:
    db_cursor = cursor

    @staticmethod
    def get_owner_by_user_id(user_id: int):
        sql_query = f"""
                    select owner_id, name, surname, surname2
                    from trolleybus_site_database.owners
                    join trolleybus_site_database.users u on u.user_id = owners.user_id
                    where owners.is_active = true and owners.user_id = {user_id};
             """
        OwnerDatabase.db_cursor.execute(sql_query)

        # fields:owner_id, name, surname, surname2
        owner_info = OwnerDatabase.db_cursor.fetchone()
        if owner_info is None:
            return None

        return Owner(*owner_info)


class Director:
    def __init__(self, director_id: int = -1, name: str = "", surname: str = "", surname2: str = ""):
        self.id = director_id
        self.name = name
        self.surname = surname
        self.surname2 = surname2


class DirectorDatabase:
    db_cursor = cursor

    @staticmethod
    def get_user_id_by_director_id(director_id: int) -> int:
        sql_query = f"""
                    select user_id
                    from trolleybus_site_database.directors
                    where directors.is_active = true and directors.director_id = {director_id};
                    """
        DirectorDatabase.db_cursor.execute(sql_query)
        director_info = DirectorDatabase.db_cursor.fetchone()
        if director_info is None:
            return None

        return director_info[0]

    @staticmethod
    def get_director_by_user_id(user_id: int):
        sql_query = f"""
                    select director_id, name, surname, surname2
                    from trolleybus_site_database.directors
                    join trolleybus_site_database.users u on u.user_id = directors.user_id
                    where directors.is_active = true and directors.user_id = {user_id};
             """
        DirectorDatabase.db_cursor.execute(sql_query)

        # fields: director_id, name, surname, surname2
        director_info = DirectorDatabase.db_cursor.fetchone()
        if director_info is None:
            return None

        return Director(*director_info)

    @staticmethod
    def get_director_by_director_id(director_id: int):
        sql_query = f"""
                        select director_id, name, surname, surname2
                        from trolleybus_site_database.directors
                        join trolleybus_site_database.users u on u.user_id = directors.user_id
                        where directors.is_active = true and directors.director_id = {director_id};
                 """
        DirectorDatabase.db_cursor.execute(sql_query)

        # fields: director_id, name, surname, surname2
        director_info = DirectorDatabase.db_cursor.fetchone()
        if director_info is None:
            return None

        return Director(*director_info)

    @staticmethod
    def get_drivers_by_director_id(director_id: int):
        sql_query = f"""
                    select driver_id, name, surname, surname2
                    from trolleybus_site_database.drivers
                    join trolleybus_site_database.users u on u.user_id = drivers.user_id
                    where drivers.is_active = true and drivers.director_id = {director_id};
                    """
        DirectorDatabase.db_cursor.execute(sql_query)

        # fields: driver_id, name, surname, surname2
        drivers_info = DirectorDatabase.db_cursor.fetchall()
        if drivers_info is None:
            return None

        drivers = []
        for driver_info in drivers_info:
            drivers.append(Driver(*driver_info))
        return drivers

    @staticmethod
    def get_all_directors() -> List[Director]:
        sql_query = f"""
                    select director_id, name, surname, surname2
                    from trolleybus_site_database.directors
                    join trolleybus_site_database.users u on u.user_id = directors.user_id
                    where is_active = true;
                    """
        DriverDatabase.db_cursor.execute(sql_query)
        directors: List[Director] = [Director(*director_info) for director_info in DriverDatabase.db_cursor.fetchall()]
        return directors


class Driver:
    station_delimiter = "-"

    def __init__(self, driver_id: int = None, name: str = None, surname: str = None, surname2: str = None,
                 stations: str = None, worked_hours: float = 0.0, rest_hours: float = 0.0, director_id: int = None):
        self.id = driver_id
        self.name = name
        self.surname = surname
        self.surname2 = surname2
        self.stations = stations
        self.worked_hours = worked_hours
        self.rest_hours = rest_hours
        self.director_id = director_id


class DriverDatabase:
    db_cursor = cursor

    @staticmethod
    def get_user_id_by_driver_id(driver_id: int) -> int:
        sql_query = f"""
                    select user_id
                    from trolleybus_site_database.drivers
                    where drivers.is_active = true and drivers.driver_id = {driver_id};
                    """
        DriverDatabase.db_cursor.execute(sql_query)
        driver_info = DriverDatabase.db_cursor.fetchone()
        if driver_info is None:
            return None

        return driver_info[0]

    @staticmethod
    def get_driver_by_driver_id(driver_id: int):
        sql_query = f"""
                    select driver_id, name, surname, surname2, stations, worked_hours, rest_hours, director_id
                    from trolleybus_site_database.drivers
                    join trolleybus_site_database.routes r on r.route_id = drivers.route_id
                    join trolleybus_site_database.users u on u.user_id = drivers.user_id
                    where drivers.is_active = true and drivers.driver_id = {driver_id};
                    """
        DriverDatabase.db_cursor.execute(sql_query)

        # fields: driver_id, name, surname, surname2, stations, worked_hours, rest_hours, director_id
        driver_info = DriverDatabase.db_cursor.fetchone()
        if driver_info is None:
            return None

        return Driver(*driver_info)

    @staticmethod
    def get_driver_by_user_id(user_id: int):
        sql_query = f"""
                        select driver_id, name, surname, surname2, stations, worked_hours, rest_hours, director_id
                        from trolleybus_site_database.drivers
                        join trolleybus_site_database.routes r on r.route_id = drivers.route_id
                        join trolleybus_site_database.users u on u.user_id = drivers.user_id
                        where drivers.is_active = true and drivers.user_id = {user_id};
                        """
        DriverDatabase.db_cursor.execute(sql_query)

        # fields: driver_id, name, surname, surname2, stations, worked_hours, rest_hours, director_id
        driver_info = DriverDatabase.db_cursor.fetchone()
        if driver_info is None:
            return None

        return Driver(*driver_info)

    @staticmethod
    def set_director_id_by_driver_id(director_id: int, driver_id: int):
        sql_query = f"""
                    update trolleybus_site_database.drivers
                    set director_id = {director_id}
                    where drivers.is_active = true and driver_id = {driver_id};
                    """
        DriverDatabase.db_cursor.execute(sql_query)
        DriverDatabase.db_cursor.execute("commit;")

    @staticmethod
    def set_worked_hours_by_driver_id(worked_hours: float, driver_id: int):
        sql_query = f"""
                    update trolleybus_site_database.drivers
                    set worked_hours = {worked_hours}
                    where drivers.is_active = true and driver_id = {driver_id};
                    """
        DriverDatabase.db_cursor.execute(sql_query)
        DriverDatabase.db_cursor.execute("commit;")

    @staticmethod
    def set_rest_hours_by_driver_id(rest_hours: float, driver_id: int):
        sql_query = f"""
                    update trolleybus_site_database.drivers
                    set rest_hours = {rest_hours}
                    where drivers.is_active = true and driver_id = {driver_id};
                    """
        DriverDatabase.db_cursor.execute(sql_query)
        DriverDatabase.db_cursor.execute("commit;")

    @staticmethod
    def set_route_id_by_driver_id(route_id: int, driver_id: int):
        sql_query = f"""
                            update trolleybus_site_database.drivers
                            set route_id = {route_id}
                            where drivers.is_active = true and driver_id = {driver_id};
                            """
        DriverDatabase.db_cursor.execute(sql_query)
        DriverDatabase.db_cursor.execute("commit;")


# USER ---------------
class User(UserMixin):
    # __slots__ = ["user_id", "user_email", "user_password", "role_id", "name", "surname", "surname2",
    #              "is_active", "is_authenticated"]

    def __init__(self, user_id: int = None, role_id: int = None, user_email: str = None, user_password: str = None,
                 name: str = "", surname: str = "", surname2: str = ""):
        """

        :param user_id:
        :param role_id: 1-'owner', 2-'director', 3-'driver', 4-'no-role'
        :param user_email:
        :param user_password:
        :param name:
        :param surname:
        :param surname2:
        """
        self.id = user_id
        self.role_id = role_id
        self.email = user_email
        self.password = user_password
        self.name = name
        self.surname = surname
        self.surname2 = surname2


class UserDatabase:
    db_cursor = cursor

    @staticmethod
    def add_user(user_email, user_password, role_id=4, name="", surname="", surname2=""):
        sql_query = f"""
                    insert into trolleybus_site_database.users (user_id, user_email, user_password, 
                    role_id, name, surname, surname2)
                    values (nextval('trolleybus_site_database.users_seq'), '{user_email}', 
                    '{user_password}', {role_id}, 
                    '{name}', '{surname}', '{surname2}');
                    """

        try:
            UserDatabase.db_cursor.execute(sql_query)
            UserDatabase.db_cursor.execute("commit;")
        except Exception as e:
            UserDatabase.db_cursor.execute("commit;")
            raise e

    @staticmethod
    def get_user_by_email(user_email) -> User:
        sql_query = f"""
                    select *
                    from trolleybus_site_database.users
                    where trolleybus_site_database.users.user_email = '{user_email}';
                    """

        UserDatabase.db_cursor.execute(sql_query)
        user_info = UserDatabase.db_cursor.fetchone()

        if user_info is not None:
            user = User(*user_info)
        else:
            user = None
        return user

    @staticmethod
    def get_user_by_user_id(user_id: int) -> User:
        sql_query = f"""
                    select *
                    from trolleybus_site_database.users
                    where trolleybus_site_database.users.user_id = {user_id};
                    """

        UserDatabase.db_cursor.execute(sql_query)
        user_info = cursor.fetchone()

        if user_info is not None:
            user = User(*user_info)
        else:
            user = None
        return user

    @staticmethod
    def get_all_no_role_users() -> List[User]:
        sql_query = f"""
                    select user_id, role_id, name, surname, surname2
                    from trolleybus_site_database.users
                    where role_id = 4;
                    """
        UserDatabase.db_cursor.execute(sql_query)

        users = []
        # fields: user_id, role_id, name, surname, surname2
        for user_info in UserDatabase.db_cursor.fetchall():
            users.append(User(user_id=user_info[0], role_id=user_info[1],
                              name=user_info[2], surname=user_info[3], surname2=user_info[4]))

        return users

    @staticmethod
    def grant_driver_role_by_user_id(user_id: int):
        sql_query = f"""
                    update trolleybus_site_database.users
                    set role_id = 3
                    where user_id = {user_id};
                    """
        UserDatabase.db_cursor.execute(sql_query)
        UserDatabase.db_cursor.execute("commit;")

    @staticmethod
    def grant_director_role_by_user_id(user_id: int):
        sql_query = f"""
                            update trolleybus_site_database.users
                            set role_id = 2
                            where user_id = {user_id};
                            """
        UserDatabase.db_cursor.execute(sql_query)
        UserDatabase.db_cursor.execute("commit;")

    @staticmethod
    def grant_owner_role_by_user_id(user_id: int):
        sql_query = f"""
                                update trolleybus_site_database.users
                                set role_id = 1
                                where user_id = {user_id};
                                """
        UserDatabase.db_cursor.execute(sql_query)
        UserDatabase.db_cursor.execute("commit;")

    @staticmethod
    def take_away_role_by_user_id(user_id: int):
        sql_query = f"""
                    update trolleybus_site_database.users
                    set role_id = 4
                    where user_id = {user_id};
                    """
        UserDatabase.db_cursor.execute(sql_query)
        UserDatabase.db_cursor.execute("commit;")
