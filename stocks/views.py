from stocks.models import Stock, PaymentTrack
from stocks.utils import should_refresh_from_api, get_data_from_api_and_update_db, encode_to_json
from django.http import JsonResponse
from ratelimit.decorators import ratelimit


@ratelimit(key='ip', rate='10/m', method=['GET'])
def get_data_from_symbol(request, symbol: str):
    """
    This method gets a symbol GET request represents the stock , checks whether it's on our DB and if not, queries
    data from Yahoo API, and update the DB (also a query counter).

    At the end, it returns a JSON with the relevant stock data to the user.
    """
    was_limited = getattr(request, 'limited', False)
    if was_limited:
        return JsonResponse({'result': 'Error! too many requests per minute!'}, status=429)
    stock_filter = Stock.objects.filter(symbol=symbol.upper())

    if stock_filter.count() == 1:
        stock_object = stock_filter.first()
        should_refresh_query = should_refresh_from_api(stock_object)
        if not should_refresh_query:
            return JsonResponse({'result': encode_to_json(stock_object)}, status=200)

    result, status = get_data_from_api_and_update_db(symbol)
    if status != 200:  # Given an error
        return JsonResponse({'result': result}, status=status)

    return JsonResponse({'result': encode_to_json(result)}, status=status)


def reset_cost(request):
    """
    This view gets a GET request and resets the query counter in the DB.
    """
    payment_object, created = PaymentTrack.objects.update_or_create(id=1, defaults={'number_of_upstream_queries': 0})
    return JsonResponse({'result': 'success'}, status=200)


def query_total_cost(request):
    """
    This method gets the total cost of the queries since the last counter reset.
    Notice we use get or create for maintaining one row every time.
    """
    payment_object, created = PaymentTrack.objects.get_or_create()
    return JsonResponse({'result': payment_object.query_cost * payment_object.number_of_upstream_queries}, status=200)
