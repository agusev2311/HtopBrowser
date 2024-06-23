# HtopBrowser

HtopBrowser is a web application that provides a graphical interface to monitor system processes and resource usage, similar to the command-line tool `htop`. The application is built using Flask, and it allows users to view system statistics and manage processes through a web browser.

## Features

- **Process Monitoring**: View a list of active processes along with their resource usage.
- **CPU Usage**: Monitor CPU usage for each core.
- **Memory Usage**: Visualize memory usage with progress bars.
- **Process Management**: Kill processes directly from the web interface.
- **User Authentication**: Secure access with a login system.

## Requirements

- Python 3.x
- Flask
- psutil
- BeautifulSoup4
- PyJWT

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/agusev2311/HtopBrowser.git
   cd HtopBrowser
   ```

2. **Install the required Python packages:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the secret key and user credentials:**
   - Create a file named `secret_key` and add a secret key.
     ```
     echo "your_secret_key" > secret_key
     ```
   - Create a file named `users` and add user credentials in the format `username password` for each user.
     ```
     echo "user1 password1" > users
     echo "user2 password2" >> users
     ```

4. **Run the application:**
   ```bash
   flask --app main run --host 0.0.0.0 --port 8000 --debug
   ```

## Usage

- Open your web browser and navigate to `http://localhost:8000`.
- Log in with your credentials.
- View system processes, CPU usage, and memory usage.
- Click on the ❌ icon next to a process to kill it.

## Project Structure

- **main.py**: The main Flask application file.
- **templates/**: Directory containing HTML templates.
  - **login.html**: Login page.
  - **index.html**: Main dashboard displaying system statistics.
- **static/**: Directory for static files such as CSS and JavaScript (if needed).

## Endpoints

- **GET /**: Redirects to `/index`.
- **GET /login**: Renders the login page.
- **POST /login**: Handles user login and sets JWT cookie.
- **GET /index**: Renders the main dashboard.
- **GET /table_css**: Returns the process table data.
- **GET /mem_info**: Returns memory information.
- **GET /mem_info_bar**: Returns memory usage bars.
- **GET /kill/<pid>**: Kills the process with the specified PID.
- **GET /cpu_info**: Returns CPU usage data.
- **GET /cpu_info_core/<core_numb>**: Returns CPU usage for a specific core.
- **GET /logout**: Logs out the user by clearing the JWT cookie.

## Security

- User authentication is handled using JWT (JSON Web Tokens).
- Ensure that the `secret_key` is kept secure and not exposed in the code.

---

Feel free to customize the project as per your requirements. Happy monitoring!
