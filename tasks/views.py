from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

# from django.views.generic.delete import DeleteView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

from tasks.models import Task, UserProfile
from tasks.utils import sortPriorities, AuthMixin, ListViewWithSearch
from tasks.forms import (
    TaskCreateForm,
    UserAuthenticationForm,
    UserCreationFormCustom,
    ModifyMailTimeForm,
)

from django.shortcuts import render


def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/tasks")
    else:
        return HttpResponseRedirect("/user/login")


class UserLoginView(LoginView):
    form_class = UserAuthenticationForm
    template_name = "user_login.html"
    success_url = "/user/login/"


class UserCreateView(CreateView):
    form_class = UserCreationFormCustom
    template_name = "user_create.html"
    success_url = "/tasks/"


# class MailTimeUpdateView(AuthMixin, UpdateView):
#     form_class = ModifyMailTimeForm
#     template_name = "modify_mail_time.html"


class MailTimeUpdateView(AuthMixin, View):
    form_class = ModifyMailTimeForm
    template_name = "modify_mail_time.html"

    def get(self, request):
        mail_time = request.GET.get("mailTime")
        # print(self.__dict__)
        print(request.__dict__)

        return render(request, "modify_mail_time.html")


class GenericTaskUpdateView(AuthMixin, UpdateView):
    form_class = TaskCreateForm
    template_name = "task_update.html"


class GenericTaskCreateView(AuthMixin, CreateView):
    form_class = TaskCreateForm
    template_name = "task_create.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class GenericTaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "task_detail.html"

    def get_success_url(self):
        return Task.objects.filter(deleted=False, user=self.request.user).exclude(
            status="COMPLETED"
        )


class GenericTaskDeleteView(AuthMixin, DeleteView):
    template_name = "task_delete.html"


class GenericTaskView(LoginRequiredMixin, ListViewWithSearch):
    queryset = Task.objects.filter(deleted=False).exclude(status="COMPLETED")
    template_name = "tasks.html"
    context_object_name = "tasks"
    paginate_by = 5


class CompleteTaskView(AuthMixin, View):
    def get(self, request, pk):
        tasks = Task.objects.filter(id=pk, user=self.request.user)
        tasks.update(status="COMPLETED")

        return HttpResponseRedirect("/tasks")


class CompletedTasksView(AuthMixin, ListViewWithSearch):
    queryset = Task.objects.filter(status="COMPLETED")
    template_name = "completed.html"
    context_object_name = "completed"
    paginate_by = 5


class AllTasksView(AuthMixin, ListViewWithSearch):
    queryset = Task.objects.all()
    template_name = "all_tasks.html"
    context_object_name = "all_tasks"
    paginate_by = 5


def session_storage_view(request):
    total_views = (
        int(request.session.get("total_views"))
        if request.session.get("total_views") is not None
        else 0
    )
    request.session["total_views"] = total_views + 1

    return HttpResponse(f"<h1>Total number of views = {total_views}</h1>")


def bg_jobs(request):
    return HttpResponse("Triggered Background jobs...")
