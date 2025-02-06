## Setup

1. **Clone Repository**
    ```sh
    git clone https://github.com/aswin1618/mt_csv_upload.git
    ```

2. **Setup virtual environment and install dependencies**
    ```sh
    python3 -m venv venv
    source venv/bin/activate  # For Windows: venv\Scripts\activate
    ```

3. **Run DB migrations**
    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

## API Usage

The API provides a single endpoint to upload CSV files.

- **Endpoint**: `/api/test/`
- **Method**: `POST`
- **File Type**: CSV file (.csv)
- **Accepted Fields**:
    - `name`: Non-empty string (required)
    - `email`: Valid email address (required)
    - `age`: Integer (must be between 0 and 120)

### Example Request

### Use Postman

1. **Postman Setup**:
    - Set the method to `POST`.
    - Set the URL to `http://127.0.0.1:8000/api/test/`.
    - In the "Body" tab, select "form-data".
    - Add a key named `file` and upload your `.csv` file.

2. **Sample CSV Content**:
    ```csv
    name,email,age
    John Doe,john@example.com,25
    Jane Doe,jane@example.com,30
    ```

3. **Sample Response**:
    ```json
    {
        "total_saved": 2,
        "total_rejected": 0,
        "total_skipped (duplicates)": 0,
        "errors": []
    }
    ```

4. **Error Response Example**:
    ```json
    {
        "total_saved": 1,
        "total_rejected": 1,
        "total_skipped (duplicates)": 0,
        "errors": [
            {
                "row": 2,
                "errors": {
                    "name": ["This field may not be blank."],
                    "email": ["Enter a valid email address."]
                }
            }
        ]
    }
    ```

### Running Tests

To ensure the functionality of the API, you can run the tests:

1. **Run Unit Tests**:
    ```bash
    python manage.py test core  # This will run all the unit tests and ensure that the API works as expected.
    ```
    