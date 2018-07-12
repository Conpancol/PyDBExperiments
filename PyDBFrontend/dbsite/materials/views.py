from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError

from .services.MaterialCreator import MaterialCreator

import requests
import json
import os

from common.BackendMessage import BackendMessage


def cleanup(filename):
    try:
        os.remove('.' + filename)
        print("removed file: " + filename)
    except Exception as error:
        print(error)


def index(request):

    template = loader.get_template('materials/index.html')
    context = {}
    return HttpResponse(template.render(context, request))

def simple_upload(request):
    try:
        if request.method == 'POST' and request.FILES['myfile']:

            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)

            # ... do here the magic
            creator = MaterialCreator()
            result = creator.createMaterialfromCSV('.' + uploaded_file_url)
            result_json = []

            for material in result:
                result_json.append(json.dumps(material))

            r = requests.post('http://localhost:4567/auth/materials/', json=result)

            backend_message = BackendMessage(json.loads(r.text))
            print(backend_message)

            cleanup(uploaded_file_url)

            return render(request, 'materials/simple_upload.html', {
                'uploaded_materials': result_json})

    except MultiValueDictKeyError as exception:
            print("No file selected")
            return render(request, 'materials/simple_upload.html', {'error_message': 'No file selected'})

    return render(request, 'materials/simple_upload.html')

