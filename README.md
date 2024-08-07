# Secure Encoder

![Screen Capture](screen_capture.JPG)


## Project Statistics

[![Stargazers][stars-shield]][stars-url]
[![Forks][forks-shield]][forks-url]
[![Follow][follow-shield]][follow-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

[![Issues][issues-shield]][issues-url]
[![Pull Requests][pulls-shield]][pulls-url]
[![Contributors][contributors-shield]][contributors-url]
[![License][license-shield]][license-url]


## Continuous Integration Status

[![Codecov][codecov-shield]][codecov-url]
[![Codacy][codacy-shield]][codacy-url]
[![CodeQL][codeql-shield]][codeql-url]
[![CI][ci-shield]][ci-url]


## Supported Languages

[![Python](https://img.shields.io/badge/python-3.9_|_3.10-3572A5)](SecureEncoderFlask\requirements.txt)
[![Typescript](https://img.shields.io/badge/typescript-^5.4.5-3178c6)](SecureEncoderReact\package.json)


## Table of Contents
- [Secure Encoder](#secure-encoder)
	- [Project Statistics](#project-statistics)
	- [Continuous Integration Status](#continuous-integration-status)
	- [Supported Languages](#supported-languages)
	- [Table of Contents](#table-of-contents)
	- [Introduction](#introduction)
	- [Features](#features)
	- [Tech Stack](#tech-stack)
	- [Project Setup](#project-setup)
		- [Prerequisites](#prerequisites)
		- [Environment Setup](#environment-setup)
		- [Running the Application in Separate Terminals](#running-the-application-in-separate-terminals)
			- [Backend](#backend)
			- [Frontend](#frontend)
- [React Frontend with Docker Compose](#react-frontend-with-docker-compose)
	- [Prerequisites](#prerequisites-1)
	- [Getting Started](#getting-started)
		- [Step 1: Build and Run the Container](#step-1-build-and-run-the-container)
		- [Step 2: Accessing the Application](#step-2-accessing-the-application)
		- [Stopping the Container](#stopping-the-container)
	- [Notes](#notes)
	- [Contributing](#contributing)
	- [License](#license)
- [](#)


## Introduction
**Secure Encoder** is a sophisticated web application crafted to provide robust encoding and decryption capabilities using various cryptographic algorithms, including AES and RSA. The application supports a variety of operations such as Base64, Hex, UTF-8, Latin-1, ASCII, and URL encoding/decoding.

Its primary goal is to offer a user-friendly interface for secure text manipulation, catering especially to developers and security professionals who require reliable and secure methods for data manipulation in web applications. This makes it particularly useful for those who need quick encoding and decoding solutions alongside robust encryption tools to ensure data safety.

Developed using Python Flask and React, and leveraging SQLalchemy with Vite and Tailwind CSS for the front end, Secure Encoder exemplifies the effective use of test-driven development (TDD) practices, advanced data structures and algorithms, and expert deployment techniques.

## Features
- [x] **Dynamic Encoding/Decoding:** Support for multiple encoding schemes including Base64, Hex, and more.
- [x] **Encryption and Decryption:** Implements AES and RSA algorithms with key management for secure data handling.
- [x] **File Uploads:** Users can upload key files needed for encryption/decoding.
- [x] **Interactive UI:** The React-based interactive UI ensures a smooth user experience.
- [x] **Security:** Implements best practices like Content Security Policy headers.

## Tech Stack

<div align="center">

| Component      | Technology Used            | Description                               |
|----------------|----------------------------|-------------------------------------------|
| Frontend       | React.js, TypeScript       | Interactive UI built with React           |
| Backend        | Flask (Python)             | Server-side logic handled by Flask        |
| CSS Framework  | Tailwind                   | Styling provided by Tailwind CSS          |
| Database       | sqlalchemy                 | ORM for database interactions (if used)   |
| CI/CD          | Codecov, Codacy, CodeQL                   | Continuous integration and deployment     |
| Containerization | Docker, Docker Compose (optional)   | Container setup for development and production environments |

</div>

## Project Setup

### Prerequisites
- [Node.js](https://nodejs.org/en/) (v14 or later)
- [npm (Node Package Manager)](https://www.npmjs.com/)
- [Python](https://www.python.org/downloads/) (3.8 or later)

### Environment Setup
1. Clone the repository:
   ```bash
   git clone git@github.com:clchinkc/SecureEncoder.git
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
   npm run dev
   ```
   Build and start the built application:
   ```bash
   npm run build
   npm run serve
   ```
   Or to run the production build on local static server:
   ```bash
   npx serve -s build
   ```
   
   This will launch the web application on `http://localhost:3000` and connect it to the Flask backend.

# React Frontend with Docker Compose

>This project sets up a React frontend application using Docker and Docker Compose for development with hot reloading.

## Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

>Follow these instructions to get the React frontend application up and running in a Docker container.

### Step 1: Build and Run the Container

Use Docker Compose to build and start the container:

```bash
docker-compose up --build
```

### Step 2: Accessing the Application

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


## Contributing

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## License
Distributed under the MIT License. See `LICENSE.txt` for more information.

#


<!-- links -->
[your-project-path]: clchinkc/SecureEncoder
[stars-shield]: https://img.shields.io/github/stars/clchinkc/SecureEncoder.svg?style=flat-square
[stars-url]: https://github.com/clchinkc/SecureEncoder/stargazers
[forks-shield]: https://img.shields.io/github/forks/clchinkc/SecureEncoder.svg?style=flat-square
[forks-url]: https://github.com/clchinkc/SecureEncoder/network/members
[follow-shield]: https://img.shields.io/github/followers/clchinkc.svg?style=flat-square
[follow-url]: https://github.com/clchinkc
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/clchinkc

[issues-shield]: https://img.shields.io/github/issues/clchinkc/SecureEncoder.svg?style=flat-square
[issues-url]: https://img.shields.io/github/issues/clchinkc/SecureEncoder.svg
[pulls-shield]: https://img.shields.io/github/issues-pr/clchinkc/SecureEncoder
[pulls-url]: https://img.shields.io/github/issues-pr/clchinkc/SecureEncoder
[contributors-shield]: https://img.shields.io/github/contributors/clchinkc/SecureEncoder.svg?style=flat-square
[contributors-url]: https://github.com/clchinkc/SecureEncoder/graphs/contributors
[license-shield]: https://img.shields.io/github/license/clchinkc/SecureEncoder.svg?style=flat-square
[license-url]: https://github.com/clchinkc/SecureEncoder/blob/master/LICENSE.txt

[codecov-shield]: https://codecov.io/gh/clchinkc/SecureEncoder/branch/main/graph/badge.svg
[codecov-url]: https://codecov.io/gh/clchinkc/SecureEncoder
[codacy-shield]: https://app.codacy.com/project/badge/Grade/9b63875ab1164fc2a2a8a774c95399aa
[codacy-url]: https://app.codacy.com/gh/clchinkc/SecureEncoder/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade
[codeql-shield]: https://github.com/clchinkc/SecureEncoder/actions/workflows/codeql-analysis.yml/badge.svg
[codeql-url]: https://github.com/clchinkc/SecureEncoder/actions/workflows/codeql-analysis.yml
[ci-shield]: https://github.com/clchinkc/SecureEncoder/actions/workflows/test-and-converage.yml/badge.svg
[ci-url]: https://github.com/clchinkc/SecureEncoder/actions/workflows/test-and-converage.yml

