from nextbestcustomer.entities.Customer import Customer


# N routes
class Route:

    def __init__(self, length_in_meters, travel_time_in_seconds, departure_time, arrival_time):
        self.route_id = None
        self.customer = None
        self.length_in_meters = length_in_meters
        self.travel_time_in_seconds = travel_time_in_seconds
        self.departure_time = departure_time
        self.arrival_time = arrival_time

    def set_route_id(self, route_id):
        self.route_id = route_id

    def set_customer(self, customer: Customer):
        self.customer = customer
