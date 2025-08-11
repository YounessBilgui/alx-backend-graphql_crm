"""
Django-crontab job definitions for CRM application
"""
import os
import django
from datetime import datetime

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'graphql_crm.settings')
django.setup()


def log_crm_heartbeat():
    """
    Log a heartbeat message to confirm CRM application health.
    Logs in format: DD/MM/YYYY-HH:MM:SS CRM is alive
    Optionally queries GraphQL hello field to verify endpoint responsiveness.
    """
    # Get current timestamp in required format
    timestamp = datetime.now().strftime('%d/%m/%Y-%H:%M:%S')
    
    # Create heartbeat message
    heartbeat_message = f"{timestamp} CRM is alive"
    
    try:
        # Optional: Test GraphQL endpoint responsiveness
        from gql import gql, Client
        from gql.transport.requests import RequestsHTTPTransport
        
        # Setup GraphQL client
        transport = RequestsHTTPTransport(url="http://localhost:8000/graphql")
        client = Client(transport=transport, fetch_schema_from_transport=True)
        
        # Query the hello field
        query = gql("""
            query {
                hello
            }
        """)
        
        result = client.execute(query)
        hello_response = result.get('hello', 'No response')
        
        # Enhanced message with GraphQL response
        heartbeat_message += f" - GraphQL hello: {hello_response}"
        
    except Exception as e:
        # If GraphQL query fails, log the error but continue with basic heartbeat
        heartbeat_message += f" - GraphQL check failed: {str(e)}"
    
    # Append heartbeat message to log file
    try:
        with open('/tmp/crm_heartbeat_log.txt', 'a') as log_file:
            log_file.write(heartbeat_message + '\n')
    except Exception as e:
        # Fallback logging if file write fails
        print(f"Failed to write heartbeat log: {e}")
        print(heartbeat_message)


def updatelowstock():
    """
    Executes the updateLowStockProducts mutation via GraphQL endpoint and logs updates.
    """
    import requests
    import json
    from datetime import datetime
    endpoint = 'http://localhost:8000/graphql/'
    mutation = '''
    mutation {
      updateLowStockProducts {
        updatedProducts {
          name
          stock
        }
        message
      }
    }
    '''
    headers = {'Content-Type': 'application/json'}
    response = requests.post(endpoint, json={'query': mutation}, headers=headers)
    log_path = '/tmp/lowstockupdates_log.txt'
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if response.status_code == 200:
        data = response.json()
        try:
            products = data['data']['updateLowStockProducts']['updatedProducts']
            message = data['data']['updateLowStockProducts']['message']
            with open(log_path, 'a') as f:
                f.write(f"[{timestamp}] {message}\n")
                for prod in products:
                    f.write(f"[{timestamp}] {prod['name']} restocked to {prod['stock']}\n")
        except Exception as e:
            with open(log_path, 'a') as f:
                f.write(f"[{timestamp}] Error parsing response: {e}\n")
    else:
        with open(log_path, 'a') as f:
            f.write(f"[{timestamp}] Request failed: {response.status_code} {response.text}\n")