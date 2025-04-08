from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import os
from datetime import date,timedelta

load_dotenv()

db_connection_string = os.getenv('DB_CONNECTION_STRING')
engine = create_engine(db_connection_string)

if not db_connection_string:
    raise ValueError("DB_CONNECTION_STRING is missing in the environment variables.")

# Function to check user login credentials
def check_user(user_name, password):
    with engine.connect() as conn:
        result = conn.execute(text(
            "SELECT * FROM users WHERE user_name = :user_name AND pass = :pass"
        ), {"user_name": user_name, "pass": password})
        user = result.fetchone()
        return dict(zip(result.keys(),user)) if user else None  # True if user exists, else False

# Function to fetch user details using user_id
def get_user_details(u_id):
    with engine.connect() as conn:
        result = conn.execute(text(
            """SELECT user_name, age, driver_id,
                     COALESCE(email, 'Not Set') AS email,
                     COALESCE(phone, 'Not Set') AS phone
                FROM users WHERE u_id = :u_id"""
        ), {"u_id": u_id})
        user = result.fetchone()
        if user:
            user_dict = dict(zip(result.keys(), user))
            print("User Details:", user_dict)  # Debugging
            return user_dict
        else:
            print("No user found for ID:", u_id)
            return None


# Function to add a new user to the database
def add_user(user_name, age, driver_id, password, keyword,email):
    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO users (user_name, age, driver_id, pass, keyword, email)
            VALUES (:user_name, :age, :driver_id, :password, :keyword, :email)
        """), {
            "user_name": user_name,
            "age": age,
            "driver_id": driver_id,
            "password": password,
            "keyword": keyword,
            "email": email
        })
        conn.commit()
        user_result = conn.execute(text("SELECT LAST_INSERT_ID()")) 
        u_id = user_result.scalar_one()
        return u_id

def update_user_details(u_id, user_name, age, driver_id, phone, email):
    with engine.connect() as conn:
        update_fields = {}
        if user_name is not None:
            update_fields['user_name'] = user_name
        if age is not None:
            update_fields['age'] = age
        if driver_id is not None:
            update_fields['driver_id'] = driver_id
        if phone is not None:
            update_fields['phone'] = phone
        if email is not None:
            update_fields['email'] = email

        if update_fields:  # Only update if there are fields to update
            set_clause = ", ".join(f"{key} = :{key}" for key in update_fields)
            query = text(f"UPDATE users SET {set_clause} WHERE u_id = :u_id")
            conn.execute(query, {**update_fields, "u_id": u_id})
            conn.commit()

# Function to get vehicle details by type, brand, and model
def get_vehicle_details(v_type, brand, model):
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT v_id, rent_per_day
            FROM vehicles
            WHERE v_type = :v_type AND brand = :brand AND model = :model
        """), {"v_type": v_type, "brand": brand, "model": model})
        vehicle = result.fetchone()
        return dict(zip(result.keys(), vehicle)) if vehicle else None

# Function to check if a vehicle is available for the given date range
def is_vehicle_available(v_id, start_date, end_date):
    print(f"Checking availability for v_id: {v_id}, start_date: {start_date}, end_date: {end_date}")
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT COUNT(*)
            FROM rentals
            WHERE v_id = :v_id
                AND (start_date <= :end_date AND end_date >= :start_date)
        """), {"v_id": v_id, "start_date": start_date, "end_date": end_date})
        count = result.scalar_one()
        print(f"Count of overlapping rentals: {count}")
        return count == 0

# Function to add a new rental record
def add_rental(v_id, u_id, start_date, end_date, total_rent):
    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO rentals (v_id, u_id, start_date, end_date, total_rent)
            VALUES (:v_id, :u_id, :start_date, :end_date, :total_rent)
        """), {
            "v_id": v_id,
            "u_id": u_id,
            "start_date": start_date,
            "end_date": end_date,
            "total_rent": total_rent
        })
        conn.commit()

# Function to find the next available date for a specific vehicle model
def get_next_available_date(v_type, brand, model, requested_start_date):
    with engine.connect() as conn:
        # First, get the vehicle ID
        vehicle_result = conn.execute(text("""
            SELECT v_id FROM vehicles
            WHERE v_type = :v_type AND brand = :brand AND model = :model
        """), {"v_type": v_type, "brand": brand, "model": model})
        vehicle = vehicle_result.fetchone()
        if not vehicle:
            return None, "Vehicle model not found."
        v_id = vehicle[0]

        # Find the latest end date of rentals for this vehicle that start on or after the requested start date
        result = conn.execute(text("""
            SELECT MAX(end_date)
            FROM rentals
            WHERE v_id = :v_id AND start_date >= :requested_start_date
        """), {"v_id": v_id, "requested_start_date": requested_start_date})
        latest_end_date = result.scalar_one_or_none()

        if latest_end_date:
            return latest_end_date + timedelta(days=1), None

        # If no future rentals found, check for rentals ending after the requested start date
        result = conn.execute(text("""
            SELECT MAX(end_date)
            FROM rentals
            WHERE v_id = :v_id AND end_date >= :requested_start_date
        """), {"v_id": v_id, "requested_start_date": requested_start_date})
        latest_end_date = result.scalar_one_or_none()

        if latest_end_date:
            return latest_end_date + timedelta(days=1), None

        return date.today(), None # If no rentals found, it's available from today

def get_user_rentals(u_id, rental_status="current"):

    today = date.today()
    filter_condition = ""
    if rental_status == "current":
        filter_condition = "r.end_date >= :today"
    elif rental_status == "past":
        filter_condition = "r.end_date < :today"
    else: # Default to current if status is invalid
        filter_condition = "r.end_date >= :today"

    with engine.connect() as conn:
        query = text(f"""
            SELECT
                v.v_type AS vehicle_type,
                v.brand,
                v.model,
                v.v_id AS vehicle_number,
                r.start_date,
                r.end_date,
                r.total_rent
            FROM rentals r
            JOIN vehicles v ON r.v_id = v.v_id
            WHERE r.u_id = :u_id AND {filter_condition}
            ORDER BY r.start_date DESC -- Optional: order by date
        """)
        result = conn.execute(query, {"u_id": u_id, "today": today})
        rentals = [dict(zip(result.keys(), row)) for row in result]
        return rentals

# Function to cancel a rental by vehicle ID, user ID, and start date
def cancel_rental_by_id(vehicle_number, u_id, start_date):
    with engine.connect() as conn:
        result = conn.execute(text("""
            DELETE FROM rentals
            WHERE v_id = :vehicle_number AND u_id = :u_id AND start_date = :start_date
        """), {"vehicle_number": vehicle_number, "u_id": u_id, "start_date": start_date})
        conn.commit()
        return result.rowcount > 0

# Function to delete a user by their ID
def delete_user_by_id(u_id):
    with engine.connect() as conn:
        conn.execute(text("""
            DELETE FROM users
            WHERE u_id = :u_id
        """), {"u_id": u_id})
        conn.commit()

# New function to place a rental order
def place_rental_order(u_id, v_id, start_date, end_date, total_rent):
    with engine.connect() as conn:
        result = conn.execute(text("""
            INSERT INTO rentals (v_id, u_id, start_date, end_date, total_rent)
            VALUES (:v_id, :u_id, :start_date, :end_date, :total_rent)
        """), {
            "v_id": v_id,
            "u_id": u_id,
            "start_date": start_date,
            "end_date": end_date,
            "total_rent": total_rent
        })
        conn.commit()
        return result.lastrowid # Return the ID of the newly inserted rental