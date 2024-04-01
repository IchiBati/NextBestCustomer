from nextbestcustomer.entities.Customer import Customer
from nextbestcustomer.entities.Route import Route
from nextbestcustomer.entities.Location import Location
from nextbestcustomer.functional import AzureMapsAPI
from nextbestcustomer.functional.ApiDataFormatter import ApiDataFormatter
from nextbestcustomer.functional.HttpTriggerWorkload import HttpTriggerWorkload


class Parser:

    def __init__(self, trigger_workload: HttpTriggerWorkload):
        self.trigger_workload = trigger_workload

    def parse(self, entity: str):
        parser = _get_parser(entity, self.trigger_workload)
        return parser


def _get_parser(entity: str, trigger_workload: HttpTriggerWorkload):
    if entity == 'route':
        return _route_deserializer(trigger_workload)
    elif entity == 'customer':
        return _customer_deserializer(trigger_workload)
    elif entity == 'locations':
        return _create_locations_from_coordinates(trigger_workload)


def _route_deserializer(trigger_workload: HttpTriggerWorkload):
    latitude = trigger_workload.query_lat
    longitude = trigger_workload.query_long
    customers = trigger_workload.http_body
    customers_geojson = ApiDataFormatter.format_data("geojson", customers, latitude, longitude)
    route_json = AzureMapsAPI.post_routematrix_http(latitude, longitude, customers_geojson)
    route_obj_list = list()
    for routes in route_json['matrix'][0]:
        route_summary = routes['response']['routeSummary']
        route_obj_list.append(Route(
            route_summary['lengthInMeters'],
            route_summary['travelTimeInSeconds'],
            route_summary['departureTime'],
            route_summary['arrivalTime']
        ))
    return route_obj_list


def _customer_deserializer(trigger_workload: HttpTriggerWorkload):
    customer_json = trigger_workload.http_body
    customer_obj_list = list()
    customer_locations = _create_locations_from_coordinates(customer_json)
    for customer, location in zip(customer_json, customer_locations):
        customer_obj_list.append(Customer(
            customer['pharmacy_id'],
            location
        ))
    return customer_obj_list


def _create_locations_from_coordinates(powerbi_customer_data):
    api_batch_items = ApiDataFormatter.format_data("batchItems", powerbi_customer_data)
    api_addresses = AzureMapsAPI.get_reverse_address_batch(api_batch_items)
    locations_obj_list = list()

    for address, coord in zip(api_addresses, powerbi_customer_data):

        if address['statusCode'] == 200:
            address_item = address['response']['addresses'][0]['address']
            locations_obj_list.append(Location(coord['latitude'], coord['longitude'], address_item))
        else:
            continue

    return locations_obj_list
