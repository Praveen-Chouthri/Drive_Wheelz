from flask import Flask, render_template, request, redirect, jsonify,url_for, session,send_file
from database import check_user, add_user,get_user_details,update_user_details,\
    get_vehicle_details, is_vehicle_available,add_rental, get_next_available_date, get_user_rentals ,\
    cancel_rental_by_id, delete_user_by_id, place_rental_order # Import the new function
from dotenv import load_dotenv
import os
from datetime import datetime,date
from flask_mail import Mail, Message
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, Image
from reportlab.lib.units import inch, mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
import qrcode

load_dotenv()


app = Flask(__name__)

faqs = {
    "account": "You can manage your account details, view booking history, and update your profile in the 'Account' section of our website.",
    "vehicle": "Browse our wide selection of cars, bikes, cycles, and trucks on our 'Vehicles' page. You can filter by type, availability, and price.",
    "how to book": "To book a vehicle, navigate to the 'Vehicles' page, select your desired vehicle and rental dates, and follow the on-screen instructions to complete your booking.",
    "rental policies": "Our detailed rental policies, including information on security deposits, driver requirements, and cancellation terms, can be found on our 'Rental Policies' page.",
    "booking confirmation": "After successfully completing your booking, you will receive a confirmation email with your booking details. Please check your inbox and spam folder.",
    "contact support": "You can reach our customer support team by emailing us at support@example.com or by calling us at +91-XXXXXXXXXX during our business hours (Monday to Friday, 9 AM to 6 PM IST)."
}

app.secret_key = os.getenv("FLASK_SECRET_KEY", "fallback_default_key")

if not app.secret_key:
    raise ValueError("FLASK_SECRET_KEY is missing in the environment variables.")

app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

mail = Mail(app)

@app.after_request
def add_header(response):
    # Prevent caching for authenticated pages
    if request.endpoint in ['profile', 'order', 'bill', 'confirm_rental']:
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
    return response

@app.route("/")
def home():
    user_id = session.get('u_id') # Check if a user ID exists in the session
    user = None # Initialize user to None
    if user_id:
        from database import get_user_details
        user = get_user_details(user_id)
    return render_template('home.html', user=user)

@app.route("/profile", methods=["GET","POST"])
def profile():
    if 'u_id' not in session:
        return redirect(url_for("home"))

    user_id = session['u_id']
    user = get_user_details(user_id)

    if not user:
        return "User not found", 404

    current_rentals = get_user_rentals(user_id, rental_status="current")
    past_rentals = get_user_rentals(user_id, rental_status="past")
    return render_template('profile.html', user = user, current_rentals=current_rentals, past_rentals=past_rentals)

@app.route("/cycle")
def cycle():
    return render_template('cycle.html')

@app.route("/bike")
def bike():
    return render_template('bike.html')

@app.route("/car")
def car():
    return render_template('car.html')

@app.route("/truck")
def truck():
    return render_template('truck.html')

@app.route("/order")
def order():
    return render_template('order.html')

@app.route("/logout")
def logout():
    session.pop('u_id', None)
    session.pop('user_name', None)
    session.pop('age', None)
    session.pop('driver_id', None)
    session.pop('email', None)
    session.pop('phone', None)
    return redirect(url_for('home'))

