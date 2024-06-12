# Secure Encoder

## Introduction
Secure Encoder is a web application designed to encode and decode text using various cryptographic algorithms. This application supports operations like Base64, Hex, UTF-8, Latin-1, ASCII, URL encoding/decoding, and encryption/decryption using AES and RSA algorithms. It aims to provide a user-friendly interface for secure text manipulation, which is especially useful for developers and security professionals. It is based on Python Flask, React, and a little bit of sqlalchemy. It is built with create-react-app and tailwind css.

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

2. Set environment variables:
   Update the `.env` file in the SecureEncoderReact directory or the src file inside SecureEncoderFlask directory if necessary.

### Running the Application in Separate Terminals

#### Backend
1. Navigate to the `SecureEncoderFlask` directory.
   ```bash
   cd SecureEncoderFlask
   ```

2. Set up the backend for the first time running:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Flask application:
   ```bash
   python run.py
   ```
   This will launch the backend on `http://localhost:5000`.

#### Frontend
1. Open a new terminal and navigate to the `SecureEncoderReact` directory.
   ```bash
   cd SecureEncoderReact
   ```

2. Set up the frontend for the first time running:
   ```bash
   npm install
   ```

3. Start the React application:
   ```bash
   npm start
   ```
   This will launch the web application on `http://localhost:3000` and connect it to the Flask backend.

# React Frontend with Docker Compose

This project sets up a React frontend application using Docker and Docker Compose for development with hot reloading.

## Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

Follow these instructions to get the React frontend application up and running in a Docker container.

### Step 1: Clone the Repository

Clone the repository to your local machine:

```bash
git clone SecureEncoderMain
cd SecureEncoderMain
```

### Step 2: Build and Run the Container

Use Docker Compose to build and start the container:

```bash
docker-compose up --build
```

### Step 3: Accessing the Application

Open your browser and navigate to:

```bash
http://localhost:3000
```

### Stopping the Container

Open your browser and navigate to:

```bash
docker-compose down
```


## Notes
- Keep your cryptographic keys secure and ensure they are not exposed to unauthorized users.
- Regularly update dependencies to mitigate vulnerabilities associated with outdated libraries.
#
