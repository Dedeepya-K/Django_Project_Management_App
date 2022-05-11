from django.shortcuts import render
from django.views.generic import (TemplateView, DetailView,
                                    ListView, CreateView,
                                    UpdateView,DeleteView,FormView,)
from .models import Branch, Domain, Project
#, Comment, WorkingDays, TimeSlots
from django.urls import reverse_lazy
from .forms import CommentForm,ReplyForm, ProjectForm
from django.http import HttpResponseRedirect



class BranchListView(ListView):
    context_object_name = 'branchs'
    model = Branch
    template_name = 'departments/branch_list_view.html'

class DomainListView(DetailView):
    context_object_name = 'branchs'
  #  extra_context = {
   #     'slots': TimeSlots.objects.all()
    #}
    model = Branch
    template_name = 'departments/domain_list_view.html'

class ProjectListView(DetailView):
    context_object_name = 'domains'
    model = Domain
    template_name = 'departments/project_list_view.html'

class ProjectDetailView(DetailView, FormView):
    context_object_name = 'projects'
    model = Project
    template_name = 'departments/project_detail_view.html'
    form_class = CommentForm
    second_form_class = ReplyForm

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(request=self.request)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(request=self.request)
        # context['comments'] = Comment.objects.filter(id=self.object.id)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'form' in request.POST:
            form_class = self.get_form_class()
            form_name = 'form'
        else:
            form_class = self.second_form_class
            form_name = 'form2'

        form = self.get_form(form_class)
        # print("the form name is : ", form)
        # print("form name: ", form_name)
        # print("form_class:",form_class)

        if form_name=='form' and form.is_valid():
            print("comment form is returned")
            return self.form_valid(form)
        elif form_name=='form2' and form.is_valid():
            print("reply form is returned")
            return self.form2_valid(form)


    def get_success_url(self):
        self.object = self.get_object()
        Branch = self.object.Branch
        domain = self.object.domain
        return reverse_lazy('departments:project_detail',kwargs={'branch':Branch.slug,
                                                             'domain':domain.slug,
                                                             'slug':self.object.slug})
    def form_valid(self, form):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.author = self.request.user
        fm.project_name = self.object.comments.name
        fm.project_name_id = self.object.id
        fm.save()
        return HttpResponseRedirect(self.get_success_url())

    def form2_valid(self, form):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.author = self.request.user
        fm.comment_name_id = self.request.POST.get('comment.id')
        fm.save()
        return HttpResponseRedirect(self.get_success_url())


class ProjectCreateView(CreateView):
    # fields = ('lesson_id','name','position','image','video','ppt','Notes')
    form_class =ProjectForm
    context_object_name = 'domain'
    model= Domain
    template_name = 'departments/project_create.html'

    def get_success_url(self):
        self.object = self.get_object()
        branch = self.object.branch
        return reverse_lazy('departments:project_list',kwargs={'branch':branch.slug,
                                                             'slug':self.object.slug})


    def form_valid(self, form, *args, **kwargs):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.created_by = self.request.user
        fm.Branch = self.object.branch
        fm.domain = self.object
        fm.save()
        return HttpResponseRedirect(self.get_success_url())

class ProjectUpdateView(UpdateView):
    fields = ('name','position','video','ppt','Other_Details')
    model= Project
    template_name = 'departments/project_update.html'
    context_object_name = 'projects'

class ProjectDeleteView(DeleteView):
    model= Project
    context_object_name = 'projects'
    template_name = 'departments/project_delete.html'

    def get_success_url(self):
        print(self.object)
        branch = self.object.Branch
        domain = self.object.domain
        return reverse_lazy('departmetns:project_list',kwargs={'branch':branch.slug,'slug':domain.slug})
