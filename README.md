
# Secure Encoder

## Introduction
Secure Encoder is a web application designed to encode and decode text using various cryptographic algorithms. This application supports operations like Base64, Hex, UTF-8, Latin-1, ASCII, URL encoding/decoding, and encryption/decryption using AES and RSA algorithms. It aims to provide a user-friendly interface for secure text manipulation, which is especially useful for developers and security professionals.

## Features
- **File Uploads:** Users can upload key files needed for encryption/decoding.
- **Dynamic Encoding/Decoding:** Support for multiple encoding schemes including Base64, Hex, and more.
- **Encryption and Decryption:** Implements AES and RSA algorithms using uploaded keys.
- **Interactive UI:** Real-time web application built with React.
- **Security:** Implements best practices like Content Security Policy headers.

## Tech Stack
- **Frontend:** React.js
- **Backend:** Flask (Python)
- **CSS Framework:** Bootstrap

## Project Setup

### Prerequisites
- Node.js (v14 or later)
- npm (Node Package Manager)
- Python 3.8 or later

### Environment Setup
1. Clone the repository:
   ```bash
   git clone SecureEncoderMain
   ```

2. Set up the backend:
   ```bash
   cd SecureEncoderFlask
   pip install -r requirements.txt
   ```

3. Set up the frontend:
   ```bash
   cd SecureEncoderReact
   npm install
   ```

4. Set environment variables:
   Update the `.env` file in the SecureEncoderReact directory or the src file inside SecureEncoderFlask directory if necessary.

### Running the Application

#### Backend
1. Navigate to the `SecureEncoderFlask` directory.
2. Run the Flask application:
   ```bash
   python run.py
   ```
   This will launch the backend on `http://localhost:5000`.

#### Frontend
1. Open a new terminal and navigate to the `SecureEncoderReact` directory.
2. Start the React application:
   ```bash
   npm start
   ```
   This will launch the web application on `http://localhost:3000` and connect it to the Flask backend.

## Notes
- Ensure CORS is properly configured to allow your frontend and backend to interact over different ports during development.
- Keep your cryptographic keys secure and ensure they are not exposed to unauthorized users.
- Regularly update dependencies to mitigate vulnerabilities associated with outdated libraries.
