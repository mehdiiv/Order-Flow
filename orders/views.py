from django.http import JsonResponse
from celery import chain, group, chord
from .tasks import (
    send_order_email, 
    send_order_email_count_down,
    process_payment,
    send_invoice_email,
    send_sms_notification,
    generate_summary_report,
    )
from celery.result import AsyncResult

def create_order_view(request):
    order_id = 1001
    customer_email = "test@example.com"

    send_order_email.delay(order_id, customer_email)

    return JsonResponse({
        "status": "Success",
        "message": "Order created! Confirmation email is sending in background." 
    })


def create_order_countdown_view(request):
    order_id = -1001
    customer_email = "test@example.com"

    send_order_email_count_down.apply_async(
        args=[order_id, customer_email],
        countdown=10,
    )

    return JsonResponse({
        "status": "Success",
        "message": "Order created! Email task scheduled to execute in 10 seconds.",
    })

def create_order_result_tracking_view(request):
    order_id = 1001
    customer_email = "test@example.com"
    
    task = send_order_email.delay(order_id, customer_email)
    
    return JsonResponse({
        "status": "Success",
        "message": "Order created successfully!",
        "task_id": task.id
    })

def check_task_status_view(request, task_id):
    result = AsyncResult(task_id)

    return JsonResponse({
        "task_id": task_id,
        "status": result.status,
        "result": str(result.result) if result.ready() else None
    })

def create_order_chain_view(request):
    order_id = 2002

    workflow = chain(process_payment.s(order_id)|send_invoice_email.s())
    result = workflow.apply_async()

    return JsonResponse({
        "status": "Success",
        "message": "Order processing pipeline started!",
        "task_id": result.id
    })

def create_order_group_view(request):
    user_ids = [101, 102, 103]

    workflow = chord(
        group(send_sms_notification.s(uid) for uid in user_ids),
        generate_summary_report.s()
    )

    result = workflow.apply_async()
    
    return JsonResponse({
        "status": "Success",
        "message": "Group and Chord workflow started!",
        "task_id": result.id
    })