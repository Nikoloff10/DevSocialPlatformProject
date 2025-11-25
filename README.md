# DevSocialPlatform Project

A Django-based social platform for developers with forum discussions, job postings, and user profiles.

## Features

- 🏗️ **Django 5.2.5** with PostgreSQL database
- 🎨 **TailwindCSS** for modern styling
- ☁️ **Cloudinary** for image storage
- 🔄 **Celery** for background tasks
- 🐳 **Docker** containerization
- 👤 **User authentication** with Django Allauth
- 💬 **Forum discussions** (Tech Nerds & Dev Problems)
- 💼 **Job postings** with bookmarking
- 📱 **Responsive design**

## Quick Start with Docker

### Prerequisites
- Docker and Docker Compose installed
- Git

### Development Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd DevSocialPlatformProject
   ```

2. **Copy environment file:**
   ```bash
   cp .env.example .env
   ```

3. **Edit `.env` file with your credentials:**
   - Set your PostgreSQL password
   - Add your Cloudinary credentials
   - Generate a new Django secret key

4. **Build and run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

5. **Run migrations (in another terminal):**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

6. **Create superuser:**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

7. **Access the application:**
   - Website: http://localhost:8000
   - Admin: http://localhost:8000/admin

### Production Deployment

1. **Copy production environment file:**
   ```bash
   cp .env.example .env.prod
   ```

2. **Edit `.env.prod` with production values:**
   - Set `DEBUG=False`
   - Use strong passwords
   - Add your domain to `ALLOWED_HOSTS`

3. **Deploy with production compose:**
   ```bash
   docker-compose -f docker-compose.prod.yml up --build -d
   ```

### Services

- **web**: Django application server
- **db**: PostgreSQL database
- **redis**: Redis for Celery background tasks
- **celery**: Celery worker for async tasks
- **nginx**: (Production only) Reverse proxy and static file server

## Manual Setup (without Docker)

### Prerequisites
- Python 3.13+
- PostgreSQL
- Node.js and npm
- Redis (for Celery)

### Installation

1. **Create virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

4. **Build TailwindCSS:**
   ```bash
   npm run build:css
   ```

5. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

6. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

7. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```

8. **Run development server:**
   ```bash
   python manage.py runserver
   ```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DB_NAME` | PostgreSQL database name | devsocialplatform |
| `DB_USER` | PostgreSQL username | postgres |
| `DB_PASSWORD` | PostgreSQL password | - |
| `DB_HOST` | PostgreSQL host | localhost |
| `DB_PORT` | PostgreSQL port | 5432 |
| `SECRET_KEY` | Django secret key | - |
| `DEBUG` | Debug mode | False |
| `ALLOWED_HOSTS` | Allowed hosts (comma-separated) | - |
| `CLOUDINARY_CLOUD_NAME` | Cloudinary cloud name | - |
| `CLOUDINARY_API_KEY` | Cloudinary API key | - |
| `CLOUDINARY_API_SECRET` | Cloudinary API secret | - |

## Project Structure

```
DevSocialPlatformProject/
├── DevSocialPlatformProject/    # Django project settings
├── devsearchey/                 # Main Django app
├── templates/                   # HTML templates
├── static/                      # Static files (CSS, JS, images)
├── media/                       # User uploads
├── docker-compose.yml           # Development Docker setup
├── docker-compose.prod.yml      # Production Docker setup
├── Dockerfile                   # Development Docker image
├── Dockerfile.prod              # Production Docker image
├── requirements.txt             # Python dependencies
├── package.json                 # Node.js dependencies
└── manage.py                    # Django management script
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request