@app.route('/bill', methods=['GET', 'POST'])
def bill():
    if request.method == 'POST':
        vehicle_type = request.form.get('vehicle_type')
        brand = request.form.get('brand')
        model = request.form.get('model')
        start_date_str = request.form.get('start_date')
        end_date_str = request.form.get('end_date')
        days = int(request.form.get('days'))

        vehicle_details = get_vehicle_details(vehicle_type, brand, model)

        if not vehicle_details:
            return jsonify({'error': 'Vehicle details not found.'}), 404

        v_id = vehicle_details['v_id']
        rent_per_day = vehicle_details['rent_per_day']

        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            total_rent = days * float(rent_per_day)

            print(f"Checking availability for v_id: {v_id}, start_date: {start_date}, end_date: {end_date}")
            if not is_vehicle_available(v_id, start_date, end_date):
                next_available_date_data = get_next_available_date(vehicle_type, brand, model, start_date)
                error_data = {'error': 'Selected vehicle is not available for the chosen dates.'}
                if isinstance(next_available_date_data, tuple) and next_available_date_data[1]:
                    error_data['next_available_date'] = next_available_date_data[1].strftime('%d.%m.%Y')
                elif next_available_date_data:
                    if isinstance(next_available_date_data, tuple):
                        if isinstance(next_available_date_data[0], date):
                            error_data['next_available_date'] = next_available_date_data[0].strftime('%d.%m.%Y')
                    elif isinstance(next_available_date_data, datetime.date):
                        error_data['next_available_date'] = next_available_date_data.strftime('%d.%m.%Y')
                    else:
                        error_data['next_available_date'] = None

                return jsonify(error_data), 409

            # Store rental details in session
            session['rental_details'] = {
                'v_id': v_id,
                'u_id': session['u_id'],
                'start_date': start_date_str,
                'end_date': end_date_str,
                'total_rent': total_rent,
                'v_type': vehicle_type.capitalize(),
                'brand': brand,
                'model': model
            }

        except ValueError:
            return jsonify({'error': 'Invalid date format.'}), 400

        return render_template('bill.html',
                               v_type=vehicle_type.capitalize(),
                               brand=brand,
                               model=model,
                               start_date=start_date_str,
                               end_date=end_date_str,
                               total_rent=total_rent,
                               vehicle_number=v_id)
    elif request.method == 'GET':
        # Handle direct navigation or page refresh
        if 'rental_details' in session:
            rental = session['rental_details']
            return render_template('bill.html', 
                v_type=rental['v_type'],
                brand=rental['brand'],
                model=rental['model'],
                start_date=rental['start_date'],
                end_date=rental['end_date'],
                total_rent=rental['total_rent'],
                vehicle_number=rental['v_id']
            )
        else:
            return redirect(url_for('order'))  # Redirect if no active rental

@app.route("/confirm_rental")
def confirm_rental():
    print("Entering /confirm_rental route")
    if 'rental_details' in session:
        rental = session['rental_details']
        print(f"Rental details from session: {rental}")
        user_id = session['u_id']

        add_rental(rental['v_id'], session['u_id'],
                   datetime.strptime(rental['start_date'], '%Y-%m-%d').date(),
                   datetime.strptime(rental['end_date'], '%Y-%m-%d').date(),
                   rental['total_rent'])
        print("add_rental function called successfully")

        user = get_user_details(user_id)
        if user and 'email' in user and user['email'] != 'Not Set':
            recipient_email = user['email']
            subject = "Your Vehicle Rental Confirmation from Drive wheelz"
            body = f"""
Dear {user['user_name']},

Thank you for choosing Drive wheelz for your vehicle rental!

Here are the details of your booking:

Vehicle: {rental['v_type']}
Brand: {rental['brand']}
Model: {rental['model']}
Starting Date: {rental['start_date']}
Return Date: {rental['end_date']}
Total Rent: {rental['total_rent']}
Vehicle Number: {rental['v_id']}

We hope you have a pleasant experience. If you have any questions, please don't hesitate to contact us.

Mail us to:
drivewheelz.rentals@gmail.com

Sincerely,
The Drive wheelz Team
"""
            msg = Message(subject, recipients=[recipient_email], body=body)

            qr_data = url_for('user_rental_info',
                                            user_id=user_id,
                                            v_type=rental['v_type'],
                                            brand=rental['brand'],
                                            model=rental['model'],
                                            vehicle_number=rental['v_id'],
                                            start_date=rental['start_date'],
                                            end_date=rental['end_date'],
                                            total_rent=rental['total_rent'],
                                            _external=True) # URL for the info page
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")

            img_buffer = BytesIO()
            img.save(img_buffer)
            img_buffer.seek(0)

            msg.attach("rental_info_qr.png", "image/png", img_buffer.read())

            try:
                mail.send(msg)
                print(f"Email sent successfully to {recipient_email}")
            except Exception as e:
                print(f"Error sending email: {e}")
        session.pop('rental_details', None)
        return redirect(url_for('profile') + '#rentedVehicleDetails')
    else:
        print("No rental details found in session in /confirm_rental")
        return "No rental details found.", 400


