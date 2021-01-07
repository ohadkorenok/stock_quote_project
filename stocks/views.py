from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    ohad = "ohad"
    return HttpResponse('hi')
