# from django.views import View
# from django.http.response import JsonResponse
from tasks.models import Task, STATUS_CHOICES  # , Changelog
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer, Serializer, Field
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import (
    DjangoFilterBackend,
    FilterSet,
    CharFilter,
    ChoiceFilter,
    DateTimeFilter,
    NumberFilter,
)


import json


class TaskFilter(FilterSet):
    title = CharFilter(
        lookup_expr="icontains"
    )  # Applying the filter - Title 'contains' search term?
    status = ChoiceFilter(choices=STATUS_CHOICES)


# class ChangelogFilter(FilterSet):
#     id = NumberFilter(lookup_expr="exact")
#     edit_time = DateTimeFilter(lookup_expr="gte")


# class ChangesSerializer(Field):
#     def to_representation(self, instance):
#         return json.loads(instance)

#     def to_internal_value(self, data):
#         return None


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("username",)


# class ChangelogSerializer(ModelSerializer):
#     # user = UserSerializer(read_only=True)
#     # diff = ChangesSerializer(read_only=True)
#     # read_only = True
#     # read_only_fields = ("task", "old_status", "new_status", "edit_time")
#     # task = serializers.CharField(read_only=True)
#     # old_status = serializers.CharField(read_only=True)
#     # new_status = serializers.CharField(read_only=True)
#     # edit_time = serializers.DateTimeField(read_only=True)

#     class Meta:
#         model = Changelog
#         fields = (
#             "task",
#             "old_status",
#             "new_status",
#             "edit_time",
#             # "user",
#         )


class TaskSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = (
            "user",
            "id",
            "title",
            "description",
            # "completed",
            "status",
        )


class TaskViewSet(ReadOnlyModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    permission_classes = (IsAuthenticated,)

    filter_backends = (DjangoFilterBackend,)
    filterset_class = TaskFilter

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, deleted=False)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# class ChangelogViewSet(ReadOnlyModelViewSet):
#     queryset = Changelog.objects.all()
#     serializer_class = ChangelogSerializer

#     permission_classes = (IsAuthenticated,)

#     filter_backends = (DjangoFilterBackend,)
#     filterset_class = ChangelogFilter

#     def get_queryset(self, *args, **kwargs):
#         print(f"\n\nRequest dict = \n\n{self.request._user._wrapped.__dict__}\n\n")
#         if "task_pk" in self.request.parser_context["kwargs"].keys():
#             # print(f"\n\nTotal request=\n\n{str(self.request.user)}\n\n")
#             return Changelog.objects.filter(
#                 # user=self.request.task.user,
#                 task=self.request.parser_context["kwargs"]["task_pk"],
#             )
#         return Changelog.objects.filter(user=self.request.user)

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)


# class TaskListAPI(LoginRequiredMixin, APIView):
#     def get(self, request, request_type):
#         if request_type in ["all", "completed", "incomplete"]:
#             if request_type == "completed":
#                 tasks_list = Task.objects.filter(user=self.request.user, completed=True)
#             elif request_type == "incomplete":
#                 tasks_list = Task.objects.filter(
#                     user=self.request.user, completed=False
#                 )
#             else:
#                 tasks_list = Task.objects.filter(user=self.request.user)
#         else:
#             tasks_list = []

#         response = TaskSerializer(tasks_list, many=True).data

#         return Response(response)


# class ChangelogListAPI(LoginRequiredMixin, APIView):
#     def filter_queryset(self, request, queryset, view):
#         filter_class = self.get_filter_class(view, queryset)

#         if filter_class:
#             return filter_class()

#     def get(self, request, task_id):
#         changelog_list = Changelog.objects.filter(user=self.request.user, task=task_id)

#         response = ChangelogSerializer(changelog_list, many=True).data

#         # print(response)
#         # print(self.request.__dict__)

#         return Response(response)


class DRFView(APIView):
    def get(self, request, task_id):
        # print(f"\n\n{[x.id for x in Task.objects.filter(user=self.request.user)]}\n\n")
        task = Task.objects.filter(id=task_id, user=self.request.user).first()

        return Response(
            {
                "priority": task.priority,
                "title": task.title,
                "description": task.description,
                "status": task.status,
            }
        )


class GenericTaskSerializer(Serializer):
    priority = serializers.IntegerField(min_value=1)
    task = serializers.CharField(max_length=100)
    description = serializers.CharField()
    status = serializers.ChoiceField(choices=STATUS_CHOICES)

    def create(self, validated_data):
        title = validated_data.get("title")
        description = validated_data.get("description")
        status = validated_data.get("status", False)
        return Task(title=title, description=description, status=status)

    def update(self, instance, validated_data):
        instance.priority = validated_data.get("priority", instance.priority)
        instance.status = validated_data.get("status", instance.status)
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        return instance
