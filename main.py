from flask import Flask, render_template, request, jsonify
import os
import requests
from supabase import create_client, Client

app = Flask(__name__)

# Security token for Zapier webhook authentication
ZAPIER_TOKEN = os.environ.get('ZAPIER_TOKEN', 'your-secret-token')
# Zapier webhook URL for forwarding Supabase updates
ZAPIER_WEBHOOK_URL = os.environ.get('ZAPIER_WEBHOOK_URL')

SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://vrfgpvzssvywmgzfcwwl.supabase.co')
SUPABASE_KEY = os.environ.get('YOUR_SUPABASE_SERVICE_ROLE_KEY')

# Only create Supabase client if key is provided (for testing without Supabase)
if SUPABASE_KEY:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
else:
    supabase = None

@app.route('/')
def member_portal():
    return render_template('member_portal.html')

@app.route('/reset_password.html')
def reset_password():
    return render_template('reset_password.html')

@app.route('/api/zoho-webuser-update', methods=['POST'])
def zoho_webuser_update():
    # Security check
    token = request.headers.get('X-Zapier-Token')
    if token != ZAPIER_TOKEN:
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.json
    # Map Zoho fields to Supabase fields
    mapped = {
        'id': data.get('ID String'),
        'name': data.get('Web User Name'),
        'phone': data.get('Phone'),
        'email': data.get('Email'),
        'membership_anniversary': data.get('Membership Anniversary'),
        'rollover_date': data.get('Points Rollover Date'),
        'membership_type': data.get('Membership Type'),
    }
    print('Mapped for Supabase:', mapped)
    # Only include non-None fields in update
    update_fields = {k: v for k, v in mapped.items() if k != 'id' and v is not None}
    if not update_fields:
        return jsonify({'error': 'No fields to update'}), 400
    try:
        if supabase:
            response = supabase.table('profiles').update(update_fields).eq('id', mapped['id']).execute()
            print('Supabase update response:', response)
            return jsonify({'status': 'success', 'supabase': response.data})
        else:
            print('Supabase client not configured - skipping database update')
            return jsonify({'status': 'success', 'message': 'Supabase not configured, data processed only'})
    except Exception as e:
        print('Supabase update error:', str(e))
        return jsonify({'error': str(e)}), 500

@app.route('/api/supabase-user-update', methods=['POST'])
def supabase_user_update():
    # This endpoint receives webhooks from Supabase
    # No token check needed since this comes directly from Supabase
    data = request.json
    
    # Extract the record data from Supabase webhook payload
    # Supabase sends data in different formats for INSERT vs UPDATE
    if 'record' in data:
        record = data['record']  # For INSERT events
    elif 'new' in data:
        record = data['new']     # For UPDATE events
    else:
        record = data  # Fallback if data is sent directly
    
    # Map Supabase fields to Zoho fields
    # Use 'name' as primary, fallback to 'User Name' if 'name' is not available
    user_name = record.get('name') or record.get('User Name')
    
    mapped = {
        'ID String': record.get('id'),
        'Web User Name': user_name,
        'Phone': record.get('phone'),
        'Email': record.get('email'),
        'Membership Anniversary': record.get('membership_anniversary'),
        'Points Rollover Date': record.get('rollover_date'),
        'Membership Type': record.get('membership_type'),
    }
    print('Mapped for Zoho:', mapped)
    
    # Filter out None values for cleaner data
    clean_mapped = {k: v for k, v in mapped.items() if v is not None}
    
    # Forward to Zapier webhook if URL is configured
    if ZAPIER_WEBHOOK_URL:
        try:
            response = requests.post(
                ZAPIER_WEBHOOK_URL,
                json=clean_mapped,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            print(f'Zapier webhook response: {response.status_code}')
            
            return jsonify({
                'status': 'success',
                'message': 'Data forwarded to Zapier',
                'zapier_status': response.status_code,
                'zoho_data': clean_mapped
            })
        except Exception as e:
            print(f'Error forwarding to Zapier: {str(e)}')
            return jsonify({
                'status': 'error',
                'message': f'Failed to forward to Zapier: {str(e)}',
                'zoho_data': clean_mapped
            }), 500
    else:
        # If no Zapier URL configured, just return the data
        return jsonify({
            'status': 'success',
            'message': 'Data processed (no Zapier URL configured)',
            'zoho_data': clean_mapped
        })

if __name__ == '__main__':
    app.run(debug=True)
