from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TelField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp
import json

app = Flask(__name__)
# IMPORTANT: This must match the SECRET_KEY in your final production environment
app.config['SECRET_KEY'] = 'GROCIFY_SUPER_SECRET_KEY_12345' 

# --- MOCK DATABASE (Simulates your DB) ---
MOCK_USERS = {
    'grouser': {
        'id': 201,
        'username': 'grouser',
        'email': 'user@grocify.com',
        'hashed_password': 'securepass', # Mock Hash
        'firstName': 'Grocify',
    }
}
# --- END MOCK DB ---


# --- 1. Registration Form Definition ---
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message='Username is required.')])
    password = PasswordField('Password', validators=[DataRequired(message='Password is required.'), Length(min=8, message='Password must be at least 8 characters long.')])
    firstName = StringField('First Name', validators=[DataRequired(message='First Name is required.')])
    lastName = StringField('Last Name', validators=[DataRequired(message='Last Name is required.')])
    email = StringField('Email ID', validators=[DataRequired(message='Email ID is required.'), Email(message='Invalid email format (e.g., user@domain.com).')])
    phone = TelField('Phone Number', validators=[DataRequired(message='Phone Number is required.'), Regexp(r'^\d{10}$', message='Phone number must be exactly 10 digits.')])
    address = StringField('Address', validators=[DataRequired(message='Address is required.')])
    landmark = StringField('Landmark')
    pincode = StringField('Pin Code', validators=[DataRequired(message='Pin Code is required.'), Regexp(r'^\d{6}$', message='Pin code must be a 6-digit number.')])
    submit = SubmitField('Register')

# --- Helper Functions (Password, Fetch User, etc. remain the same) ---
def verify_password(stored_hash, provided_password):
    return stored_hash == provided_password # Mock verification

def fetch_user(login_id):
    if login_id in MOCK_USERS:
        return MOCK_USERS[login_id]
    for user in MOCK_USERS.values():
        if user['email'] == login_id:
            return user
    return None

# --- 2. API Routes ---

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    username_or_email = data.get('username')
    password = data.get('password')

    user = fetch_user(username_or_email)

    if user and verify_password(user['hashed_password'], password):
        safe_user_details = {'id': user['id'], 'username': user['username'], 'firstName': user['firstName']}
        return jsonify({
            'success': True,
            'message': f'Welcome back, {user["firstName"]}!',
            'user': safe_user_details,
            'token': 'mock_grocify_token_456'
        }), 200
    else:
        return jsonify({'success': False, 'message': 'Invalid username/email or password.'}), 401

# --- 3. Frontend Routes (Serving Pages) ---

# Index Route (Handling GET for display and POST for order submission)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Extract data from the placeorder.html form submission
            order_details_json = request.form.get('order_details_json')
            order_total = request.form.get('order_total_value')
            
            # Shipping details
            shipping_name = request.form.get('name')
            shipping_address = request.form.get('address')
            
            # --- Order Processing Logic ---
            # In a real app: Save order to database, process payment, send confirmation email.
            
            cart_data = json.loads(order_details_json)
            print(f"--- NEW ORDER RECEIVED ---")
            print(f"Total: Rs. {order_total}")
            print(f"Ship to: {shipping_name}, {shipping_address}")
            print(f"Items: {cart_data}")
            print(f"--------------------------")
            
            # Redirect back to the place order page with a success message
            # The client-side JS must clear the cart after successful order submission.
            return render_template('placeorder.html', message=f"Order Rs. {order_total} Confirmed! Thank you, {shipping_name}. Your groceries are on the way!")
            
        except Exception as e:
            print(f"ORDER SUBMISSION ERROR: {e}")
            # Redirect back to the place order page with an error message
            return render_template('placeorder.html', message="Error processing order. Please check all fields.")
    
    # If GET request, render the homepage
    return render_template('index.html')

# New Route for the Place Order page
@app.route('/placeorder.html', methods=['GET'])
def place_order():
    # Renders the placeorder page, which pulls data from URL query params via JS
    return render_template('placeorder.html')


@app.route('/login.html')
def render_login():
    return render_template('login.html')

@app.route('/dashboard.html')
def render_dashboard():
    return render_template('dashboard.html')

@app.route('/CART.HTML', methods=['GET', 'POST']) 
def render_register():
    form = RegistrationForm()

    if form.validate_on_submit():
        if form.username.data in MOCK_USERS or any(u['email'] == form.email.data for u in MOCK_USERS.values()):
            return render_template('CART.HTML', form=form, registration_error="Username or Email already exists. Try logging in.")
            
        # Add the NEW USER to the MOCK_USERS dictionary
        new_user_id = max(u['id'] for u in MOCK_USERS.values()) + 1 if MOCK_USERS else 201
        
        MOCK_USERS[form.username.data] = {
            'id': new_user_id,
            'username': form.username.data,
            'email': form.email.data,
            'hashed_password': form.password.data, 
            'firstName': form.firstName.data,
        }
        
        return redirect(url_for('render_login'))

    return render_template('CART.HTML', form=form)

# Category Pages Routes
@app.route('/FRUITS.HTML')
def render_fruits():
    return render_template('FRUITS.HTML')

@app.route('/VEGETABLES.HTML')
def render_vegetables():
    return render_template('VEGETABLES.HTML')

@app.route('/nuts.html')
def render_nuts():
    return render_template('nuts.html')

@app.route('/pickels.html')
def render_pickels():
    return render_template('pickels.html')

@app.route('/sauces.html')
def render_sauces():
    return render_template('sauces.html')

@app.route('/spices.html')
def render_spices():
    return render_template('spices.html')
# Other dummy category routes (omitted for brevity)

if __name__ == '__main__':
    app.run(debug=True, port=5000)