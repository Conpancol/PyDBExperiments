from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.core.files.storage import FileSystemStorage

from .services.QuoteCreator import QuoteCreator
from .forms import QuotesForm

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


def quotes_upload(request):
    try:
        if request.method == 'POST':
            form = QuotesForm(request.POST, request.FILES)
            if form.is_valid():

                quote = QuoteCreator()

                internal_code = form.cleaned_data['internalCode']
                external_code = form.cleaned_data['externalCode']
                provider_code = form.cleaned_data['providerCode']
                received_date = form.cleaned_data['receivedDate']
                sent_date = form.cleaned_data['sentDate']
                user = form.cleaned_data['user']
                provider_id = form.cleaned_data['providerId']
                provider_name = form.cleaned_data['providerName']
                contact_name = form.cleaned_data['contactName']
                incoterms = form.cleaned_data['incoterms']
                note = form.cleaned_data['note']

                quote.setQuoteInformation(internal_code, external_code, provider_code, provider_id, provider_name,
                                          contact_name, received_date, sent_date, user)
                quote.setQuoteIncoterms(incoterms)
                quote.setQuoteNote(note)

                myfile = request.FILES['document']
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                uploaded_file_url = fs.url(filename)

                result = quote.createQuotefromCSV('.' + uploaded_file_url)

                # ...  print(json.dumps(result))

                r = requests.post('http://localhost:4567/auth/quotes/', json=result)

                backend_message = BackendMessage(json.loads(r.text))
                print(backend_message)

                cleanup(uploaded_file_url)

                return render(request, 'quotes/quote_upload.html', {'form': form,
                                                                    'error_message': backend_message.getValue()})

        else:
            form = QuotesForm()
        return render(request, 'quotes/quote_upload.html', {'form': form})

    except Exception as error:
        print("View")
        print(error)

