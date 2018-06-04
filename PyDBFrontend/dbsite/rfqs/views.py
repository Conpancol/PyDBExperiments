from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.core.files.storage import FileSystemStorage

from .services.RFQCreator import RFQCreator
from .forms import RFQForm

import requests
import json
import os
import importlib.util

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("BackendMessage", BASE_DIR+'\common\BackendMessage.py')
common = importlib.util.module_from_spec(spec)
spec.loader.exec_module(common)


def cleanup(filename):
    try:
        os.remove('.' + filename)
        print("removed file: " + filename)
    except Exception as error:
        print(error)


def index(request):

    template = loader.get_template('rfqs/index.html')
    context = {}
    return HttpResponse(template.render(context, request))


def rfq_upload(request):
    try:
        if request.method == 'POST':
            form = RFQForm(request.POST, request.FILES)
            if form.is_valid():

                rfq = RFQCreator()

                internal_code = form.cleaned_data['internalCode']
                external_code = form.cleaned_data['externalCode']
                sender = form.cleaned_data['sender']
                company = form.cleaned_data['company']
                received_date = form.cleaned_data['receivedDate']
                note = form.cleaned_data['note']

                rfq.setRFQInformation(internal_code, external_code, sender, company, received_date)
                rfq.addRFQNote(note)

                myfile = request.FILES['document']
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                uploaded_file_url = fs.url(filename)

                result = rfq.createRFQfromCSV('.' + uploaded_file_url)

                print(json.dumps(result))

                r = requests.post('http://localhost:4567/auth/rfqs/', json=result)

                backend_message = common.BackendMessage(json.loads(r.text))
                print(backend_message)

                cleanup(uploaded_file_url)

                return render(request, 'rfqs/rfq_upload.html', {'form': form, 'error_message': backend_message.getValue()})
        else:
            form = RFQForm()
        return render(request, 'rfqs/rfq_upload.html', {'form': form})

    except Exception as error:
        print(error)

