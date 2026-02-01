from django.shortcuts import render,redirect

def api_root_view(request):
    return redirect('api-root')