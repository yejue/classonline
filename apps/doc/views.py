from django.shortcuts import render

# Create your views here.


def docDownload(request):
    return render(request, 'doc/docDownload.html')
