from django.urls import path
from .views import (
    create_order_view,
    create_order_countdown_view,
    create_order_result_tracking_view,
    check_task_status_view,
    create_order_chain_view,
    create_order_group_view
    )

urlpatterns = [
    path('create/', create_order_view, name='create-order'),
    path(
        "createcountdown/",
        create_order_countdown_view,
        name="create-order-countdown",
    ),
    path('create_result_tracking/', create_order_result_tracking_view, name='check-task-status'),
    path('status/<str:task_id>/', check_task_status_view, name='check-task-status'),
    path('chain_create/', create_order_chain_view, name='chain_create'),
    path('group_create/', create_order_group_view, name='group_create'),
]