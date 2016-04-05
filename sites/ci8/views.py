from django.shortcuts import render_to_response
from staticsites.decorators import staticview


@staticview
def index(request):
    ctx = {'title': 'Christian Bianciotto'}

    return render_to_response('ci8/index.html', ctx)
