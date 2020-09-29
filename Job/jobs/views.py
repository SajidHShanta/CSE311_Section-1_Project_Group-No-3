from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView
from .forms import *
from .models import Job, Category


class HomeView(ListView):
    template_name = 'jobs/index.html'
    context_object_name = 'jobs'
    model = Job
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


@method_decorator(login_required(login_url='/'), name='dispatch')
class CreateJobView(SuccessMessageMixin, CreateView):
    model = Job
    template_name = 'jobs/create-jobs.html'
    form_class = CreateJobForm
    success_url = '/'
    success_message = "Job has been posted!"

    def form_valid(self, form):
        job = form.save(commit=False)
        job.employer = self.request.user
        job.save()
        return super(CreateJobView, self).form_valid(form)
