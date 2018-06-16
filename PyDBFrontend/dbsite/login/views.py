from django.template import loader
from django.shortcuts import render
from django.http import HttpResponse

from .forms import UserForm

import json
import os
import importlib.util
import requests
import jwt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("BackendMessage", BASE_DIR+'\common\BackendMessage.py')
common = importlib.util.module_from_spec(spec)
spec.loader.exec_module(common)


def simple_login(request):

    try:
        if request.method == 'POST':
            form = UserForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                passwd = form.cleaned_data['password']

                result = {"username": username, "password": passwd}
                print(json.dumps(result))

                r = requests.post('http://localhost:4568/auth/login/', json=result)

                backend_message = common.BackendMessage(json.loads(r.text))
                print(backend_message)

            return render(request, 'login/simple_login.html', {'form': form})
        else:
            form = UserForm()
            return render(request, 'login/simple_login.html', {'form': form})

    except Exception as ex:
        print(ex)
        template = loader.get_template('login/simple_login.html')
        context = {}
        return HttpResponse(template.render(context, request))