@app.route("/user_rental_info/<user_id>")
def user_rental_info(user_id):
    user = get_user_details(user_id)
    rental_policies = "Coming soon..."
    v_type = request.args.get('v_type')
    brand = request.args.get('brand')
    model = request.args.get('model')
    vehicle_number = request.args.get('vehicle_number')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    total_rent = request.args.get('total_rent')

    if user:
        return render_template('rental_info.html',
                                           user=user,
                                           rental_policies=rental_policies,
                                           v_type=v_type,
                                           brand=brand,
                                           model=model,
                                           vehicle_number=vehicle_number,
                                           start_date=start_date,
                                           end_date=end_date,
                                           total_rent=total_rent)
    else:
        return "User not found", 404

@app.route("/login", methods=["POST"])
def login():
    user_name = request.form.get("login-user_name")
    password = request.form.get("login-password")
    user = check_user(user_name, password)
    if user:
        session['u_id'] = user['u_id']
        session['user_name'] = user['user_name']
        session['age'] = user['age']
        session['driver_id'] = user['driver_id']
        session['email'] = user['email']
        session['phone'] = user['phone']
        return redirect(url_for("profile"))
    else:
        return render_template("home.html", error="Wrong Username or Password")

@app.route("/signup", methods=["POST"])
def signup():
    user_name = request.form.get("signup-user_name")
    age = request.form.get("signup-age")
    driver_id = request.form.get("signup-driver_id")
    email = request.form.get("signup-email_id")
    password = request.form.get("signup-password")
    confirm_password = request.form.get("signup-confirm-password")
    keyword = request.form.get("signup-keyword")

    if password != confirm_password:
        return "Passwords do not match", 400

    u_id = add_user(user_name, age, driver_id, password, keyword,email)

    if u_id:
        session['u_id'] = u_id
        session['user_name'] = user_name
        session['age'] = age
        session['driver_id'] = driver_id
        session['email'] = email
        return redirect(url_for("profile"))
    else:
        return render_template("home.html", signup_error="Signup failed, try again")

@app.route("/update_profile", methods=["POST"])
def update_profile():
    if "u_id" not in session:
        return redirect(url_for("home"))

    u_id = session["u_id"]
    user_name = request.form.get("user_name")
    age = request.form.get("age")
    driver_id = request.form.get("driver_id")
    phone = request.form.get("phone")
    email = request.form.get("email")

    update_user_details(u_id, user_name, age, driver_id, phone, email)

    return redirect(url_for("profile"))

@app.route("/cancel_rental", methods=["POST"])
def cancel_rental():
    if 'u_id' not in session:
        return redirect(url_for('home'))

    vehicle_number = request.form.get('vehicle_number')
    start_date_str = request.form.get('start_date')

    if not all([vehicle_number, start_date_str]):
        return "Missing rental information.", 400

    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    except ValueError:
        return "Invalid date format for start date.", 400

    u_id = session['u_id']
    if cancel_rental_by_id(vehicle_number, u_id, start_date):
        return redirect(url_for('profile') + '#rentedVehicleTab')
    else:
        return "Could not cancel the rental. Please try again or contact support.", 400

@app.route("/delete_account", methods=["POST"])
def delete_account():
    if 'u_id' not in session:
        return redirect(url_for('home'))

    password = request.form.get('signup-confirm-password') # Using the same name as in the popup
    user_id = session['u_id']
    user_details = get_user_details(user_id)

    if user_details and check_user(user_details['user_name'], password):
        delete_user_by_id(user_id)
        session.pop('u_id', None)
        session.pop('user_name', None)
        session.pop('age', None)
        session.pop('driver_id', None)
        session.pop('email', None)
        session.pop('phone', None)
        return redirect(url_for('home'))
    else:
        return "Incorrect password. Account deletion failed.", 401 # 401 Unauthorized

