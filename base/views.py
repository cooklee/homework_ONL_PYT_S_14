from django.shortcuts import render, redirect


# Create your views here.
def index(request):
    lang = request.COOKIES.get('lang', 'not set')
    return render(request, 'base/base.html', {'lang': lang})

def set_language_view(request):
    if request.method == 'POST':
        lang = request.POST['lang']
        http_response = redirect('index')
        http_response.set_cookie('lang', lang)
    return http_response