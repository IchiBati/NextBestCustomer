import geojson


class ApiDataFormatter:

    @staticmethod
    def format_data(target_format, input_data, input_lat=0, input_lon=0):
        formatter = _get_formatter(target_format, input_data, input_lat, input_lon)
        return formatter


def _get_formatter(target_format, input_data, input_lat=0, input_lon=0):
    if target_format == "geojson":
        return _format_to_geojson(input_data, input_lat, input_lon)
    elif target_format == "batchItems":
        return _format_to_address_reverse(input_data)


def _format_to_geojson(input_data, input_lat, input_lon):
    geojson_template = {"origins": {}, "destinations": {}}
    multipoint_origin = geojson.MultiPoint([(float(input_lon), float(input_lat))])
    destination_coords = [
        (float(i["longitude"]), float(i["latitude"])) for i in input_data
    ]
    multipoint_dest = geojson.MultiPoint(destination_coords)
    geojson_template["origins"] = multipoint_origin
    geojson_template["destinations"] = multipoint_dest
    return geojson_template


def _format_to_address_reverse(input_data: list):
    coordinates_list = input_data
    api_template = dict()
    item_array = []
    for coordinate in coordinates_list:
        item = {"query": f"?query={coordinate['latitude']},{coordinate['longitude']}"}
        item_array.append(item)
    api_template["batchItems"] = item_array
    return api_template
