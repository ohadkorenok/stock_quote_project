from requests import get
from json import loads
from stocks.models import Query, PaymentTrack
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.models import F
from datetime import datetime, timedelta, timezone

import os


def retrieve_from_query(symbol_to_retrieve: str) -> dict:
    """
    This method gets a symbol to retrieve and retrieves the data from the query.
    """
    query_url_prefix = os.environ.get("YAHOO_SERVICE_URL")
    query_url = f'{query_url_prefix}{symbol_to_retrieve}'
    query_response = get(query_url)
    if query_response.status_code != 200:
        return {'result': f'Error on retrieving symbol from query {symbol_to_retrieve}',
                'status': query_response.status_code}
    quote_dict = loads(query_response.content)['quoteResponse']
    if not quote_dict['result']:
        return {'result': f'Could not find Symbol {symbol_to_retrieve}', 'status': 404}
    return {'result': quote_dict['result'], 'status': 200}


def create_or_update_object_and_increment_query_count(object_from_query: dict) -> Query:
    """
    This method creates object and inserts it to the DB.In additon, it creates a counter (if not exist already) and
     increment its value"""

    query_object, created = Query.objects.update_or_create(
        symbol=object_from_query['symbol'],
        defaults={'exchange': object_from_query.get('exchange', ''),
                  'short_name': object_from_query.get('shortName', ''),
                  'price': object_from_query.get('regularMarketPrice', 0),
                  'currency': object_from_query.get('currency', 'USD'),
                  'change_percent': object_from_query.get('regularMarketChangePercent', 0),
                  'avg_daily_volume_10day': object_from_query.get('averageDailyVolume10Day', 0),
                  'update_time': datetime.now(tz=timezone.utc),
                  'trading_hours': True if object_from_query['marketState'] == 'REGULAR' else False}
    )
    payment_row = PaymentTrack.objects.get_or_create(payment_track_id=1)[0]
    payment_row.number_of_upstream_queries = F('number_of_upstream_queries') + 1
    payment_row.save()
    return query_object


def should_refresh(query_object: Query) -> bool:
    """
    This method validates whether a query object should be refreshed or not, by the following terms:
        1. if trading_hours == True:
            a. if avg_daily_volume_10day >= 10M:
                if more than 10 minutes old -> return True (should refresh), else False
            b. if avg_daily_volume_10day < 10M:
                if more than 20 minutes old -> return True (should refresh), else False
        2. if more than one hour - > True else False
    """
    delta_time = datetime.now(tz=timezone.utc) - query_object.update_time
    if query_object.trading_hours:
        if query_object.avg_daily_volume_10day >= 10000000:
            return delta_time > timedelta(minutes=10)
        else:
            return delta_time > timedelta(minutes=20)
    else:
        return delta_time > timedelta(hours=1)


def handle_query(symbol: str) -> dict:
    """This method sends a query given a symbol to the third party url, handle DB operations and return a dict with the
    dict created object """
    response_object = retrieve_from_query(symbol)
    if response_object['status'] != 200:
        return response_object  # {result:...,status:...}
    query_object = create_or_update_object_and_increment_query_count(response_object['result'][0])
    return {'result': query_object.to_dict(), 'status': 200}


def reset_counter():
    payment_row = PaymentTrack.objects.get_or_create(payment_track_id=1)[0]
    payment_row.number_of_upstream_queries = 0
    payment_row.save()


def format_message(message, status_code):
    return {'result': message, 'status': status_code}
