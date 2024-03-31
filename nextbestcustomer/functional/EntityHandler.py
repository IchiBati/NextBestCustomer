from nextbestcustomer.entities.Route import Route
from nextbestcustomer.entities.User import User
from nextbestcustomer.entities.Customer import Customer


class EntityHandler:

    def __init__(self, user: User, route_list: list[Route], customer_list: list[Customer]):
        self.computed_routes = None
        self.user = user
        self.routes = route_list
        self.customers = customer_list
        self._compute_entities()

    def _compute_entities(self):
        self._add_customer_to_route()
        self.user.add_route(self.routes)
        self.computed_routes = self._compute_route_list()

    def _add_customer_to_route(self):
        for route, customer in zip(self.routes, self.customers):
            route.customer = customer

    def _compute_route_list(self):
        computed_route_list = []
        user_route = self.user.routes
        for route in self.routes:
            route_customer = route.customer
            computed_route_list.append((self.user.user_id,
                                        route_customer.customer_id,
                                        route.length_in_meters,
                                        route.travel_time_in_seconds,
                                        route.departure_time,
                                        route.arrival_time))

        return computed_route_list
