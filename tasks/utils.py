# from django.views import View
from django.views.generic.list import ListView

# from django.views.generic.edit import CreateView, UpdateView, DeleteView
# from django.views.generic.detail import DetailView

# from django.views.generic.delete import DeleteView

# from django.forms import ModelForm

# from django.contrib.auth.forms import UserCreationForm

# from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

from tasks.models import Task


def diffCheck(obj1, obj2):
    str_rep1: str = str(obj1).split("\n")
    str_rep2: str = str(obj2).split("\n")
    diff_lines: list = []

    if str_rep2 != str_rep1:
        i: int = 0
        if len(str_rep1) > len(str_rep2):
            for i in range(len(str_rep2)):
                if str_rep1[i] != str_rep2[i]:
                    diff_lines += [(str_rep1, str_rep2)]
            for i in range(len(str_rep2), len(str_rep1)):
                diff_lines += [(str_rep1[i], "")]

        elif len(str_rep1) < len(str_rep2):
            for i in range(len(str_rep1)):
                if str_rep1[i] != str_rep2[i]:
                    diff_lines += [(str_rep1, str_rep2)]
            for i in range(len(str_rep1), len(str_rep2)):
                diff_lines += [("", str_rep2[i])]

    return diff_lines


def IsDiff(obj1, obj2):
    str_rep1: str = str(obj1)
    str_rep2: str = str(obj2)

    return str_rep1 != str_rep2


def sortPriorities(priorityValue, queryset):
    for i in range(queryset.count() - 1):
        if queryset[i].priority == priorityValue:
            queryset[i].priority += 1

        if queryset[i].priority == queryset[i + 1].priority:
            queryset[i + 1].priority += 1

    return queryset


class AuthMixin(LoginRequiredMixin):
    login_url = "/user/login"
    success_url = "/tasks"
    model = Task

    def get_success_url(self):
        return "/tasks"


class ViewMixin(LoginRequiredMixin):
    pass


class ListViewWithSearch(ListView):
    def get_queryset(self):
        search_term = self.request.GET.get("search")
        tasks = self.queryset.filter(user=self.request.user)

        if search_term:
            tasks = self.queryset.filter(
                title__icontains=search_term, user=self.request.user
            )

        return tasks
