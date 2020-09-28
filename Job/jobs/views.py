from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from .models import Job,Category


class HomeView(ListView):
    template_name = 'jobs/index.html'
    context_object_name = 'jobs'
    model = Job
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
