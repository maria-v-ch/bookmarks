# User Management System

A Django-based user management system with role-based access control, social authentication, and automated backup functionality.

## Core Features

- User Authentication
  - Registration with email verification
  - Login with email or username
  - Password reset functionality
  - Google OAuth2 integration
  - Session management

- Role Management
  - Admin/User role separation
  - Role-based access control
  - Admin dashboard for user management
  - User promotion/demotion functionality

- Security
  - Password validation
  - Email uniqueness validation
  - Protected views with decorators
  - CSRF protection
  - Automatic profile creation

- Data Management
  - Automated database backups
  - Backup rotation (keeps last 5)
  - Backup restoration capability
  - SQLite/PostgreSQL support

## Technology Stack

- Python 3.12
- Django 5.0.1
- PostgreSQL/SQLite
- Docker & Docker Compose
- Coverage.py (86% test coverage)
- Social Auth for OAuth2

## Project Structure

```
bookmarks/
├── account/ # Main application
│ ├── management/ # Custom management commands
│ │ └── commands/ # Create superuser command
│ ├── static/ # Static files (CSS)
│ ├── templates/ # HTML templates
│ │ ├── account/ # App-specific templates
│ │ └── registration/ # Auth-related templates
│ ├── tests/ # Test modules
│ └── migrations/ # Database migrations
├── docker/ # Docker configuration files
└── bookmarks/ # Project configuration
```


## Quick Start

1. Clone and set up environment:
```bash
git clone https://github.com/yourusername/bookmarks.git
cd bookmarks
cp .env.example .env
```


2. Configure environment variables in `.env` following template in example.env.


3. Build and start services:
```bash
chmod +x docker-commands.sh
./docker-commands.sh build
```


4. Access the application:

```bash
http://localhost:8004
```

## Development Commands

- Start services:
```bash
./docker-commands.sh start
```
- Rebuild containers:
```bash
./docker-commands.sh build
```
- Create database backup:
```bash
./docker-commands.sh backup
```
- Run tests:
```bash
./docker-commands.sh test
```


## Testing

The project maintains 93% test coverage including:
- Model tests (Profile creation, admin roles)
- View tests (authentication, registration, permissions)
- Form validation tests
- Integration tests
- Command tests

## Key Features

### User Management
- Registration with email verification
- Login/logout functionality
- Password reset capability
- Profile editing
- Google OAuth2 integration

### Admin Features
- User role management
- Admin dashboard
- User promotion/demotion
- User list view

### Security
- Password validation
- Email uniqueness checks
- Protected views
- CSRF protection
- Role-based access control

### Data Management
- Automated backups
- Backup rotation (last 5 kept)
- PostgreSQL database
- Docker volume persistence

## Architecture

- **Frontend**: Django templates, CSS
- **Backend**: Django 5.0.1
- **Database**: PostgreSQL 13
- **Container**: Docker & Docker Compose
- **Authentication**: Django Auth + Social Auth
- **Testing**: Django Test + Coverage.py

## Best Practices

- PEP 8 compliant code
- Comprehensive docstrings
- Automated testing
- Separation of concerns
- Environment configuration
- Secure credential handling

## Production Considerations

1. Security:
   - Change default credentials
   - Set DEBUG=False
   - Configure allowed hosts
   - Use strong passwords
   - Enable HTTPS

2. Backup:
   - Configure off-site backup storage
   - Set up backup monitoring
   - Test restore procedures

3. Monitoring:
   - Set up error tracking
   - Monitor system resources
   - Configure logging

## License

MIT License - see LICENSE file for details

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request

## Support

For support, please open an issue in the GitHub repository.