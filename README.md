

# Vehicle Management REST API

This project is a REST API built using Python for managing vehicle-related data such as vehicle details, owners, insurance, tax, inspection, and ownership transfers. The API uses Oracle Database for data storage and provides endpoints to perform CRUD operations.

---

## Features

1. *Vehicle Management*:
   - Add, retrieve, and update vehicle details.
2. *Owner Management*:
   - Add, retrieve, and transfer ownership of vehicles.
3. *Insurance Management*:
   - Add and retrieve vehicle insurance details.
4. *Tax Management*:
   - Add and retrieve vehicle tax details.
5. *Inspection Management*:
   - Add and retrieve vehicle inspection details.
6. *Ownership Transfers*:
   - Manage and track ownership transfers of vehicles.

---

## Prerequisites

Before running this project, ensure you have the following installed:

1. Python 3.x
2. Oracle Database
3. Oracle Database Driver (cx_Oracle)
4. Postman or similar API testing tools

---

## Installation

1. Clone this repository:
   bash
   git clone https://github.com/Tushar2002bogir/python-project-zensar.git
   

2. Navigate to the project directory:
   bash
   cd vehicle-management-api
   

3. Install the required dependencies:
   bash
   pip install cx_Oracle
   

4. Configure the Oracle Database:
   - Update the DB_CONFIG dictionary in the script with your database credentials:
     python
     DB_CONFIG = {
         "host": "localhost",
         "user": "root",
         "password": "root",
         "database": "vehicle"
     }
     

5. Set up the database schema:
   - Create tables by running the provided SQL script (schema.sql) in your Oracle database.

6. Start the server:
   bash
   python vehicle_management_api.py
   

---

## Endpoints

The API provides the following endpoints:

### Vehicles

- *GET* /vehicles/ - Retrieve all vehicles.
- *GET* /vehicles/{vehicle_id} - Retrieve a specific vehicle by ID.
- *POST* /vehicles/ - Add a new vehicle.

### Owners

- *GET* /owners/{owner_id} - Retrieve owner details by ID.
- *POST* /owners/ - Add a new owner.

### Ownership Transfers

- *POST* /ownership_transfer/ - Transfer ownership of a vehicle.

### Vehicle Insurance

- *GET* /vehicle_insurance/{insurance_id} - Retrieve insurance details by ID.
- *POST* /vehicle_insurance/ - Add new insurance details.

### Vehicle Tax

- *GET* /vehicle_tax/{tax_id} - Retrieve tax details by ID.
- *POST* /vehicle_tax/ - Add new tax details.

### Vehicle Inspection

- *GET* /vehicle_inspection/{inspection_id} - Retrieve inspection details by ID.
- *POST* /vehicle_inspection/ - Add new inspection details.

---



















## Sample Database Schema

sql
CREATE TABLE Owner (
    Owner_ID NUMBER PRIMARY KEY,
    Owner_Name VARCHAR2(50),
    Contact_Number VARCHAR2(15),
    Address VARCHAR2(100)
);

CREATE TABLE Vehicle (
    Vehicle_ID NUMBER PRIMARY KEY,
    Vehicle_Type VARCHAR2(20),
    Vehicle_Number VARCHAR2(20),
    Owner_ID NUMBER,
    FOREIGN KEY (Owner_ID) REFERENCES Owner(Owner_ID)
);

CREATE TABLE Ownership_Transfer (
    Transfer_ID NUMBER PRIMARY KEY,
    Vehicle_ID NUMBER,
    Old_Owner_ID NUMBER,
    New_Owner_ID NUMBER,
    Transfer_Date DATE,
    FOREIGN KEY (Vehicle_ID) REFERENCES Vehicle(Vehicle_ID)
);

CREATE TABLE Vehicle_Insurance (
    Insurance_ID NUMBER PRIMARY KEY,
    Vehicle_ID NUMBER,
    Policy_Number VARCHAR2(30),
    Start_Date DATE,
    End_Date DATE,
    Premium_Amount NUMBER,
    FOREIGN KEY (Vehicle_ID) REFERENCES Vehicle(Vehicle_ID)
);

CREATE TABLE Vehicle_Tax (
    Tax_ID NUMBER PRIMARY KEY,
    Vehicle_ID NUMBER,
    Tax_Type VARCHAR2(30),
    Amount NUMBER,
    Payment_Date DATE,
    FOREIGN KEY (Vehicle_ID) REFERENCES Vehicle(Vehicle_ID)
);

CREATE TABLE Vehicle_Inspection (
    Inspection_ID NUMBER PRIMARY KEY,
    Vehicle_ID NUMBER,
    Inspection_Date DATE,
    Inspection_Result VARCHAR2(50),
    FOREIGN KEY (Vehicle_ID) REFERENCES Vehicle(Vehicle_ID)
);


---

## Usage

### Starting the Server
Run the following command to start the HTTP server:
bash
python vehicle_management_api.py


Here’s a short version of your **Postman Testing Guide** for the **Vehicle Management REST API**:

---

## Testing with Postman

### **GET Request**:
- **URL**: `http://localhost:8080/{endpoint}`
- **Example**: `GET http://localhost:8080/vehicles/1`  
  - **Response**: JSON with vehicle details.

### **POST Request**:
- **URL**: `http://localhost:8080/{endpoint}`
- **Example**: Add a vehicle
  - **Method**: `POST`
  - **Body (JSON)**:
    ```json
    {
        "Vehicle_ID": 1,
        "Vehicle_Type": "Car",
        "Vehicle_Number": "MH12AB1234",
        "Owner_ID": 1
    }
    ```
  - **Response**: `{ "message": "Data added successfully" }`

### **PUT Request**:
- **URL**: `http://localhost:8080/{endpoint}/{id}`
- **Example**: Update vehicle details
  - **Method**: `PUT`
  - **Body (JSON)**:
    ```json
    {
        "Vehicle_Type": "Truck",
        "Vehicle_Number": "MH12XY9876",
        "Owner_ID": 2
    }
    ```
  - **Response**: `{ "message": "Data updated successfully" }`

### **DELETE Request**:
- **URL**: `http://localhost:8080/{endpoint}/{id}`
- **Example**: Delete vehicle by ID
  - **Method**: `DELETE`
  - **Response**: `{ "message": "Data deleted successfully" }`

---

### Common Endpoints:
- **GET** `/vehicles/` - Fetch all vehicles.
- **POST** `/vehicles/` - Add a new vehicle.
- **POST** `/ownership_transfer/` - Transfer ownership.
- **POST** `/vehicle_insurance/` - Add insurance details.
- **PUT** `/vehicles/{vehicle_id}` - Update vehicle info.
- **DELETE** `/vehicles/{vehicle_id}` - Delete vehicle.

---




---




