# Authenticated-Calculator


## Overview
This project is a Flask-based web application that provides:
- User authentication (registration and login)
- Basic arithmetic operations (addition, subtraction, multiplication, and division)
- User history management for calculations

## Features
- User registration and authentication using `Flask-Bcrypt`
- Secure password storage and validation
- Endpoint to perform arithmetic calculations
- History tracking for user calculations
- Ability to clear calculation history

## Installation

1. Clone this repository:
   ```sh
   git clone https://github.com/gayatrirkaware/Authenticated-Calculator.git
   cd Authenticated-Calculator
   ```

2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3. Configure the project settings in `project_config.py`.

4. Run the Flask application:
   ```sh
   python main.py
   ```

## API Endpoints

### Authentication
- `POST /register` - Registers a new user
- `POST /login` - Logs in an existing user

### Arithmetic Operations
- `POST /calculate` - Performs basic arithmetic operations (`add`, `sub`, `mul`, `div`)
- `POST /history` - Retrieves calculation history for a user
- `POST /clear-history` - Clears the user's calculation history

### Example API Request
#### Register a user
```sh
curl -X POST http://localhost:8083/register -H "Content-Type: application/json" -d '{"username": "testuser", "password": "securepass"}'
```

#### Perform a calculation
```sh
curl -X POST http://localhost:8083/calculate -H "Content-Type: application/json" -d '{"username": "testuser", "password": "securepass", "operation": "add", "operand1": 5, "operand2": 3}'
```

## Database
The application uses MongoDB to store:
- User credentials
- Calculation history


