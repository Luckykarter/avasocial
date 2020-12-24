from django.shortcuts import redirect


def swagger(request):
    return redirect('/swagger/')
