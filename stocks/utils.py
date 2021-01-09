from requests import get
from json import loads
from stocks.models import Stock, PaymentTrack
from django.db.models import F
from datetime import datetime, timedelta, timezone
from stock_quote_app.settings import YAHOO_SERVICE_URL


def create_or_update_object_and_increment_query_count(object_from_query: dict) -> Stock:
    """
    This method creates stock object and inserts it to the DB.
    In addition, it creates a counter (if not exist already) and
    increment its value
    """

    query_object, created = Stock.objects.update_or_create(
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
    payment_object, created = PaymentTrack.objects.get_or_create(id=1)
    payment_object.number_of_upstream_queries = F('number_of_upstream_queries') + 1
    payment_object.save()
    return query_object


def should_refresh_from_api(stock_object: Stock) -> bool:
    """
    This method validates whether a stock object should be refreshed or not, by the following terms:
        1. if trading_hours == True:
            a. if avg_daily_volume_10day >= 10M:
                if more than 10 minutes old -> return True (should refresh), else False
            b. if avg_daily_volume_10day < 10M:
                if more than 20 minutes old -> return True (should refresh), else False
        2. if more than one hour - > True else False
    """
    delta_time = datetime.now(tz=timezone.utc) - stock_object.update_time
    if stock_object.trading_hours:
        if stock_object.avg_daily_volume_10day >= 10000000:
            return delta_time > timedelta(minutes=10)
        else:
            return delta_time > timedelta(minutes=20)
    else:
        return delta_time > timedelta(hours=1)


def get_data_from_api_and_update_db(symbol: str) -> tuple:
    """
    This method sends a query given a symbol to the third party url, handle DB operations which are:
    1. update/ insert object - depends if the stock exists in DB or not
    2. increment query count

    return : tuple of : (Stock object or str representing error, status_code:int)
    """
    query_url = f'{YAHOO_SERVICE_URL}{symbol}'
    query_response = get(query_url)
    if query_response.status_code != 200:
        return f'Error on retrieving symbol from query {symbol}', query_response.status_code
    quote_response = loads(query_response.content)['quoteResponse']
    if not quote_response['result']:
        return f'Could not find Symbol {symbol}', 404
    stock_object = create_or_update_object_and_increment_query_count(quote_response['result'][0])
    return stock_object, 200


def encode_to_json(stock_object: Stock):
    """
    This method encodes the Stock object to json object with our desired keys.
    """
    return {key: getattr(stock_object, key) for key in
            ['symbol', 'update_time', 'exchange', 'short_name', 'price', 'currency', 'change_percent']}
