from nextbestcustomer.entities.Location import Location


# N Customer
class Customer:
    def __init__(self, customer_id, customer_location):
        self.customer_id = customer_id
        self.customer_location = customer_location

    def set_location(self, location: Location):
        self.customer_location = location
