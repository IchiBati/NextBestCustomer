
# N Locations
class Location:

    def __init__(self, lat, long, address):

        address_search_json = address

        self.latitude = lat
        self.longitude = long
        self.street = address_search_json.get('street')
        self.house_number = address_search_json.get('buildingNumber')
        self.zipcode = address_search_json.get('postalCode')
        self.city = address_search_json.get('municipality')
        self.district = address_search_json.get('municipalitySubdivision')
        self.state = address_search_json.get('countrySubdivision')
        self.country = address_search_json.get('country')
        self.freeFormAddressString = address_search_json.get('freeformAddress')

    def __str__(self):
        if self.freeFormAddressString is not None:
            return self.freeFormAddressString
        else:
            return "No address found"
