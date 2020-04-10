from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.template.context_processors import request

# Create your views here.

@login_required
def report_expire(request):
    return render(request, 'report_ex.html')