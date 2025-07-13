from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Security token for Zapier webhook authentication
ZAPIER_TOKEN = os.environ.get('ZAPIER_TOKEN', 'your-secret-token')

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
        'anniversary_date': data.get('Membership Anniversary Date'),
        'rollover_date': data.get('Points Rollover Date'),
        'membership_type': data.get('Membership Type'),
    }
    print('Mapped for Supabase:', mapped)
    # TODO: Update or insert user in Supabase using mapped data
    return jsonify({'status': 'success'})

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
        'Membership Anniversary Date': data.get('anniversary_date'),
        'Points Rollover Date': data.get('rollover_date'),
        'Membership Type': data.get('membership_type'),
    }
    print('Mapped for Zoho:', mapped)
    # TODO: Update or insert user in Zoho using mapped data
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
