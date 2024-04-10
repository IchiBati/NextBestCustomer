import azure.functions as func
import logging
import json
import pyodbc
from nextbestcustomer.functional.DatabaseConnector import DatabaseConnector
from nextbestcustomer.functional.EntityHandler import EntityHandler
from nextbestcustomer.functional.RequestValidator import (
    InvalidQueryParameter,
    InvalidRequestBody,
    RequestValidator
)
from nextbestcustomer.functional.HttpTriggerWorkload import HttpTriggerWorkload
from nextbestcustomer.functional import ErrorHandler
from nextbestcustomer.functional.Parser import Parser
from nextbestcustomer.entities.User import User
from nextbestcustomer.functional import AzureMapsAPI
import os


app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.route(route="userInput")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:

    logging.info("Python HTTP trigger function processed a request.")

    trigger_request = req

    validator = RequestValidator(trigger_request)

    try:
        validator.validate("query")
    except InvalidQueryParameter as ex:
        return func.HttpResponse(ex.args[0], status_code=400)

    try:
        validator.validate("body")
    except InvalidRequestBody as ex:
        return func.HttpResponse(ex.args[0], status_code=400)

    # query parameters of request
    query_params = trigger_request.params

    user_lat = query_params.get("lat")
    user_long = query_params.get("long")
    user_mail = query_params.get("mail")
    user_destinations = trigger_request.get_json()

    try:
        database = DatabaseConnector()
    except pyodbc.Error as ex:
        return func.HttpResponse(ex.args[1], status_code=500)

    poly = AzureMapsAPI.get_route_range_poly(user_lat, user_long, 10000)
    payload = HttpTriggerWorkload(user_destinations, user_lat, user_long, user_mail)
    user = User(payload.query_mail, payload.query_lat, payload.query_long)
    database.insert_user(user=user)

    # get user and customer objects of JSON Object (HTTP-Body)
    entity_parser = Parser(trigger_workload=payload)

    
    
    # functionality to prepare enitites for Azure Database insert
    # Routes are computed here by AzureMapsApi
    handler = EntityHandler(
        user=user,
        route_list=entity_parser.parse("route"),
        customer_list=entity_parser.parse("customer"),
    )

    database.insert_route(entities=handler)

    return func.HttpResponse("Test call passed", status_code=200)
