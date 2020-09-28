from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from .models import Job


class HomeView(ListView):
    template_name = 'jobs/index.html'
    context_object_name = 'jobs'
    model = Job

    paginate_by = 1
