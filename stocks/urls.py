from django.urls import path, re_path

from . import views

# FIXME: fix regex url path
urlpatterns = [
    path(r'reset', views.reset, name='reset'),
    path(r'total_cost', views.get_total_cost, name='total_cost'),
    re_path(r'(?P<symbol>\w+)', views.symbol, name='index')

]
