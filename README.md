# reality_bot

This project scrapes the SReality API every 10 minutes, compares the listings with those saved in MongoDB, and sends notification emails for new listings.

## Setup

1. Install dependencies:
    ```
    pip install -r requirements.txt
    ```

2. Set up environment variables in `.env`.

3. Run the FastAPI application:
    ```
    uvicorn app.main:app --reload
    ```

## Usage

- The scraper runs automatically every 10 minutes.
- Access the API at `http://127.0.0.1:8000`.

## Development

- Use `dev_notebook.ipynb` for development and testing.

