#!/bin/bash

# ["365", "delete", "print", "count"]

# Move to root dir
cd ../../

# Check if the virtual environment exists and activate it
if [ -d "crm_env" ]; then
    source crm_env/bin/activate
fi

timestamp=$(date +"%Y-%m-%d %H:%M:%S")

# Execute the Django shell command to find and delete inactive customers
python manage.py shell --command="
import os
import django
from datetime import timedelta
from django.utils import timezone
from django.db.models import Max

# Set up Django environment if not already done by manage.py
if not os.environ.get('DJANGO_SETTINGS_MODULE'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')
    django.setup()

from customers.models import Customer, Order

try:
    # Calculate the date for one year ago
    one_year_ago = timezone.now() - timedelta(days=365)

    # Find customers with no orders or whose last order was over a year ago
    # We use a subquery to find the latest order date for each customer
    inactive_customers = Customer.objects.annotate(
        last_order_date=Max('orders__order_date')
    ).filter(
        last_order_date__lt=one_year_ago
    ) | Customer.objects.filter(
        orders__isnull=True
    )

    # Count the number of customers to be deleted
    deleted_count = inactive_customers.count()
    
    # Perform the deletion
    if deleted_count > 0:
        inactive_customers.delete()

    # Log the result to the specified file
    with open('/tmp/customer_cleanup_log.txt', 'a') as log_file:
        log_file.write(f'{timestamp}: Deleted {deleted_count} inactive customers.\n')

except Exception as e:
    with open('/tmp/customer_cleanup_log.txt', 'a') as log_file:
        log_file.write(f'{timestamp}: An error occurred - {e}\n')

print(f'Customer cleanup complete. Deleted {deleted_count} customers.')
"

# Deactivate the virtual environment
deactivate