from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView
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


class SingleJobView(SuccessMessageMixin, UpdateView):
    template_name = 'jobs/single.html'
    model = Job
    context_object_name = 'job'
    form_class = ApplyJobForm
    success_message = "You applied this job!"

    def get_context_data(self, **kwargs):
        context = super(SingleJobView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['employee_applied'] = Job.objects.get(pk=self.kwargs['pk']).employee.all().filter(id=self.request.user.id)
        try:
            context['applied_employees'] = Job.objects.get(pk=self.kwargs['pk'], employer_id=self.request.user.id).employee.all()
            context['employer_id'] = Job.objects.get(pk=self.kwargs['pk']).employer_id
        except:
            pass
        return context

    def form_valid(self, form):
        employee = self.request.user
        form.instance.employee.add(employee)
        form.save()
        return super(SingleJobView, self).form_valid(form)

    def get_success_url(self):
        return reverse('jobs:single_job', kwargs={'slug': self.object.slug, "pk": self.object.pk})


class CategoryDetailView(ListView):
    model = Job
    template_name = 'jobs/category-detail.html'
    context_object_name = 'jobs'
    paginate_by = 2

    def get_queryset(self):
        self.category = get_object_or_404(Category, pk=self.kwargs['pk'])
        return Job.objects.filter(category=self.category)

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(*args, **kwargs)
        self.category = get_object_or_404(Category, pk=self.kwargs['pk'])
        context['categories'] = Category.objects.all()
        context['category'] = self.category
        return context


class SearchJobView(ListView):
    model = Job
    template_name = 'jobs/search.html'
    paginate_by = 2
    context_object_name = 'jobs'

    def get_queryset(self):
        q1 = self.request.GET.get("job_title")
        q2 = self.request.GET.get("job_type")
        q3 = self.request.GET.get("job_location")

        if q1 or q2 or q3:
            return Job.objects.filter(Q(title__icontains=q1) |
                                      Q(description__icontains=q1),
                                      job_type=q2,
                                      location__icontains=q3).order_by('-id')
        return Job.objects.all().order_by('-id')

    def get_context_data(self, *args, **kwargs):
        context = super(SearchJobView, self).get_context_data(*args, **kwargs)
        context['categories'] = Category.objects.all()

        return context
