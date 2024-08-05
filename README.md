# Netflix clone - BINGE HUB

## Project Description

This learning project is a simple Netflix clone. The user can register and log in and then stream videos. The registration should be verified by a confirmation email.

## Why is this project useful?

This is only a learning project. In general, however, a user can access content at any time and from anywhere.

## Contributing

We welcome contributions from the community! Here are some ways you can contribute:
- Report bugs: Open an issue with a detailed description of the problem.
- Suggest features: Propose new features that could enhance the project.
- Code contributions: Fork the project, make the desired changes, and send a pull request.

## Getting Help

If you have questions or run into problems, you can:
- Open an issue on GitHub

## Project Management and Contributions

This project is managed by B². The main contributors are:
- Benjamin Bennewitz (https://github.com/benjaminBennewitz) - Project lead and main developer


## Installation and Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/benjaminBennewitz/binge_hub_backend.git
    ```
2. Change to the project directory:
    ```bash
    cd binge_hub_backend
    ```
3. Create a virtual environment and install the dependencies:
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows: env\Scripts\activate
    pip install -r requirements.txt
    ```
4. Create .env file for email settings:
    ```
    create a new file in root directory named ".env". There you have to set up the email settings with your datas.

    EMAIL_HOST=smtp.office365.com
    EMAIL_PORT=587
    EMAIL_HOST_USER=your-email
    EMAIL_HOST_PASSWORD=your-password
    EMAIL_USE_TLS=True
    EMAIL_USE_SSL=False
    DEFAULT_FROM_EMAIL=your-email
    ```
5. Run the migrations:
    ```bash
    python manage.py migrate
    ```
6. Create Superuser
    ```bash
    python manage.py migrate
    ```
7. Change Site ID
    ```bash
    login to Django Backend with superuser an go to table "Sites", here you change example.com to localhost:8000
    ```
8. Start the Django development server:
    ```bash
    python manage.py runserver
    ```
9. Start the RQ server:
    First: start Redis in an Ubuntu (WSL) Terminal
    ```bash
    sudo service redis-server start
    ```
    Second: Check if Redis working
    ```bash
    redis-cli
    ping
    ANSWERS: PONG
    ```
10. Check URLS and Ports:
    ```right port/url
    make sure to use port :8000 for backend otherwhise some links doesnt work
    ```

## License

This project is licensed under the MIT License