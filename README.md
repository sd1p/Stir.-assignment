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

3. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the FastAPI backend:

   ```bash
   uvicorn main:app --reload --port 3001
   ```

5. Access the API documentation:
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

<video width="800" controls>
  <source src="assets/stri-assignment-demo.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

# References

Got free Proxies from - <https://webshare.io>

How to use proxy while scrapping -<https://www.browserstack.com/guide/set-proxy-in-selenium>
