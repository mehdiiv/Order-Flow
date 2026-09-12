from celery import shared_task, chain, group, chord
import time

@shared_task
def send_order_email(order_id, customer_email):
    time.sleep(15)
    return f"Order #{order_id} email sent successfully to {customer_email}"

@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_kwargs={'max_retries': 3, 'countdown': 5}
)
def send_order_email_count_down(self, order_id, customer_email):
    print(f"Attempting to send email for order #{order_id} (Attempt {self.request.retries + 1})...")
    time.sleep(2)
    
    # Simulation: if order_id is negative, raise exception to test retry
    if order_id < 0:
        raise ValueError("Invalid order ID! Email service connection failed.")
        
    return f"Order #{order_id} email sent successfully to {customer_email}"

@shared_task
def check_pending_orders():
    print("Checking pending orders status in background...")
    return "Pending orders checked successfully"

@shared_task
def process_payment(order_id):
    print(f"Processing payment for order #{order_id}...")
    time.sleep(3)
    return order_id

@shared_task
def send_invoice_email(order_id):
    print(f"Sending invoice email for order #{order_id}...")
    time.sleep(2)
    return f"Order #{order_id} fully processed and invoice sent."

@shared_task
def send_sms_notification(user_id):
    print(f"Sending SMS notification to user #{user_id}...")
    time.sleep(2)
    return f"SMS sent to user {user_id}"

@shared_task
def generate_summary_report(results):
    print(f"Processing final report for results: {results}")
    return f"Summary report generated successfully for {len(results)} users."