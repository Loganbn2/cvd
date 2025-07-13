from flask import Flask, render_template, request, jsonify
import os
from supabase import create_client, Client

app = Flask(__name__)

# Security token for Zapier webhook authentication
ZAPIER_TOKEN = os.environ.get('ZAPIER_TOKEN', 'your-secret-token')

SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://vrfgpvzssvywmgzfcwwl.supabase.co')
SUPABASE_KEY = os.environ.get('YOUR_SUPABASE_SERVICE_ROLE_KEY')
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

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
        'points_rollover_date': data.get('Points Rollover Date'),
        'membership_type': data.get('Membership Type'),
    }
    print('Mapped for Supabase:', mapped)
    # Only include non-None fields in update
    update_fields = {k: v for k, v in mapped.items() if k != 'id' and v is not None}
    if not update_fields:
        return jsonify({'error': 'No fields to update'}), 400
    try:
        response = supabase.table('profiles').update(update_fields).eq('id', mapped['id']).execute()
        print('Supabase update response:', response)
        return jsonify({'status': 'success', 'supabase': response.data})
    except Exception as e:
        print('Supabase update error:', str(e))
        return jsonify({'error': str(e)}), 500

@app.route('/api/supabase-user-update', methods=['POST'])
def supabase_user_update():
    # Security check
    token = request.headers.get('X-Zapier-Token')
    if token != ZAPIER_TOKEN:
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.json
    # Map Supabase fields to Zoho fields
    mapped = {
        'ID String': data.get('id'),
        'Web User Name': data.get('name'),
        'Phone': data.get('phone'),
        'Email': data.get('email'),
        'Membership Anniversary': data.get('membership_anniversary'),
        'Points Rollover Date': data.get('rollover_date'),
        'Membership Type': data.get('membership_type'),
    }
    print('Mapped for Zoho:', mapped)
    # TODO: Update or insert user in Zoho using mapped data
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
