from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import login, logout
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Organization, Task, PersonalToDoItem, Membership, Notification
from .forms import OrganizationForm, TaskForm, PersonalToDoItemForm, MembershipForm, UserRegistrationForm
from django.db.utils import IntegrityError
from django.http import JsonResponse
import json

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to ToDoManagement.')
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'core/register.html', {'form': form})

@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have been successfully logged out.')
        return redirect('login')
    return render(request, 'core/logout.html')

# Dashboard View
@login_required
def dashboard(request):
    managed_orgs = Organization.objects.filter(manager=request.user)
    member_orgs = Organization.objects.filter(memberships__user=request.user, memberships__role='m')
    assigned_tasks = Task.objects.filter(assignees=request.user, status='P')
    personal_todos = PersonalToDoItem.objects.filter(user=request.user, completed=False)
    notifications = Notification.objects.filter(user=request.user, read=False)[:5]
    
    context = {
        'managed_orgs': managed_orgs,
        'member_orgs': member_orgs,
        'assigned_tasks': assigned_tasks,
        'personal_todos': personal_todos,
        'notifications': notifications,
    }
    return render(request, 'core/dashboard.html', context)

# Organization Views
class OrganizationListView(LoginRequiredMixin, ListView):
    model = Organization
    template_name = 'core/organization_list.html'
    context_object_name = 'organizations'

    def get_queryset(self):
        return Organization.objects.filter(
            Q(manager=self.request.user) |
            Q(memberships__user=self.request.user)
        ).distinct()

class OrganizationDetailView(LoginRequiredMixin, DetailView):
    model = Organization
    template_name = 'core/organization_detail.html'
    context_object_name = 'organization'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = self.object.tasks.all()
        context['members'] = self.object.memberships.all()
        return context

class OrganizationCreateView(LoginRequiredMixin, CreateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'core/organization_form.html'
    success_url = reverse_lazy('organization_list')

    def form_valid(self, form):
        form.instance.manager = self.request.user
        response = super().form_valid(form)
        # Create membership for the manager
        Membership.objects.create(
            user=self.request.user,
            organization=form.instance,
            role='M'
        )
        return response

class OrganizationUpdateView(LoginRequiredMixin, UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'core/organization_form.html'
    success_url = reverse_lazy('organization_list')

    def get_queryset(self):
        return Organization.objects.filter(manager=self.request.user)

class OrganizationDeleteView(LoginRequiredMixin, DeleteView):
    model = Organization
    template_name = 'core/organization_confirm_delete.html'
    success_url = reverse_lazy('organization_list')

    def get_queryset(self):
        return Organization.objects.filter(manager=self.request.user)

# Task Views
class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'core/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(
            Q(organization__manager=self.request.user) |
            Q(assignees=self.request.user)
        ).distinct()

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'core/task_detail.html'
    context_object_name = 'task'

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'core/task_form.html'
    success_url = reverse_lazy('task_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['assignees'].queryset = User.objects.filter(
            Q(memberships__organization=self.kwargs['org_id']) |
            Q(managed_organizations=self.kwargs['org_id'])
        ).distinct()
        return form

    def form_valid(self, form):
        form.instance.organization_id = self.kwargs['org_id']
        return super().form_valid(form)

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'core/task_form.html'
    success_url = reverse_lazy('task_list')

    def get_queryset(self):
        return Task.objects.filter(organization__manager=self.request.user)

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'core/task_confirm_delete.html'
    success_url = reverse_lazy('task_list')

    def get_queryset(self):
        return Task.objects.filter(organization__manager=self.request.user)

@login_required
def mark_task_complete(request, pk):
    task = get_object_or_404(Task, pk=pk, assignees=request.user)
    task.status = 'C'
    task.save()
    messages.success(request, f'Task "{task.title}" marked as complete.')
    return redirect('task_list')

# Personal To-Do Views
class PersonalToDoListView(LoginRequiredMixin, ListView):
    model = PersonalToDoItem
    template_name = 'core/personal_todo_list.html'
    context_object_name = 'todos'

    def get_queryset(self):
        return PersonalToDoItem.objects.filter(user=self.request.user)

class PersonalToDoCreateView(LoginRequiredMixin, CreateView):
    model = PersonalToDoItem
    form_class = PersonalToDoItemForm
    template_name = 'core/personal_todo_form.html'
    success_url = reverse_lazy('personal_todo_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PersonalToDoUpdateView(LoginRequiredMixin, UpdateView):
    model = PersonalToDoItem
    form_class = PersonalToDoItemForm
    template_name = 'core/personal_todo_form.html'
    success_url = reverse_lazy('personal_todo_list')

    def get_queryset(self):
        return PersonalToDoItem.objects.filter(user=self.request.user)

class PersonalToDoDeleteView(LoginRequiredMixin, DeleteView):
    model = PersonalToDoItem
    template_name = 'core/personal_todo_confirm_delete.html'
    success_url = reverse_lazy('personal_todo_list')

    def get_queryset(self):
        return PersonalToDoItem.objects.filter(user=self.request.user)

@login_required
def mark_todo_complete(request, pk):
    todo = get_object_or_404(PersonalToDoItem, pk=pk, user=request.user)
    todo.completed = True
    todo.save()
    messages.success(request, f'To-do item "{todo.title}" marked as complete.')
    return redirect('personal_todo_list')

# Membership Views
@login_required
def add_member(request, org_id):
    organization = get_object_or_404(Organization, pk=org_id, manager=request.user)
    if request.method == 'POST':
        form = MembershipForm(request.POST)
        if form.is_valid():
            try:
                membership = form.save(commit=False)
                membership.organization = organization
                membership.save()
                messages.success(request, f'Member added successfully.')
            except IntegrityError:
                messages.error(request, 'This user is already a member of the organization.')
            return redirect('organization_detail', pk=org_id)
    else:
        form = MembershipForm()
        # Filter out users who are already members
        existing_members = organization.memberships.values_list('user_id', flat=True)
        form.fields['user'].queryset = User.objects.exclude(id__in=existing_members)
    return render(request, 'core/membership_form.html', {'form': form, 'organization': organization})

@login_required
def remove_member(request, org_id, user_id):
    membership = get_object_or_404(
        Membership,
        organization_id=org_id,
        user_id=user_id,
        organization__manager=request.user
    )
    membership.delete()
    messages.success(request, f'Member removed successfully.')
    return redirect('organization_detail', pk=org_id)

@login_required
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.read = True
    notification.save()
    return JsonResponse({'success': True})

