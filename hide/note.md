Created using "npx create-react-app react-app"
https://react.dev/learn/start-a-new-react-project
https://react.dev/learn/add-react-to-an-existing-project

Run "python app.py" and backend is running in http://localhost:5000
Run "npm start" and frontend is running in http://localhost:3000



### Overall Project Structure

```
/SecureEncoderProject
    /flask-backend
        /venv               # Virtual environment for Flask
        app.py              # Main Flask application file
        requirements.txt    # Python dependencies
        /keys               # Folder to store uploaded keys
    /react-frontend
        /node_modules       # Node.js dependencies
        /public             # Public assets like index.html
        /src                # Source files for the React application
            /components     # React components
                Header.js
                KeyUploader.js
                TextProcessor.js
                ResultDisplay.js
            App.js
            index.js        # Entry point for React application
        package.json        # Project metadata and dependencies for Node.js
        README.md           # Project description and setup instructions
```

### Detailed Description

**Flask Backend (`/flask-backend`):**
- **`app.py`**: This is the main Python file containing your Flask API logic. It includes endpoints for uploading keys, processing text, and other functionalities.
- **`requirements.txt`**: Lists all the Python libraries that the project depends on. Typical contents might include `flask`, `flask_cors`, `werkzeug`, etc.
- **`/keys`**: Directory where uploaded keys (e.g., `.pem` files) are stored.
- **`/venv`**: A Python virtual environment where Flask and other Python dependencies are installed.

**React Frontend (`/react-frontend`):**
- **`/node_modules`**: Contains all the Node.js modules installed via npm or yarn. These support the React application.
- **`/public`**: Holds static files like `index.html`, favicon, and other assets accessible to the public.
- **`/src`**: Contains all the React source code.
  - **`/components`**: Individual React components such as `Header`, `KeyUploader`, `TextProcessor`, and `ResultDisplay`.
  - **`App.js`**: The main React component that includes other components and manages state across them.
  - **`index.js`**: The entry point for the React application, which renders the `App` component.
- **`package.json`**: Defines project metadata, scripts, and lists dependencies necessary for the project.
- **`README.md`**: Provides an overview of the project, setup instructions, and other useful information about the application.

This structure provides a clean separation between the client (React) and the server (Flask), facilitating development and maintenance. Each part of the project can be independently developed and deployed, which is especially useful in team environments or when updating parts of the system.