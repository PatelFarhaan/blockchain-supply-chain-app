# Blockchain Smart Supply Chain

A full-featured supply chain management platform powered by blockchain technology. This application provides user and admin portals for managing warehouses, cargo shipments, and IoT sensors, with all cargo movement data recorded immutably on a blockchain for transparency and auditability.

## Tech Stack

- **Backend:** Python 3, Flask
- **Database:** MongoDB (via MongoEngine)
- **Authentication:** Flask-Login with password hashing (Werkzeug)
- **Serialization:** Flask-Marshmallow
- **Validation:** JSON Schema
- **Routing:** Google Maps Directions API (with Polyline decoding)
- **Architecture:** Blueprint-based modular Flask application

## Features

- **User Management:** Registration, login/logout, session-based authentication
- **Admin Portal:** User management, billing, warehouse overview
- **Warehouse Management:** Create, view, and delete warehouses with geolocation data
- **Cargo Management:** Create, track, and manage cargo shipments between warehouses
- **Sensor Integration:** IoT sensor registration and real-time data collection (temperature, weight, position)
- **Blockchain Recording:** Cargo sensor data is mined into blockchain blocks for tamper-proof audit trails
- **Route Visualization:** Google Maps integration for cargo route mapping
- **Billing System:** Usage-based billing calculated from blockchain nodes and cargo blocks
- **Mobile API Support:** Dedicated mobile endpoints for all operations
- **Input Validation:** JSON Schema validation on all API inputs
- **Error Handling:** Centralized error handlers for 403, 404, 405, and 500 responses

## Prerequisites

- Python 3.7+
- MongoDB 4.0+
- Google Maps API key (for route visualization)
- pip

## Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/<username>/Blockchain-Smart-Supply-Chain.git
   cd Blockchain-Smart-Supply-Chain
   ```

2. **Create and activate a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Start MongoDB**
   ```bash
   mongod --dbpath /path/to/data
   ```

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `SECRET_KEY` | Flask secret key for session management | `change-me-in-production` |
| `MONGODB_URI` | MongoDB connection string | `mongodb://127.0.0.1:27017/admin` |
| `PORT` | Application port | `80` |
| `GOOGLE_MAPS_API_KEY` | Google Maps Directions API key | - |
| `BLOCKCHAIN_NODE_URL` | URL of the blockchain mining node | `http://localhost:80` |

## How to Run

```bash
python app.py
```

The application starts on `http://0.0.0.0:80` by default.

## API Endpoints

### Admin Routes (`/admin`)

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/admin/login` | Admin login |
| `GET` | `/admin/logout` | Admin logout |
| `POST` | `/admin/register` | Register new admin |
| `GET` | `/admin/users` | List all users |
| `DELETE` | `/admin/delete-user` | Delete a user |
| `GET` | `/admin/warehouse` | List all warehouses |
| `GET` | `/admin/billing` | Get billing for all users |
| `POST` | `/admin/user-billing` | Get billing for a single user |

### User Routes (`/user`)

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/user/login` | User login |
| `GET` | `/user/logout` | User logout |
| `POST` | `/user/register` | Register new user |
| `GET/POST` | `/user/warehouse` | View/create warehouses |
| `DELETE` | `/user/warehouse/<name>` | Delete a warehouse |
| `GET/POST` | `/user/cargo` | View/create cargo |
| `GET` | `/user/cargo/<id>` | Get cargo route map details |
| `DELETE` | `/user/cargo/<id>` | Delete a cargo |
| `GET/POST` | `/user/sensor` | View/create sensors |
| `DELETE` | `/user/deletesensor/<id>` | Delete a sensor |
| `POST` | `/user/updatesensor/<name>` | Update sensor data and mine to blockchain |
| `GET` | `/user/warehouse-details` | Get warehouse statistics |
| `GET` | `/user/blockchain-details` | Get recent blockchain activity |

## Project Structure

```
Blockchain-Smart-Supply-Chain/
├── app.py                          # Application entry point
├── requirements.txt                # Python dependencies
├── compiled_files_cleanup.sh       # Cleanup script for .pyc files
├── common_utilities/
│   ├── __init__.py                 # Configuration constants (env-based)
│   ├── admin_json_schema.py        # Admin input validation schemas
│   ├── cargo_json_schema.py        # Cargo input validation schemas
│   ├── sensor_json_schema.py       # Sensor input validation schemas
│   ├── user_json_schema.py         # User input validation schemas
│   └── warehouse_json_schema.py    # Warehouse input validation schemas
└── project/
    ├── __init__.py                 # Flask app factory and configuration
    ├── models.py                   # MongoEngine document models
    ├── admin/
    │   ├── admin_serializer.py     # Admin Marshmallow schemas
    │   └── views.py                # Admin blueprint routes
    ├── error/
    │   └── error_handler.py        # Centralized error handlers
    └── users/
        ├── users_serializer.py     # User Marshmallow schemas
        └── views.py                # User blueprint routes
```

## License

This project is licensed under the MIT License.
