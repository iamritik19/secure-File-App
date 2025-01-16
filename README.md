# secure-File-App
# Project Documentation

## Overview
This project about file management system designed to manage file uploads and downloads securely. The system distinguishes between two user types:

1. **Ops Users**: Responsible for uploading files to the system.
2. **Client Users**: Can view and download files uploaded by Ops users through secure links.

The application employs **session-based authentication** and uses **SQLite3** as the database backend during development.

---

## Key Concepts and Components

### 1. **User Authentication and Authorization**
- **Session-Based Authentication**:
  - The application uses Django's built-in session-based authentication mechanism.
  - Sessions are used to store the user's authentication state on the server side after logging in.
  - This approach ensures that sensitive credentials are not exposed to the client.

- **User Types**:
  - **Ops Users**: Allowed to upload files and view the list of uploaded files. They cannot download files.
  - **Client Users**: Allowed to view and download files uploaded by Ops users. Each file is accessed through a secure, encrypted URL.

- **Access Control**:
  - Middleware and decorators are used to ensure that users can only access pages and functionalities authorized for their user type.

### 2. **File Upload and Storage**
- **Upload Workflow**:
  - Ops users upload files through an HTML form that validates the file type and size.
  - Allowed file types are restricted to `.pptx`, `.docx`, and `.xlsx` for security and compatibility.
  - Files are saved in the `media` directory on the server, with metadata stored in the database.

- **Validation**:
  - File type validation ensures that only permitted file types are uploaded.
  - File size validation restricts files to a maximum size (e.g., 5 MB).

### 3. **Secure File Download**
- **Secure Links**:
  - When a client user views the files, each file is accompanied by a secure, encrypted URL generated using Django's `signing` module.
  - This prevents unauthorized users from accessing files by guessing URLs.

- **Access Restrictions**:
  - Only client users can access the secure download links.
  - Attempts by Ops users or unauthenticated users to use the download URLs result in an access denial.

### 4. **Database**
- The project uses **SQLite3** as the database during development.
  - Lightweight and easy to set up for development purposes.
  - Stores user information, uploaded file metadata, and other related data.

- Key Tables:
  - **User Table**: Stores information about users, including their username, password (hashed), email, and user type.
  - **File Table**: Stores metadata about uploaded files, such as the file name, upload timestamp, and the user who uploaded it.

### 5. **Frontend**
- **Ops Dashboard**:
  - Ops users can upload files and view a list of all uploaded files.
  - Download functionality is disabled for Ops users.

- **Client Dashboard**:
  - Displays all uploaded files with secure download links.
  - Links are generated dynamically and expire after a certain period or become invalid if tampered with.

- **HTML Templates**:
  - Simple HTML templates are used with Django's template engine for rendering forms and displaying data dynamically.
  - Templates include CSRF tokens for securing POST requests.

### 6. **Validation and Error Handling**
- The system includes robust validation mechanisms to ensure secure and correct functionality:
  - Input validation for file type and size during uploads.
  - Authentication checks to ensure only logged-in users can access dashboards.
  - Authorization checks to enforce user-type-specific restrictions.

- User-friendly error messages and JSON responses are provided for invalid requests.

### 7. **Testing**
- Test cases verify the correctness of critical functionalities:
  - User login and logout.
  - File uploads and secure link generation.
  - Access control for unauthorized users.

- Django’s testing framework is used to create and run these test cases.

---

## Deployment Strategy
### Steps for Production Deployment:
1. **Setup Production Environment**:
   - Use a production-grade database like PostgreSQL for scalability and reliability.
   - Configure the application to use a web server like Nginx and a WSGI server like Gunicorn.

2. **Secure the Application**:
   - Use HTTPS for encrypted communication.
   - Secure sensitive configurations like database credentials and secret keys using environment variables or a secret management service.

3. **Static and Media Files**:
   - Serve static files using a CDN or web server.
   - Store media files in a cloud storage solution (e.g., AWS S3) for scalability.

4. **Testing and Debugging**:
   - Ensure all test cases pass before deployment.
   - Use tools like Sentry to monitor errors in the production environment.

5. **Continuous Deployment**:
   - will use CI/CD pipelines to automate testing, building, and deployment of the application.

6. **Monitoring and Maintenance**:
   - Monitor the application's performance and logs using tools like Prometheus and Grafana.
   - Schedule regular backups of the database and media files.

---

## Future Enhancements
- **File Previews**: Enable clients to preview files before downloading.
- **Cloud Deployment**: Deploy the application on a cloud platform like AWS or Azure for better scalability.
- **Email Notifications**: Notify users via email when new files are uploaded.

---

