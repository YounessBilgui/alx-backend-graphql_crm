"""
Celery tasks for CRM application
"""
import os
import django
from datetime import datetime
from celery import shared_task
import requests

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'graphql_crm.settings')
django.setup()


@shared_task
def generatecrmreport():
    """
    Generate a weekly CRM report using GraphQL queries.
    Fetches total customers, orders, and revenue, then logs to file.
    """
    endpoint = 'http://localhost:8000/graphql/'
    query = '''
    query {
        allCustomers {
            edges { node { id } }
        }
        allOrders {
            edges { node { id totalAmount } }
        }
    }
    '''
    headers = {'Content-Type': 'application/json'}
    response = requests.post(endpoint, json={'query': query}, headers=headers)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_path = '/tmp/crmreportlog.txt'
    if response.status_code == 200:
        data = response.json()
        customers = data['data']['allCustomers']['edges']
        orders = data['data']['allOrders']['edges']
        total_customers = len(customers)
        total_orders = len(orders)
        total_revenue = sum(float(order['node']['totalAmount']) for order in orders)
        with open(log_path, 'a') as f:
            f.write(f"{timestamp} - Report: {total_customers} customers, {total_orders} orders, {total_revenue:.2f} revenue\n")
    else:
        with open(log_path, 'a') as f:
            f.write(f"{timestamp} - Error: {response.status_code} {response.text}\n")


@shared_task
def test_celery():
    """Test task to verify Celery is working"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message = f"{timestamp} - Celery test task executed successfully"
    
    try:
        with open('/tmp/celery_test_log.txt', 'a') as log_file:
            log_file.write(message + '\n')
    except Exception as e:
        print(f"Failed to write test log: {e}")
    
    print(message)
    return message