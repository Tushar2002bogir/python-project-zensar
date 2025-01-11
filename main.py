import json
import cx_Oracle
from datetime import date, datetime
from decimal import Decimal
from http.server import BaseHTTPRequestHandler, HTTPServer

# Oracle database configuration
DB_CONFIG = {
   "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "vehicle"
}

def get_db_connection():
    """Get an Oracle database connection."""
    return cx_Oracle.connect(**DB_CONFIG)

class CustomJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder to handle date, datetime, and Decimal types."""
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)

class RequestHandler(BaseHTTPRequestHandler):
    """RequestHandler to process GET and POST requests."""

    def do_GET(self):
        """Handle GET requests."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            if self.path.startswith("/vehicles/"):
                vehicle_id = self.path.split("/")[-1]
                cursor.execute("SELECT * FROM Vehicle WHERE Vehicle_ID = :vehicle_id", {"vehicle_id": vehicle_id})
                result = cursor.fetchone()
            elif self.path.startswith("/owners/"):
                owner_id = self.path.split("/")[-1]
                cursor.execute("SELECT * FROM Owner WHERE Owner_ID = :owner_id", {"owner_id": owner_id})
                result = cursor.fetchone()
            elif self.path.startswith("/ownership_transfer/"):
                transfer_id = self.path.split("/")[-1]
                cursor.execute("SELECT * FROM Ownership_Transfer WHERE Transfer_ID = :transfer_id", {"transfer_id": transfer_id})
                result = cursor.fetchone()
            elif self.path.startswith("/vehicle_insurance/"):
                insurance_id = self.path.split("/")[-1]
                cursor.execute("SELECT * FROM Vehicle_Insurance WHERE Insurance_ID = :insurance_id", {"insurance_id": insurance_id})
                result = cursor.fetchone()
            elif self.path.startswith("/vehicle_tax/"):
                tax_id = self.path.split("/")[-1]
                cursor.execute("SELECT * FROM Vehicle_Tax WHERE Tax_ID = :tax_id", {"tax_id": tax_id})
                result = cursor.fetchone()
            elif self.path.startswith("/vehicle_inspection/"):
                inspection_id = self.path.split("/")[-1]
                cursor.execute("SELECT * FROM Vehicle_Inspection WHERE Inspection_ID = :inspection_id", {"inspection_id": inspection_id})
                result = cursor.fetchone()
            else:
                cursor.execute("SELECT * FROM Vehicle")  # Default to fetching all vehicles
                result = cursor.fetchall()

            response_body = json.dumps(result, cls=CustomJSONEncoder)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(response_body.encode())
        except Exception as e:
            self.send_error(500, str(e))
        finally:
            cursor.close()
            conn.close()

    def do_POST(self):
        """Handle POST requests."""
        cursor = None
        conn = None
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)

            # Handle insertion based on the URL path
            if self.path.startswith("/owners/"):
                self.create_owner(data)

            elif self.path.startswith("/vehicles/"):
                self.create_vehicle(data)

            elif self.path.startswith("/ownership_transfer/"):
                self.transfer_ownership(data)

            elif self.path.startswith("/vehicle_insurance/"):
                self.add_vehicle_insurance(data)

            elif self.path.startswith("/vehicle_tax/"):
                self.add_vehicle_tax(data)

            elif self.path.startswith("/vehicle_inspection/"):
                self.add_vehicle_inspection(data)

            self.send_response(201)  # Created
            self.send_header("Content-type", "application/json")
            self.end_headers()

            response = {"message": "Data added successfully"}
            self.wfile.write(json.dumps(response).encode())

        except cx_Oracle.Error as db_err:
            self.send_error(500, f"Database error: {str(db_err)}")
        except Exception as e:
            self.send_error(500, f"Error: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    # Procedure for creating an Owner
    def create_owner(self, data):
        owner_id = data.get("Owner_ID")
        owner_name = data.get("Owner_Name")
        contact_number = data.get("Contact_Number")
        address = data.get("Address")
        
        if not all([owner_id, owner_name, contact_number, address]):
            self.send_error(400, "Missing required fields")
            return
        
        insert_query = """
            INSERT INTO Owner (Owner_ID, Owner_Name, Contact_Number, Address)
            VALUES (:owner_id, :owner_name, :contact_number, :address)
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(insert_query, {
            "owner_id": owner_id,
            "owner_name": owner_name,
            "contact_number": contact_number,
            "address": address
        })
        conn.commit()

    # Procedure for creating a Vehicle
    def create_vehicle(self, data):
        vehicle_id = data.get("Vehicle_ID")
        vehicle_type = data.get("Vehicle_Type")
        vehicle_number = data.get("Vehicle_Number")
        owner_id = data.get("Owner_ID")

        if not all([vehicle_id, vehicle_type, vehicle_number, owner_id]):
            self.send_error(400, "Missing required fields")
            return

        insert_query = """
            INSERT INTO Vehicle (Vehicle_ID, Vehicle_Type, Vehicle_Number, Owner_ID)
            VALUES (:vehicle_id, :vehicle_type, :vehicle_number, :owner_id)
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(insert_query, {
            "vehicle_id": vehicle_id,
            "vehicle_type": vehicle_type,
            "vehicle_number": vehicle_number,
            "owner_id": owner_id
        })
        conn.commit()

    # Procedure for transferring ownership
    def transfer_ownership(self, data):
        vehicle_id = data.get("Vehicle_ID")
        new_owner_id = data.get("New_Owner_ID")

        if not all([vehicle_id, new_owner_id]):
            self.send_error(400, "Missing required fields")
            return
        
        # First, fetch the current owner from the Vehicle table
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT Owner_ID FROM Vehicle WHERE Vehicle_ID = :vehicle_id", {"vehicle_id": vehicle_id})
        old_owner_id = cursor.fetchone()[0]
        
        # Insert ownership transfer record
        insert_query = """
            INSERT INTO Ownership_Transfer (Transfer_ID, Vehicle_ID, Old_Owner_ID, New_Owner_ID, Transfer_Date)
            VALUES (Ownership_Transfer_SEQ.NEXTVAL, :vehicle_id, :old_owner_id, :new_owner_id, SYSDATE)
        """
        cursor.execute(insert_query, {
            "vehicle_id": vehicle_id,
            "old_owner_id": old_owner_id,
            "new_owner_id": new_owner_id
        })
        conn.commit()

        # Update the vehicle's owner
        cursor.execute("UPDATE Vehicle SET Owner_ID = :new_owner_id WHERE Vehicle_ID = :vehicle_id", {
            "new_owner_id": new_owner_id,
            "vehicle_id": vehicle_id
        })
        conn.commit()

    # Procedure for adding Vehicle Insurance
    def add_vehicle_insurance(self, data):
        insurance_id = data.get("Insurance_ID")
        vehicle_id = data.get("Vehicle_ID")
        policy_number = data.get("Policy_Number")
        start_date = data.get("Start_Date")
        end_date = data.get("End_Date")
        premium_amount = data.get("Premium_Amount")

        if not all([insurance_id, vehicle_id, policy_number, start_date, end_date, premium_amount]):
            self.send_error(400, "Missing required fields")
            return

        insert_query = """
            INSERT INTO Vehicle_Insurance (Insurance_ID, Vehicle_ID, Policy_Number, Start_Date, End_Date, Premium_Amount)
            VALUES (:insurance_id, :vehicle_id, :policy_number, :start_date, :end_date, :premium_amount)
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(insert_query, {
            "insurance_id": insurance_id,
            "vehicle_id": vehicle_id,
            "policy_number": policy_number,
            "start_date": start_date,
            "end_date": end_date,
            "premium_amount": premium_amount
        })
        conn.commit()

    # Procedure for adding Vehicle Tax
    def add_vehicle_tax(self, data):
        tax_id = data.get("Tax_ID")
        vehicle_id = data.get("Vehicle_ID")
        tax_type = data.get("Tax_Type")
        amount = data.get("Amount")
        payment_date = data.get("Payment_Date")

        if not all([tax_id, vehicle_id, tax_type, amount, payment_date]):
            self.send_error(400, "Missing required fields")
            return

        insert_query = """
            INSERT INTO Vehicle_Tax (Tax_ID, Vehicle_ID, Tax_Type, Amount, Payment_Date)
            VALUES (:tax_id, :vehicle_id, :tax_type, :amount, :payment_date)
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(insert_query, {
            "tax_id": tax_id,
            "vehicle_id": vehicle_id,
            "tax_type": tax_type,
            "amount": amount,
            "payment_date": payment_date
        })
        conn.commit()

    # Procedure for adding Vehicle Inspection
    def add_vehicle_inspection(self, data):
        inspection_id = data.get("Inspection_ID")
        vehicle_id = data.get("Vehicle_ID")
        inspection_date = data.get("Inspection_Date")
        inspection_result = data.get("Inspection_Result")

        if not all([inspection_id, vehicle_id, inspection_date, inspection_result]):
            self.send_error(400, "Missing required fields")
            return

        insert_query = """
            INSERT INTO Vehicle_Inspection (Inspection_ID, Vehicle_ID, Inspection_Date, Inspection_Result)
            VALUES (:inspection_id, :vehicle_id, :inspection_date, :inspection_result)
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(insert_query, {
            "inspection_id": inspection_id,
            "vehicle_id": vehicle_id,
            "inspection_date": inspection_date,
            "inspection_result": inspection_result
        })
        conn.commit()

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    """Run the HTTP server."""
    server_address = ("", port)
    print(f"Server started at port {port}")
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == "__main__":
    run()
