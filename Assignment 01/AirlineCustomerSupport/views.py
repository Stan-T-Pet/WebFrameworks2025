from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.admin.views.decorators import staff_member_required
from .forms import CustomerRegisterForm, SupportRequestForm, MessageForm, ManualUserCreateForm
from django.utils.crypto import get_random_string
from .models import SupportRequest, Message
from django.contrib import messages
import uuid


# =========================
# Role-Based Decorators
# =========================

def support_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'support':
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# =========================
# Public Views
# =========================

def register(request):
    if request.method == 'POST':
        form = CustomerRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatic login after registration
            messages.success(request, "Welcome! Your account was created successfully.")
            return redirect('dashboard')  # Redirect to customer dashboard on auto login
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomerRegisterForm()
    return render(request, 'AirlineCustomerSupport/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")

            # Role-based redirection
            if user.role == 'customer':
                return redirect('dashboard')
            elif user.role == 'support':
                return redirect('support_dashboard')
            elif user.role == 'admin':
                return redirect('admin_dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'AirlineCustomerSupport/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

# =========================
# Customer Views
# =========================

@login_required
def customer_dashboard(request):
    if not request.user.role == 'customer':
        raise PermissionDenied
    return render(request, 'AirlineCustomerSupport/dashboard.html')

@login_required
def support_request(request):
    if request.method == 'POST':
        form = SupportRequestForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.customer = request.user
            ticket.request_code = get_random_string(8)
            ticket.save()
            messages.success(request, "Support request submitted.")
            return redirect('customer_messages')
    else:
        form = SupportRequestForm()
    return render(request, 'AirlineCustomerSupport/support_request.html', {'form': form})


@login_required
def customer_messages(request):
    if not request.user.role == 'customer':
        raise PermissionDenied
    tickets = request.user.support_requests.all()
    return render(request, 'AirlineCustomerSupport/messages.html', {'tickets': tickets})

@login_required
def customer_chat(request, request_code):
    ticket = get_object_or_404(SupportRequest, request_code=request_code)
    if ticket.customer != request.user:
        raise PermissionDenied

    messages = Message.objects.filter(support_request=ticket)
    form = MessageForm(request.POST or None)
    if form.is_valid():
        msg = form.save(commit=False)
        msg.sender = request.user
        msg.support_request = ticket
        msg.save()
        return redirect('customer_chat', request_code=request_code)
    return render(request, 'AirlineCustomerSupport/customer_chat.html', {
        'ticket': ticket,
        'messages': messages,
        'form': form
    })

# =========================
# Support Agent Views
# =========================

@login_required
@support_required
def staff_login(request):
    return redirect('support_dashboard')

@login_required
@support_required
def support_dashboard(request):
    return render(request, 'AirlineCustomerSupport/support_dashboard.html')

@login_required
@support_required
def agent_message_list(request):
    tickets = SupportRequest.objects.all()
    return render(request, 'AirlineCustomerSupport/agent_messages.html', {'tickets': tickets})

@login_required
@support_required
def support_chat(request, request_code):
    ticket = get_object_or_404(SupportRequest, request_code=request_code)
    messages_qs = Message.objects.filter(support_request=ticket).order_by('timestamp')

    if request.method == 'POST':
        message_form = MessageForm(request.POST)
        status = request.POST.get('status')

        if message_form.is_valid():
            msg = message_form.save(commit=False)
            msg.sender = request.user
            msg.support_request = ticket
            msg.save()

        if status and status != ticket.status:
            ticket.status = status
            ticket.save()

        return redirect('support_chat', request_code=request_code)
    else:
        message_form = MessageForm()

    return render(request, 'AirlineCustomerSupport/support_chat.html', {
        'ticket': ticket,
        'messages': messages_qs,
        'form': message_form,
        'status_choices': SupportRequest.STATUS_TYPES
    })


@login_required
@support_required
def support_elevator(request, request_code):
    ticket = get_object_or_404(SupportRequest, request_code=request_code)
    return render(request, 'AirlineCustomerSupport/support_elevator.html', {'ticket': ticket})

# =========================
# Admin Views
# =========================

@login_required
@staff_member_required
def admin_dashboard(request):
    return render(request, 'AirlineCustomerSupport/admin_dashboard.html')

@login_required
@staff_member_required
def chat_manager(request):
    chats = Message.objects.all()
    return render(request, 'AirlineCustomerSupport/chat_manager.html', {'chats': chats})

@login_required
@staff_member_required
def user_manager(request):
    return render(request, 'AirlineCustomerSupport/user_manager.html')

@login_required
@staff_member_required
def manual_user_create(request):
    form = ManualUserCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('admin_dashboard')
    return render(request, 'AirlineCustomerSupport/manual_user_create.html', {'form': form})
