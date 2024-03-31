from nextbestcustomer.entities.Location import Location
from nextbestcustomer.entities.Route import Route
from nextbestcustomer.functional import AzureMapsAPI as Azure


# 1 User
class User:

    def __init__(self, mail, latitude, longitude):
        self.user_id = None
        self.routes = None
        self.location = Location(latitude, longitude, Azure.get_reverse_address(latitude, longitude))
        self.mail = mail

    def add_route(self, routes: list[Route]):
        self.routes = routes

    def add_id(self, user_id):
        self.user_id = user_id

    def add_location(self, location: Location):
        self.location = location

    def __str__(self):
        return f'Mail: {self.mail}, Location: {self.location}, ID: {self.user_id}, Route counts: {len(self.routes)}'
