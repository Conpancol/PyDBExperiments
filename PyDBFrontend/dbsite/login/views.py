from django.template import loader
from django.shortcuts import render
from django.http import HttpResponse

from .forms import UserForm

import json
import requests
import jwt

from common.BackendMessage import BackendMessage


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

                backend_message = BackendMessage(json.loads(r.text))
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

