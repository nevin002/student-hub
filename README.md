# StudentHub - Complete Django Student Collaboration Platform

A comprehensive, resume-ready Django application that provides a complete platform for student collaboration, resource sharing, expense management, and blogging.

## 🚀 Features

### 🔐 Authentication & Profiles
- **User Registration & Login**: Secure signup with email verification and auto-login
- **Profile Management**: Every user gets an automatic profile with avatar and bio
- **Avatar System**: Choose from preloaded avatars or upload custom ones
- **Flash Messages**: Bootstrap-styled notifications for all user actions

### 📚 Resource Sharing
- **File & Link Sharing**: Upload files or share external links
- **Tagging System**: Organize resources with custom tags
- **Search & Filter**: Find resources by title, description, or tags
- **Upvoting**: Like and discover popular resources
- **Comments**: Discuss and provide feedback on resources
- **Pagination**: Browse through resources efficiently (10 per page)

### 💰 Expense Tracking
- **Equal Split Calculator**: Automatically calculate per-person costs
- **Balance Tracking**: See your net balance (paid vs. owed)
- **Participant Management**: Add multiple people to expense splits
- **Visual Dashboard**: Clear overview of all your expenses

### 📝 Student Blog
- **Post Creation**: Share thoughts, experiences, and insights
- **Comment System**: Engage with other students' posts
- **Search Functionality**: Find posts by title or content
- **Pagination**: Browse through posts efficiently
- **Author Profiles**: See who wrote what and when

### 🎨 Modern UI/UX
- **Bootstrap 5**: Responsive, mobile-first design
- **Bootstrap Icons**: Professional iconography throughout
- **Responsive Layout**: Works perfectly on all devices
- **Clean Navigation**: Intuitive user experience

## 🛠️ Tech Stack

- **Backend**: Django 4.x (Python 3.10+)
- **Database**: SQLite (development), PostgreSQL ready (production)
- **Frontend**: Bootstrap 5, HTML5, CSS3
- **File Handling**: Django FileField with media serving
- **Authentication**: Django's built-in auth system
- **Forms**: Django Forms with Bootstrap styling
- **Templates**: Django Template Language with inheritance

## 📁 Project Structure

```
studenthub/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── README.md                # This file
├── studenthub/              # Django project settings
│   ├── __init__.py
│   ├── settings.py          # Project configuration
│   ├── urls.py              # Main URL routing
│   └── wsgi.py              # WSGI configuration
├── accounts/                 # Authentication & profiles app
│   ├── models.py            # Profile model
│   ├── views.py             # Auth views
│   ├── forms.py             # Signup form
│   ├── signals.py           # Auto-profile creation
│   ├── urls.py              # Auth URL patterns
│   └── admin.py             # Admin interface
├── resources/                # Resource sharing app
│   ├── models.py            # Resource, Tag, Comment models
│   ├── views.py             # Resource views
│   ├── forms.py             # Resource forms
│   ├── urls.py              # Resource URL patterns
│   └── admin.py             # Admin interface
├── expenses/                 # Expense tracking app
│   ├── models.py            # Expense model
│   ├── views.py             # Expense views
│   ├── forms.py             # Expense forms
│   ├── urls.py              # Expense URL patterns
│   └── admin.py             # Admin interface
├── blog/                     # Student blog app
│   ├── models.py            # Post, PostComment models
│   ├── views.py             # Blog views
│   ├── forms.py             # Blog forms
│   ├── urls.py              # Blog URL patterns
│   └── admin.py             # Admin interface
├── templates/                # HTML templates
│   ├── base.html            # Base template with navigation
│   ├── home.html            # Homepage
│   ├── signup.html          # Registration page
│   ├── login.html           # Login page
│   ├── choose_avatar.html   # Avatar selection
│   ├── resources/           # Resource templates
│   ├── expenses/            # Expense templates
│   └── blog/                # Blog templates
├── media/                    # User-uploaded files
│   └── avatars/             # User avatar images
└── static/                   # Static files (CSS, JS, images)
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd studenthub_full
   ```

2. **Create virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Navigate to Django project**
   ```bash
   cd studenthub
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Open your browser**
   Navigate to `http://127.0.0.1:8000/`

## 👤 Adding Avatars

To add more avatar options for users:

1. **Place image files** in the `media/avatars/` directory
2. **Supported formats**: PNG, JPG, JPEG, GIF
3. **Recommended size**: 200x200 pixels or larger
4. **File naming**: Use descriptive names (e.g., `student1.png`, `graduate.jpg`)

The system will automatically detect new avatar files and make them available in the avatar selection page.

## 🔧 Configuration

### Environment Variables
The project is configured for development by default. For production:

1. Set `DEBUG = False` in `settings.py`
2. Configure `ALLOWED_HOSTS`
3. Use environment variables for `SECRET_KEY`
4. Set up proper database (PostgreSQL recommended)
5. Configure static and media file serving

### Database
- **Development**: SQLite (default)
- **Production**: PostgreSQL (recommended)

## 📱 Available Endpoints

### Public Routes
- `/` - Homepage
- `/accounts/login/` - Login page
- `/accounts/signup/` - Registration page
- `/resources/` - Browse resources
- `/blog/` - Read blog posts

### Protected Routes (Login Required)
- `/accounts/avatars/` - Choose avatar
- `/resources/new/` - Create resource
- `/expenses/` - Manage expenses
- `/expenses/new/` - Create expense
- `/blog/new/` - Write blog post

### Admin
- `/admin/` - Django admin interface

## 🧪 Testing

Run the test suite:
```bash
python manage.py test
```

## 🚀 Deployment

### Production Checklist
- [ ] Set `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use environment variables for secrets
- [ ] Set up PostgreSQL database
- [ ] Configure static file serving
- [ ] Set up media file serving (S3 recommended)
- [ ] Use HTTPS
- [ ] Set up logging
- [ ] Configure backup strategy

### Recommended Hosting
- **Heroku**: Easy deployment with PostgreSQL add-on
- **DigitalOcean**: VPS with managed database
- **AWS**: EC2 with RDS and S3
- **PythonAnywhere**: Django-specific hosting

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🎯 Resume Highlights

This project demonstrates:
- **Full-Stack Development**: Complete Django application with modern frontend
- **Database Design**: Complex models with relationships and custom methods
- **User Authentication**: Secure login system with profile management
- **File Handling**: File uploads and media serving
- **API Design**: RESTful URL structure and views
- **Frontend Development**: Responsive Bootstrap 5 interface
- **Testing**: Comprehensive test coverage
- **Deployment Ready**: Production-ready configuration

## 📞 Support

For questions or support:
- Create an issue in the repository
- Check the Django documentation
- Review the code comments for implementation details

---

**Built with ❤️ using Django and Bootstrap 5**
