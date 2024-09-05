Here’s a comprehensive `README.md` for your project that includes details about the functionality, installation, usage, and testing:

---

# **Network Usage Monitoring API**

This is a **FastAPI** application that provides APIs to monitor network data usage, speed test results, and other related metrics.

## **Features**

- **Line Management**: Fetch and manage network lines.
- **Quota Monitoring**: Track data usage, remaining balance, and renewal costs for each line.
- **Speed Test Tracking**: Log and retrieve speed test results (ping, upload, and download speeds).
- **Usage Statistics**: Get averages for speed and ping, and total data used for a specific period.

## **Tech Stack**

- **Backend**: FastAPI, SQLAlchemy
- **Database**: MySQL or any SQLAlchemy-supported DB (e.g., SQLite for testing)
- **Models**: Pydantic for request/response validation
- **Environment Management**: Python-dotenv for configuration

---

## **Getting Started**

### **Prerequisites**

Make sure you have the following installed:

- **Python 3.8+**
- **MySQL** or another supported database

### **Installation**

1. **Clone the repository**:

   ```bash
   git clone https://github.com/MennaAli02/Network-Usage-Monitoring-API.git
   cd Network-Usage-Monitoring-API
   ```

2. **Create a virtual environment** and activate it:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:

   Create a `.env` file in the project root with the following:

   ```bash
   DB_USER=<your-db-user>
   DB_PASSWORD=<your-db-password>
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=<your-db-name>
   DB_DRIVER=mysql+pymysql  # Or another SQLAlchemy driver
   ```

5. **Run database migrations** (if any).

6. **Start the application**:

   ```bash
   uvicorn app:app --reload
   ```

7. **API Documentation**:

   You can access the interactive API documentation at `http://127.0.0.1:8000/docs`.

---

## **API Endpoints**

### **General**

- **`GET /`**: Health check of the API.

### **Lines**

- **`GET /lines`**: Fetches all network lines or a specific line by ID.

### **Quota Results**

- **`GET /quota-results?line_id={line_id}`**: Fetch quota results for a specific line.

### **Speed Test Results**

- **`GET /speed-test-results?line_id={line_id}`**: Fetch speed test results for a specific line.

### **Statistics**

- **`GET /total-dataused-per-line`**: Fetch total data used for each line.
- **`GET /count-per-renewal-cost`**: Fetch the number of occurrences for each renewal cost.
- **`GET /remaining-balance-by-line`**: Fetch the remaining balance for all lines.
- **`GET /average-speeds-per-line?days={days}`**: Fetch average download and upload speeds for each line over a specified number of days.
- **`GET /average-ping-per-line?days={days}`**: Fetch average ping for each line over a specified number of days.

---

## **Database Models**

### **Line**

- **id**: Unique identifier
- **line_number**: Line number
- **name**: Line name

### **QuotaResults**

- **id**: Unique identifier
- **process_id**: Process identifier for quota
- **line_id**: Foreign key referencing the line
- **data_used**: Data used in MB
- **usage_percentage**: Percentage of the total quota used
- **data_remaining**: Data remaining
- **balance**: Remaining balance
- **renewal_date**: Date of the next renewal
- **remaining_days**: Number of days until renewal
- **renewal_cost**: Cost of renewal
- **date_time**: Timestamp of the record

### **SpeedTestResult**

- **id**: Unique identifier
- **process_id**: Process identifier for speed test
- **line_id**: Foreign key referencing the line
- **ping**: Ping in milliseconds
- **upload_speed**: Upload speed in Mbps
- **download_speed**: Download speed in Mbps
- **public_ip**: Public IP address of the test
- **date_time**: Timestamp of the record

---

## **Running Tests**

This project includes **pytest** for testing.

### **Unit Tests**

1. **Install the development dependencies**:
   ```bash
   pip install pytest
   ```

2. **Run the tests**:

   ```bash
   pytest
   ```

### **Test Coverage**

- Unit tests cover the functionality of each function, including database CRUD operations and calculations for statistics (e.g., average speeds, remaining balance).

---

## **Contributing**

Contributions are welcome! Please fork the repository and create a new branch for any changes you make. Once done, create a pull request with a clear description of what you have changed or added.

1. Fork the repo.
2. Create your feature branch:
   ```bash
   git checkout -b my-new-feature
   ```
3. Commit your changes:
   ```bash
   git commit -am 'Add some feature'
   ```
4. Push the branch:
   ```bash
   git push origin my-new-feature
   ```
5. Create a new pull request.

---

## **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

This `README.md` provides a clear and organized overview of the project, setup instructions, usage details, and how to run tests. You can modify any sections according to your specific requirements.
