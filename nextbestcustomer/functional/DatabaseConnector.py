
from nextbestcustomer.functional.EntityHandler import EntityHandler
from nextbestcustomer.functional.LocalCredentials import sql_connection_string as connection_string
from nextbestcustomer.entities.User import User
import pyodbc
import os




class DatabaseConnector:
    def __init__(self):
        self.connection = pyodbc.connect(os.environ["sql_connection_string"])
        

    def _delete_user(self, cursor, user: User):
        cursor.execute("DELETE FROM func.[user] WHERE email = ?", user.mail)

    def insert_user(self, user: User):
        cursor = self.connection.cursor()
        self._delete_user(cursor, user)

        last_id_cursor = cursor.execute(
            "INSERT INTO func.[user] (email, latitude, longitude) OUTPUT INSERTED.user_id VALUES(?, ?, ?)",
            (user.mail, user.location.latitude, user.location.longitude)).fetchone()

        user.user_id = last_id_cursor[0]

        self.connection.commit()

    def _delete_route(self, cursor, entities: EntityHandler):
        cursor.execute("DELETE FROM func.[computed_route] WHERE user_id = ?", entities.user.user_id)

    def insert_route(self, entities: EntityHandler):
        insert_route_cursor = self.connection.cursor()
        self._delete_route(insert_route_cursor, entities)
        insert_string = ("INSERT INTO func.[computed_route] (user_id, destination_id, lengthInMeters, "
                         "travelTimeInSeconds, departureTime, arrivalTime) values (?, ?, ?, ?, ?, ?)")
        insert_route_cursor.fast_executemany = True
        insert_route_cursor.executemany(insert_string, entities.computed_routes)
        self.connection.commit()
        self.connection.close()
