import os
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# Firebase configuration check and connection initialization
FIREBASE_CONFIGURED = False
db = None
SERVICE_ACCOUNT_FILE = 'firebase-service-account.json'

try:
    if os.path.exists(SERVICE_ACCOUNT_FILE):
        cred = credentials.Certificate(SERVICE_ACCOUNT_FILE)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        FIREBASE_CONFIGURED = True
        print("[Firebase] Firestore connected successfully!")
    else:
        # Fallback env check
        env_cred = os.environ.get("FIREBASE_CREDENTIALS_JSON")
        if env_cred:
            import json
            cred_dict = json.loads(env_cred)
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
            db = firestore.client()
            FIREBASE_CONFIGURED = True
            print("[Firebase] Firestore connected via environment variable!")
        else:
            print("[Firebase] Warning: firebase-service-account.json not found. Running in demo fallback mode.")
except Exception as e:
    print(f"[Firebase] Error: Failed to initialize Firebase: {e}")

def init_firestore_db():
    """Initializes Firestore with mock data if collections are empty."""
    if not FIREBASE_CONFIGURED:
        return

    try:
        # 1. Seed Staff
        staff_ref = db.collection('staff')
        staff_docs = staff_ref.limit(1).get()
        if not staff_docs:
            print("Seeding staff mock records to Firestore...")
            mock_staff = [
                {"employeeId": "EMP101", "name": "Rajesh Kumar", "phoneNumber": "+91 98765 43210", "aadharNumber": "1234 5678 9012", "paymentNumber": "pay@9876543210", "baseSalary": 25000.0, "role": "Incharge", "status": "Approved", "photoUrl": "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=150&q=80", "qrCodeToken": "EMP101", "createdAt": datetime.now().isoformat()},
                {"employeeId": "EMP102", "name": "Suresh Sharma", "phoneNumber": "+91 87654 32109", "aadharNumber": "2345 6789 0123", "paymentNumber": "suresh@ybl", "baseSalary": 15000.0, "role": "Chef", "status": "Approved", "photoUrl": "https://images.unsplash.com/photo-1570295999919-56ceb5ecca61?auto=format&fit=crop&w=150&q=80", "qrCodeToken": "EMP102", "createdAt": datetime.now().isoformat()},
                {"employeeId": "EMP103", "name": "Amit Patel", "phoneNumber": "+91 76543 21098", "aadharNumber": "3456 7890 1234", "paymentNumber": "9876543210@paytm", "baseSalary": 14000.0, "role": "Security", "status": "Approved", "photoUrl": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=150&q=80", "qrCodeToken": "EMP103", "createdAt": datetime.now().isoformat()},
                {"employeeId": "EMP104", "name": "Priya Singh", "phoneNumber": "+91 65432 10987", "aadharNumber": "4567 8901 2345", "paymentNumber": "priya@ybl", "baseSalary": 32000.0, "role": "Admin", "status": "Approved", "photoUrl": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=150&q=80", "qrCodeToken": "EMP104", "createdAt": datetime.now().isoformat()},
                {"employeeId": "EMP105", "name": "Sunita Devi", "phoneNumber": "+91 54321 09876", "aadharNumber": "5678 9012 3456", "paymentNumber": "sunita@sbi", "baseSalary": 12000.0, "role": "Janitor", "status": "Pending", "photoUrl": "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?auto=format&fit=crop&w=150&q=80", "qrCodeToken": "EMP105", "createdAt": datetime.now().isoformat()},
                {"employeeId": "EMP106", "name": "Vikram Malhotra", "phoneNumber": "+91 43210 98765", "aadharNumber": "6789 0123 4567", "paymentNumber": "vikram@axis", "baseSalary": 22000.0, "role": "Warden", "status": "Pending", "photoUrl": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=150&q=80", "qrCodeToken": "EMP106", "createdAt": datetime.now().isoformat()},
            ]
            for staff in mock_staff:
                staff_ref.document(staff['employeeId']).set(staff)

        # 2. Seed Attendance
        attendance_ref = db.collection('attendance')
        attendance_docs = attendance_ref.limit(1).get()
        if not attendance_docs:
            print("Seeding attendance logs to Firestore...")
            today_str = datetime.now().strftime("%Y-%m-%d")
            yesterday_str = (datetime.now().replace(day=datetime.now().day - 1) if datetime.now().day > 1 else datetime.now()).strftime("%Y-%m-%d")
            mock_attendance = [
                {"employeeId": "EMP102", "date": yesterday_str, "scanTimestamp": f"{yesterday_str} 08:15:32", "scannedBy": "EMP101"},
                {"employeeId": "EMP103", "date": yesterday_str, "scanTimestamp": f"{yesterday_str} 08:30:11", "scannedBy": "EMP101"},
                {"employeeId": "EMP102", "date": today_str, "scanTimestamp": f"{today_str} 08:05:44", "scannedBy": "EMP101"},
                {"employeeId": "EMP103", "date": today_str, "scanTimestamp": f"{today_str} 08:22:15", "scannedBy": "EMP101"},
            ]
            for att in mock_attendance:
                attendance_ref.add(att)

        # 3. Seed Assets
        assets_ref = db.collection('assets')
        assets_docs = assets_ref.limit(1).get()
        if not assets_docs:
            print("Seeding asset inventory to Firestore...")
            mock_assets = [
                {"itemName": "Single Iron Beds", "quantity": 120, "status": "Excellent"},
                {"itemName": "Ceiling Fans 48-inch", "quantity": 65, "status": "Good"},
                {"itemName": "Commercial Water Purifier RO", "quantity": 3, "status": "Maintenance Required"},
                {"itemName": "Wooden Study Tables", "quantity": 80, "status": "Good"},
                {"itemName": "Plastic Dining Chairs", "quantity": 150, "status": "Excellent"},
                {"itemName": "LED Tube Lights", "quantity": 200, "status": "Good"},
            ]
            for asset in mock_assets:
                assets_ref.add(asset)
    except Exception as e:
        print(f"[Firebase] Error seeding Firestore: {e}")

def require_firebase(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not FIREBASE_CONFIGURED:
            return jsonify({
                "error": "Firebase Firestore is not configured. Please place the 'firebase-service-account.json' file in the project directory."
            }), 503
        return f(*args, **kwargs)
    return decorated_function

# ----------------- API Endpoints -----------------

@app.route('/api/login', methods=['POST'])
def login():
    """Authenticates Admin or Incharge based on custom credentials."""
    data = request.json
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Username and password are required"}), 400
        
    username = data['username'].strip()
    password = data['password'].strip()

    if username == "nani@123" and password == "nanimk@123":
        return jsonify({
            "message": "Admin authentication successful!",
            "role": "Admin",
            "username": username,
            "token": "admin-session-token-9834527"
        }), 200
    elif username == "nanimk@123" and password == "nani@123":
        return jsonify({
            "message": "Incharge authentication successful!",
            "role": "Incharge",
            "username": username,
            "token": "incharge-session-token-1823498"
        }), 200
    else:
        return jsonify({"error": "Invalid username or password. Please try again."}), 401

@app.route('/api/staff', methods=['GET'])
@require_firebase
def get_staff():
    """Fetches all staff members from Firestore."""
    try:
        docs = db.collection('staff').stream()
        staff_list = []
        for doc in docs:
            staff_list.append(doc.to_dict())
        staff_list.sort(key=lambda x: x.get('employeeId', ''), reverse=True)
        return jsonify(staff_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/staff', methods=['POST'])
@require_firebase
def add_staff():
    """Onboards a new staff member with 'Pending' status."""
    data = request.json
    if not data:
        return jsonify({"error": "Missing form data"}), 400
        
    required_fields = ['name', 'phoneNumber', 'aadharNumber', 'paymentNumber', 'baseSalary', 'role']
    for field in required_fields:
        if field not in data or not str(data[field]).strip():
            return jsonify({"error": f"Field '{field}' is required"}), 400

    try:
        # Determine the next employee ID
        docs = db.collection('staff').stream()
        max_id_num = 100
        for doc in docs:
            emp_id_str = doc.id
            if emp_id_str.startswith("EMP"):
                try:
                    num = int(emp_id_str[3:])
                    if num > max_id_num:
                        max_id_num = num
                except ValueError:
                    pass
        emp_id = f"EMP{max_id_num + 1}"
        
        photo_url = data.get('photoUrl')
        if not photo_url or not photo_url.strip():
            photo_url = "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=150&q=80"

        new_staff = {
            "employeeId": emp_id,
            "name": data['name'].strip(),
            "phoneNumber": data['phoneNumber'].strip(),
            "aadharNumber": data['aadharNumber'].strip(),
            "paymentNumber": data['paymentNumber'].strip(),
            "baseSalary": float(data['baseSalary']),
            "role": data['role'].strip(),
            "status": "Pending",
            "photoUrl": photo_url.strip(),
            "qrCodeToken": emp_id,
            "createdAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        db.collection('staff').document(emp_id).set(new_staff)
        return jsonify({"message": "Staff onboarding request submitted successfully!", "staff": new_staff}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/staff/<emp_id>/status', methods=['PATCH'])
@require_firebase
def update_staff_status(emp_id):
    """Approves or rejects a staff profile in Firestore."""
    data = request.json
    if not data or 'status' not in data:
        return jsonify({"error": "Status field is required"}), 400
        
    status = data['status']
    if status not in ['Approved', 'Rejected']:
        return jsonify({"error": "Invalid status. Must be 'Approved' or 'Rejected'"}), 400

    try:
        doc_ref = db.collection('staff').document(emp_id)
        doc = doc_ref.get()
        if not doc.exists:
            return jsonify({"error": "Staff member not found"}), 404
        
        staff_data = doc.to_dict()
        if status == 'Rejected':
            # Delete staff document
            doc_ref.delete()
            # Clean up associated attendance logs
            att_docs = db.collection('attendance').where('employeeId', '==', emp_id).stream()
            for att_doc in att_docs:
                db.collection('attendance').document(att_doc.id).delete()
            message = f"Staff application for {staff_data['name']} ({emp_id}) was rejected and removed."
        else:
            doc_ref.update({"status": status})
            message = f"Staff member {staff_data['name']} ({emp_id}) approved successfully!"

        return jsonify({"message": message, "status": status})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/attendance', methods=['GET'])
@require_firebase
def get_attendance():
    """Retrieves all attendance logs with in-memory staff lookup optimization."""
    try:
        # Fetch all approved staff for rapid in-memory joining
        staff_docs = db.collection('staff').stream()
        staff_map = {doc.id: doc.to_dict() for doc in staff_docs}

        # Fetch attendance logs
        att_docs = db.collection('attendance').stream()
        attendance_list = []
        for doc in att_docs:
            att_data = doc.to_dict()
            att_data['id'] = doc.id
            
            emp_id = att_data.get('employeeId')
            staff_info = staff_map.get(emp_id, {})
            
            att_data['name'] = staff_info.get('name', 'Unknown')
            att_data['role'] = staff_info.get('role', 'Unknown')
            att_data['photoUrl'] = staff_info.get('photoUrl', '')
            attendance_list.append(att_data)

        # Sort by timestamp descending
        attendance_list.sort(key=lambda x: x.get('scanTimestamp', ''), reverse=True)
        return jsonify(attendance_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/attendance', methods=['POST'])
@require_firebase
def log_attendance():
    """Logs a scan timestamp for daily attendance in Firestore."""
    data = request.json
    if not data or 'employeeId' not in data or 'scannedBy' not in data:
        return jsonify({"error": "employeeId and scannedBy are required"}), 400
        
    emp_id = data['employeeId'].strip()
    scanned_by = data['scannedBy'].strip()
    
    try:
        # Validate employee exists and is approved
        staff_doc = db.collection('staff').document(emp_id).get()
        if not staff_doc.exists:
            return jsonify({"error": f"Invalid QR Code. Employee ID '{emp_id}' not found."}), 404
            
        staff_data = staff_doc.to_dict()
        if staff_data.get('status') != 'Approved':
            return jsonify({"error": f"Staff member '{staff_data.get('name')}' is pending approval and cannot log attendance."}), 400

        # Check if already scanned today
        today_str = datetime.now().strftime("%Y-%m-%d")
        duplicates = db.collection('attendance') \
                       .where('employeeId', '==', emp_id) \
                       .where('date', '==', today_str) \
                       .limit(1).get()
        if duplicates:
            existing_data = duplicates[0].to_dict()
            return jsonify({
                "message": f"Attendance already logged for {staff_data.get('name')} today!",
                "alreadyLogged": True,
                "staff": staff_data,
                "timestamp": existing_data.get('scanTimestamp')
            }), 200

        # Log daily attendance
        timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.collection('attendance').add({
            "employeeId": emp_id,
            "date": today_str,
            "scanTimestamp": timestamp_str,
            "scannedBy": scanned_by
        })
        
        return jsonify({
            "message": f"Attendance logged successfully for {staff_data.get('name')}!",
            "alreadyLogged": False,
            "staff": staff_data,
            "timestamp": timestamp_str
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ----------------- Asset Management CRUD -----------------

@app.route('/api/assets', methods=['GET'])
@require_firebase
def get_assets():
    """Fetches all assets from Firestore."""
    try:
        docs = db.collection('assets').stream()
        assets_list = []
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            assets_list.append(data)
        assets_list.sort(key=lambda x: x.get('itemName', '').lower())
        return jsonify(assets_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/assets', methods=['POST'])
@require_firebase
def add_asset():
    """Adds a new asset to inventory in Firestore with unique validation."""
    data = request.json
    if not data or 'itemName' not in data or 'quantity' not in data or 'status' not in data:
        return jsonify({"error": "itemName, quantity, and status are required"}), 400
        
    item_name = data['itemName'].strip()
    try:
        # Enforce unique asset name
        existing = db.collection('assets').where('itemName', '==', item_name).limit(1).get()
        if existing:
            return jsonify({"error": "An asset with this name already exists"}), 400

        new_asset = {
            "itemName": item_name,
            "quantity": int(data['quantity']),
            "status": data['status'].strip()
        }
        # Create a document reference explicitly to get its unique ID
        doc_ref = db.collection('assets').document()
        doc_ref.set(new_asset)
        new_asset['id'] = doc_ref.id
        
        return jsonify({"message": "Asset added successfully", "asset": new_asset}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/assets/<asset_id>', methods=['PUT'])
@require_firebase
def update_asset(asset_id):
    """Updates an existing asset's fields in Firestore."""
    data = request.json
    if not data or 'itemName' not in data or 'quantity' not in data or 'status' not in data:
        return jsonify({"error": "itemName, quantity, and status are required"}), 400

    item_name = data['itemName'].strip()
    try:
        # Ensure name is not taken by another asset
        existing = db.collection('assets').where('itemName', '==', item_name).limit(1).get()
        if existing and existing[0].id != asset_id:
            return jsonify({"error": "Another asset with this name already exists"}), 400

        db.collection('assets').document(asset_id).update({
            "itemName": item_name,
            "quantity": int(data['quantity']),
            "status": data['status'].strip()
        })
        return jsonify({"message": "Asset updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/assets/<asset_id>', methods=['DELETE'])
@require_firebase
def delete_asset(asset_id):
    """Deletes an asset from Firestore inventory."""
    try:
        db.collection('assets').document(asset_id).delete()
        return jsonify({"message": "Asset deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ----------------- Frontend HTML Serving -----------------

@app.route('/')
def home():
    """Serves the central single page application HTML."""
    try:
        with open(os.path.join('templates', 'index.html'), 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Inject warning banner if Firebase is not connected
        if not FIREBASE_CONFIGURED:
            warning_banner = """
            <div id="firebase-warning-banner" style="background-color: #f59e0b; color: #78350f; padding: 12px; text-align: center; font-weight: 600; font-family: sans-serif; position: sticky; top: 0; z-index: 9999; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
                &#9888;&#65039; RUNNING IN DEMO MODE (Firebase Credentials Missing): Please place the <code>firebase-service-account.json</code> file in the root of the project directory.
            </div>
            """
            body_idx = html_content.find("<body")
            if body_idx != -1:
                close_idx = html_content.find(">", body_idx)
                if close_idx != -1:
                    html_content = html_content[:close_idx+1] + "\n" + warning_banner + html_content[close_idx+1:]

        return render_template_string(html_content)
    except FileNotFoundError:
        return """
        <div style="font-family: sans-serif; text-align: center; margin-top: 100px;">
            <h1 style="color: #4f46e5;">Mahesh Hostel Staff Management Website</h1>
            <p style="color: #4b5563;">Frontend file templates/index.html is missing.</p>
        </div>
        """, 404

if __name__ == '__main__':
    if FIREBASE_CONFIGURED:
        init_firestore_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
