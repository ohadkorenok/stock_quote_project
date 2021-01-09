from django.urls import path, re_path

from . import views

# FIXME: fix regex url path
urlpatterns = [
    path(r'reset_cost', views.reset_cost, name='reset_cost'),
    path(r'total_cost', views.query_total_cost, name='query_total_cost'),
    re_path(r'(?P<symbol>\w+)', views.get_data_from_symbol, name='index')

]
