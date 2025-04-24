from django.urls import path
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    # Redirect root to login
    path('', RedirectView.as_view(url='login/', permanent=False)),

    # Public
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Customer
    path('dashboard/', views.customer_dashboard, name='dashboard'),
    path('support-request/', views.support_request, name='support_request'),
    path('messages/', views.customer_messages, name='customer_messages'),
    path('customer-chat/<str:request_code>/', views.customer_chat, name='customer_chat'),

    # Staff
    path('staff-login/', views.staff_login, name='staff_login'),
    path('support-dashboard/', views.support_dashboard, name='support_dashboard'),
    path('customer-messages/', views.agent_message_list, name='agent_messages'),
    path('support-chat/<str:request_code>/', views.support_chat, name='support_chat'),
    path('support-elevator/<str:request_code>/', views.support_elevator, name='support_elevator'),

    # Admin
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('chat-manager/', views.chat_manager, name='chat_manager'),
    path('user-manager/', views.user_manager, name='user_manager'),
    path('user/<int:user_id>/', views.view_user, name='view_user'),
    path('user/<int:user_id>/edit/', views.edit_user, name='edit_user'),
    path('user/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    path('manual-user-create/', views.manual_user_create, name='manual_user_create'),
]
