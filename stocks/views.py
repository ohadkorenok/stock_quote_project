from stocks.models import Query, PaymentTrack
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from stocks.utils import should_refresh, handle_query, reset_counter, format_message
from django.http import JsonResponse


def symbol(request, symbol):  # FIXME:: if the stock is not in the query... Should we save it too?
    try:
        query_object = Query.objects.get(symbol=symbol.upper())
        query_object_dict = query_object.to_dict()
        should_refresh_query = should_refresh(query_object)
        if should_refresh_query:
            result = handle_query(query_object.symbol)
        else:
            result = format_message(query_object_dict, 200)

    except MultipleObjectsReturned as e:
        result = format_message('Error! Multiple objects returned', 500)

    except ObjectDoesNotExist as e:
        result = handle_query(symbol)

    return JsonResponse(result)


def reset(request):
    try:
        reset_counter()
        result = format_message('success', 200)
    except Exception as e:
        result = format_message('Error ! Could not reset the counter!', 500)
    return JsonResponse(result)


def get_total_cost(request):
    try:
        payment_row = PaymentTrack.objects.get_or_create(payment_track_id=1)[0]
        result = format_message(payment_row.query_cost * payment_row.number_of_upstream_queries, 200)
    except Exception as e:
        result = format_message("error in getting the total cost! ", 500)
    return JsonResponse(result)
