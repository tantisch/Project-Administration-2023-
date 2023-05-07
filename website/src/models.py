# DRIVER ----
from flask_login import UserMixin

from src import cursor


class Director:
    def __init__(self, director_id: int = -1, name: str = "", surname: str = "", surname2: str = "",
                 owner_id: int = -1):
        self.id = director_id
        self.name = name
        self.surname = surname
        self.surname2 = surname2
        self.owner_id = owner_id


class DirectorDatabase:
    db_cursor = cursor

    @staticmethod
    def get_director_by_user_id(user_id: int):
        sql_query = f"""
                    select director_id, name, surname, surname2, owner_id
                    from trolleybus_site_database.directors
                    join trolleybus_site_database.users u on u.user_id = directors.user_id
                    where directors.user_id = {user_id};
             """
        DirectorDatabase.db_cursor.execute(sql_query)

        # fields: director_id, name, surname, surname2, owner_id
        director_info = DirectorDatabase.db_cursor.fetchone()
        if director_info is None:
            return None

        return Director(*director_info)


class Driver:
    station_delimiter = "-"

    def __init__(self, driver_id: int = -1, name: str = "", surname: str = "", surname2: str = "",
                 stations: str = "", worked_hours: float = 0.0, rest_hours: float = 0.0, director_id: int = -1):
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
    def get_driver_by_driver_id(driver_id: int):
        sql_query = f"""
                    select driver_id, name, surname, surname2, stations, worked_hours, rest_hours, director_id
                    from trolleybus_site_database.drivers
                    join trolleybus_site_database.routes r on r.route_id = drivers.route_id
                    join trolleybus_site_database.users u on u.user_id = drivers.user_id
                    where drivers.driver_id = {driver_id};
                    """
        DriverDatabase.db_cursor.execute(sql_query)

        # fields: driver_id, name, surname, surname2, stations, worked_hours, rest_hours, director_id
        driver_info = DriverDatabase.db_cursor.fetchone()
        if driver_info is None:
            return None

        return Driver(*driver_info)

    @staticmethod
    def get_user_id_by_driver_id(driver_id: int) -> int:
        sql_query = f"""
                    select u.user_id
                    from trolleybus_site_database.drivers
                    join trolleybus_site_database.users u on u.user_id = drivers.user_id
                    where drivers.driver_id = {driver_id};
                    """
        DriverDatabase.db_cursor.execute(sql_query)

        driver_info = DriverDatabase.db_cursor.fetchone()
        return driver_info[0]


# USER ---------------
class User(UserMixin):
    # __slots__ = ["user_id", "user_email", "user_password", "role_id", "name", "surname", "surname2",
    #              "is_active", "is_authenticated"]

    def __init__(self, user_id: int = -1, role_id: int = 4, user_email: str = "", user_password: str = "",
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
    def get_user_by_id(user_id) -> User:
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
