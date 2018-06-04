from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError

import requests
import json
import os
import importlib.util

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("BackendMessage", BASE_DIR+'\common\BackendMessage.py')
common = importlib.util.module_from_spec(spec)
spec.loader.exec_module(common)

def index(request):

    template = loader.get_template('materials/index.html')
    context = {}
    return HttpResponse(template.render(context, request))
