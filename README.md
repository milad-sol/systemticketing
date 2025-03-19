# Django Ticket System

A comprehensive ticket management system built with Django that allows users to create, track, and resolve support tickets.

## Features

- **User Authentication**: Register, login, and manage user profiles
- **Role-Based Access**: Different dashboards for regular users and staff members
- **Ticket Management**: Create, view, update, and close support tickets
- **File Attachments**: Upload files with tickets and messages
- **Messaging System**: Communicate about tickets through a threaded messaging interface
- **Form Validation**: Robust validation for all user inputs
- **Bootstrap Integration**: Clean, responsive user interface

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/milad-sol/django-ticket-system.git
   cd django-ticket-system
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```
   python manage.py migrate
   ```

5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

7. Access the application at http://127.0.0.1:8000/

## Project Structure

```
django-ticket-system/
├── ticket_system/           # Main Django project folder
│   ├── settings.py          # Project settings
│   ├── urls.py              # Main URL configuration
│   └── wsgi.py              # WSGI configuration
├── tickets/                 # Ticket application
│   ├── forms.py             # Form definitions
│   ├── models.py            # Data models
│   ├── views.py             # View logic
│   ├── urls.py              # URL patterns
│   └── templates/           # HTML templates
├── static/                  # Static files (CSS, JS, images)
└── media/                   # User-uploaded files
```

## Key Components

### Models

- **Ticket**: Stores ticket information including subject, description, status, and file attachments
- **Messages**: Handles communication related to tickets

### Forms

- **UserLoginForm**: Handles user authentication
- **UserRegisterForm**: Manages user registration with validation
- **CreateTicketForm**: Creates new support tickets
- **MessageForm**: Adds messages to existing tickets

### Views

- **Authentication Views**: Handle login, registration, and logout functionality
- **Ticket Management Views**: Create, list, detail, and update tickets
- **Dashboard Views**: Provide different interfaces for users and staff

## Usage

### User Workflow

1. **Register/Login**: Create an account or login with existing credentials
2. **Create Ticket**: Submit a new support ticket with a subject, description, and optional file attachment
3. **View Tickets**: See all your submitted tickets and their current status
4. **Add Messages**: Communicate with support staff by adding messages to your ticket
5. **Close Ticket**: Mark a ticket as resolved when your issue is fixed

### Staff Workflow

1. **Login**: Access the staff dashboard
2. **View All Tickets**: See tickets from all users
3. **Respond to Tickets**: Add messages and update ticket status
4. **Assign Tickets**: Take ownership of specific tickets
5. **Close Resolved Tickets**: Mark tickets as complete when issues are resolved

## Customization

### Adding New Ticket Statuses

1. Update the `STATUS_CHOICES` in the `Ticket` model
2. Run migrations to apply changes:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

### Extending User Profiles

1. Create a custom user model or profile model
2. Update authentication views to include additional fields
3. Modify templates to display new user information

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin new-feature`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Django framework: https://www.djangoproject.com/
- Bootstrap: https://getbootstrap.com/
