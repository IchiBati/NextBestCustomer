
class HttpTriggerWorkload:

    def __init__(self, http_body_json, http_query_lat, http_query_long, http_query_mail):
        self.http_body = http_body_json
        self.query_lat = http_query_lat
        self.query_long = http_query_long
        self.query_mail = http_query_mail