@app.route("/download_receipt")
def download_receipt():
    v_type = request.args.get('v_type', 'N/A')
    brand = request.args.get('brand', 'N/A')
    model = request.args.get('model', 'N/A')
    vehicle_number = request.args.get('vehicle_number', 'N/A')
    start_date_str = request.args.get('start_date', 'N/A')
    end_date_str = request.args.get('end_date', 'N/A')
    total_rent = request.args.get('total_rent', '0.00')
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    margin_px = 80
    margin = margin_px * mm / 3.78
    bg_color = colors.powderblue
    p.setFillColor(bg_color)
    p.rect(0, 0, width, height, fill=1)
    p.setStrokeColor(colors.darkcyan)
    p.setLineWidth(3)
    p.rect(margin, margin, width - 2 * margin, height - 2 * margin)
    logo_path = os.path.join(app.root_path, 'static', 'images', 'logo.png')
    if os.path.exists(logo_path):
        logo = ImageReader(logo_path)
        logo_size = 62
        logo_gap = 85 * mm / 3.78
        logo_x = logo_gap
        logo_y = height - logo_size - logo_gap
        p.saveState()
        p.beginPath()
        p.circle(logo_x + logo_size / 2, logo_y + logo_size / 2, logo_size / 2)
        p.clipPath
        p.drawImage(logo, logo_x, logo_y, logo_size, logo_size, mask='auto')
        p.restoreState()
        p.setStrokeColor(colors.goldenrod)
        p.setLineWidth(2)
        p.circle(logo_x + logo_size / 2, logo_y + logo_size / 2, logo_size / 2)
    p.setFillColor(colors.black)
    p.setFont("Helvetica-Bold", 24)
    p.drawCentredString(width / 2, height - margin - 1.8 * inch, "Drive Wheelz")
    p.setFont("Helvetica-Bold", 12)
    user_details = [
        ("User Name:", str(session.get('user_name', 'N/A'))),
        ("Age:", str(session.get('age', 'N/A'))),
        ("Driver ID:", str(session.get('driver_id', 'N/A'))),
        ("Email:", str(session.get('email', 'N/A'))),
        ("Phone:", str(session.get('phone', 'N/A'))),
    ]
    y_position = height - margin - 2.5 * inch
    line_height = 0.3 * inch
    inner_margin = 50 * mm / 3.78
    x_label = margin + inner_margin
    x_value = margin + 2 * inch + inner_margin
    for label, value in user_details:
        p.drawString(x_label, y_position, label)
        p.setFont("Helvetica", 12)
        p.drawString(x_value, y_position, str(value))
        p.setFont("Helvetica-Bold", 12)
        y_position -= line_height
    p.line(margin, y_position - 0.1 * inch, width - margin, y_position - 0.1 * inch)
    y_position -= 1.0 * inch
    p.setFont("Helvetica-Bold", 12)
    vehicle_details = [
        ("Vehicle:", v_type),
        ("Brand:", brand),
        ("Model:", model),
        ("Vehicle Number:", vehicle_number),
        ("Renting Date:", start_date_str),
        ("Returning Date:", end_date_str),
        ("Total Rent:", total_rent)
    ]
    inner_margin = 50 * mm / 3.78
    x_label = margin + inner_margin
    x_value = margin + 2 * inch  + inner_margin
    for label, value in vehicle_details:
        p.drawString(x_label, y_position, label)
        p.setFont("Helvetica", 12)
        if isinstance(value, int):
            value = str(value)
        p.drawString(x_value, y_position, str(value))
        p.setFont("Helvetica-Bold", 12)
        y_position -= line_height
    p.setFillColor(colors.green)
    p.setFont("Helvetica-Bold", 17.5)
    p.drawCentredString(width / 2, margin + 1.0 * inch, "Thank you for renting with Drive Wheelz!")
    p.showPage()
    p.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=False,
                     mimetype='application/pdf')

@app.route("/chatbot", methods=["POST"])
def chatbot():
    user_message = request.form["message"].lower()
    response = faqs.get(user_message, "Sorry, I don't have information on that. Please try another query.")
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)