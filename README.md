# Local Setup of Project

Ensure you have the following installed:

- Python 3.9+
- Node.js and npm
- Git
- Virtual Environment
  
## Backend Setup

1. Navigate to the `backend` directory:

   ```bash
   cd ./backend
   ```

2. Create and activate a virtual environment:
   - **Linux/MacOS**:

     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

   - **Windows**:

     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

3. Create a .env file from the .example.env template and fill in the required values:

    ```
    cp .example.env .env
    ```

    Edit the .env file and add the necessary values:

    ```env
    CHROME_DRIVER_PATH=chrome_driver_path
    TWITTER_USERNAME=twitter_username
    TWITTER_EMAIL=twitter_email
    TWITTER_PASSWORD=twitter_password
    MONGO_DB_URL=mongo_db_url
    PROXY_USERNAME=proxy_username
    PROXY_PASSWORD=proxy_password
    ```

4. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

5. Run the FastAPI backend:

   ```bash
   uvicorn main:app --reload --port 3001
   ```

6. Access the API documentation:
   - Open [http://localhost:3001/docs](http://localhost:3001/docs) for Swagger UI.

## Frontend Setup

### Steps to Set Up the Frontend

1. Navigate to the `frontend` directory:

   ```bash
   cd ./frontend
   ```

2. Install frontend dependencies using npm:

   ```bash
   npm install
   ```

3. Run the frontend development server:

   ```bash
   npm start
   ```

4. Access the application in your browser:
   - Open [http://localhost:3000](http://localhost:3000).

---

# Demo Video

[Watch the demo video](https://drive.google.com/file/d/1PilJcs9iVEmEHZYnm4szigYVQi1Xjmi0/view?usp=sharing)


https://github.com/user-attachments/assets/97e2306b-1a09-4e52-9ff8-fc7fbf1757d5



# References

Got free Proxies from - <https://webshare.io>

How to use proxy while scrapping -<https://www.browserstack.com/guide/set-proxy-in-selenium>
