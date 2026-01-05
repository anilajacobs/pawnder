# Pawnder - Deployment Guide

Complete guide to deploying your Django pet dating application to production.

## 📋 Pre-Deployment Checklist

Before deploying, prepare your project:

### 1. Update Settings for Production

Create a `production_settings.py` or modify `settings.py`:

```python
import os
from decouple import config
import dj_database_url

# Security Settings
DEBUG = config('DEBUG', default=False, cast=bool)
SECRET_KEY = config('SECRET_KEY')
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')

# Database - Use PostgreSQL in production
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}

# Static Files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media Files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Add WhiteNoise to middleware (for serving static files)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this
    # ... rest of middleware
]

# Security Headers
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
```

### 2. Update Requirements

Create `requirements-prod.txt`:
```
Django>=5.1
Pillow>=10.2.0
python-decouple==3.8
gunicorn==21.2.0
whitenoise==6.6.0
psycopg2-binary==2.9.9
dj-database-url==2.1.0
```

### 3. Create Environment Variables File

Create `.env` (never commit this):
```
SECRET_KEY=your-very-secret-key-here-generate-a-new-one
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgres://user:password@host:port/database
```

Generate a secret key:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## 🚀 Deployment Options

## Option 1: PythonAnywhere (Easiest)

**Best for:** Beginners, quick deployment, free tier
**Cost:** Free tier available, paid from $5/month
**Website:** https://www.pythonanywhere.com

### Steps:

1. **Sign Up**
   - Create free account at PythonAnywhere
   - No credit card required for free tier

2. **Upload Code**
   ```bash
   # On PythonAnywhere Bash console:
   git clone https://github.com/yourusername/pawnder.git
   # OR upload via Files tab
   ```

3. **Setup Virtual Environment**
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 pawnder
   cd pawnder
   pip install -r requirements.txt
   ```

4. **Configure Web App**
   - Go to "Web" tab
   - Click "Add a new web app"
   - Choose "Manual configuration" → Python 3.10
   - Set source code: `/home/yourusername/pawnder`
   - Set working directory: `/home/yourusername/pawnder`

5. **Edit WSGI File**
   Click on WSGI configuration file and replace with:
   ```python
   import os
   import sys

   path = '/home/yourusername/pawnder'
   if path not in sys.path:
       sys.path.append(path)

   os.environ['DJANGO_SETTINGS_MODULE'] = 'pawnder_project.settings'

   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```

6. **Configure Static/Media Files**
   In Web tab, add:
   - URL: `/static/` → Directory: `/home/yourusername/pawnder/staticfiles/`
   - URL: `/media/` → Directory: `/home/yourusername/pawnder/media/`

7. **Run Migrations**
   ```bash
   cd /home/yourusername/pawnder
   python manage.py migrate
   python manage.py collectstatic
   python manage.py createsuperuser
   ```

8. **Reload Web App**
   - Click green "Reload" button in Web tab
   - Visit: `yourusername.pythonanywhere.com`

---

## Option 2: Railway (Modern & Easy)

**Best for:** Automatic deployments, modern workflow
**Cost:** Free $5 credit/month, then pay-as-you-go
**Website:** https://railway.app

### Steps:

1. **Prepare Your Project**

Create `Procfile`:
```
web: gunicorn pawnder_project.wsgi --log-file -
```

Create `runtime.txt`:
```
python-3.11.0
```

Update `requirements.txt`:
```
Django>=5.1
Pillow>=10.2.0
python-decouple==3.8
gunicorn==21.2.0
whitenoise==6.6.0
psycopg2-binary==2.9.9
dj-database-url==2.1.0
```

2. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/pawnder.git
   git push -u origin main
   ```

3. **Deploy on Railway**
   - Sign up at railway.app
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway auto-detects Django

4. **Add PostgreSQL Database**
   - In your project, click "New" → "Database" → "PostgreSQL"
   - Railway automatically sets DATABASE_URL

5. **Set Environment Variables**
   - Go to your service → Variables
   - Add:
     ```
     SECRET_KEY=your-secret-key
     DEBUG=False
     ALLOWED_HOSTS=*.railway.app
     ```

6. **Run Initial Commands**
   ```bash
   # In Railway CLI or dashboard
   railway run python manage.py migrate
   railway run python manage.py createsuperuser
   railway run python manage.py collectstatic --noinput
   ```

7. **Access Your App**
   - Railway provides URL like: `pawnder-production.up.railway.app`

---

## Option 3: Heroku (Popular Choice)

**Best for:** Established platform, good documentation
**Cost:** Free tier discontinued, starts at $7/month
**Website:** https://www.heroku.com

### Steps:

1. **Install Heroku CLI**
   ```bash
   # Mac
   brew install heroku/brew/heroku

   # Windows
   # Download from heroku.com
   ```

2. **Prepare Project**

Create `Procfile`:
```
web: gunicorn pawnder_project.wsgi
```

Create `runtime.txt`:
```
python-3.11.0
```

3. **Login and Create App**
   ```bash
   heroku login
   heroku create pawnder-app
   ```

4. **Add PostgreSQL**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

5. **Set Environment Variables**
   ```bash
   heroku config:set SECRET_KEY='your-secret-key'
   heroku config:set DEBUG=False
   heroku config:set ALLOWED_HOSTS='pawnder-app.herokuapp.com'
   ```

6. **Deploy**
   ```bash
   git push heroku main
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   heroku run python manage.py collectstatic --noinput
   ```

7. **Open App**
   ```bash
   heroku open
   ```

---

## Option 4: DigitalOcean App Platform

**Best for:** Balanced ease and control
**Cost:** $5-12/month
**Website:** https://www.digitalocean.com

### Steps:

1. **Sign Up** at DigitalOcean

2. **Create App**
   - Apps → Create App
   - Connect GitHub repository
   - Choose branch

3. **Configure Build**
   - Detected as Python app
   - Build command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - Run command: `gunicorn pawnder_project.wsgi`

4. **Add Database**
   - Add PostgreSQL database component
   - Automatically connects via DATABASE_URL

5. **Environment Variables**
   - Add in App Settings
   - SECRET_KEY, DEBUG, ALLOWED_HOSTS

6. **Deploy**
   - Click Deploy
   - Auto-deploys on every push to main branch

---

## Option 5: AWS (Most Control)

**Best for:** Large scale, full control
**Cost:** Variable, can start free
**Complexity:** High

### Services Needed:
- EC2 (server)
- RDS (PostgreSQL database)
- S3 (media files)
- CloudFront (CDN)
- Route 53 (DNS)

**Recommended:** Use Elastic Beanstalk for easier AWS deployment

---

## Option 6: VPS (Full Control)

**Best for:** Complete control, custom setup
**Providers:** DigitalOcean Droplets, Linode, Vultr
**Cost:** $5-10/month

### Stack:
- Ubuntu 22.04 LTS
- Nginx (web server)
- Gunicorn (WSGI server)
- PostgreSQL (database)
- Supervisor (process control)

### Quick Setup:

1. **Create Droplet** (DigitalOcean example)

2. **SSH into Server**
   ```bash
   ssh root@your-server-ip
   ```

3. **Install Dependencies**
   ```bash
   apt update
   apt install python3-pip python3-venv nginx postgresql postgresql-contrib
   ```

4. **Setup Application**
   ```bash
   cd /var/www
   git clone your-repo pawnder
   cd pawnder
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. **Configure PostgreSQL**
   ```bash
   sudo -u postgres psql
   CREATE DATABASE pawnder;
   CREATE USER pawnder_user WITH PASSWORD 'yourpassword';
   GRANT ALL PRIVILEGES ON DATABASE pawnder TO pawnder_user;
   \q
   ```

6. **Configure Gunicorn**
   Create `/etc/systemd/system/gunicorn.service`:
   ```ini
   [Unit]
   Description=Gunicorn daemon for Pawnder
   After=network.target

   [Service]
   User=www-data
   Group=www-data
   WorkingDirectory=/var/www/pawnder
   ExecStart=/var/www/pawnder/venv/bin/gunicorn \
             --workers 3 \
             --bind unix:/var/www/pawnder/pawnder.sock \
             pawnder_project.wsgi:application

   [Install]
   WantedBy=multi-user.target
   ```

7. **Configure Nginx**
   Create `/etc/nginx/sites-available/pawnder`:
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;

       location = /favicon.ico { access_log off; log_not_found off; }

       location /static/ {
           root /var/www/pawnder;
       }

       location /media/ {
           root /var/www/pawnder;
       }

       location / {
           include proxy_params;
           proxy_pass http://unix:/var/www/pawnder/pawnder.sock;
       }
   }
   ```

8. **Enable and Start Services**
   ```bash
   systemctl start gunicorn
   systemctl enable gunicorn
   ln -s /etc/nginx/sites-available/pawnder /etc/nginx/sites-enabled
   systemctl restart nginx
   ```

---

## 📊 Comparison Table

| Platform | Difficulty | Cost/Month | Free Tier | Auto-Deploy | Best For |
|----------|-----------|------------|-----------|-------------|----------|
| **PythonAnywhere** | ⭐ Easy | $0-5 | ✅ Yes | ❌ No | Beginners |
| **Railway** | ⭐⭐ Easy | $0-10 | ✅ $5 credit | ✅ Yes | Modern apps |
| **Heroku** | ⭐⭐ Easy | $7+ | ❌ No | ✅ Yes | Quick deploy |
| **DigitalOcean App** | ⭐⭐ Medium | $5-12 | ❌ No | ✅ Yes | Balanced |
| **VPS** | ⭐⭐⭐ Hard | $5-10 | ❌ No | ❌ No | Full control |
| **AWS** | ⭐⭐⭐⭐ Very Hard | Variable | ✅ Limited | ❌ Manual | Enterprise |

---

## 🔒 Production Security Checklist

Before going live:

- [ ] Set `DEBUG = False`
- [ ] Use strong `SECRET_KEY` (generate new one)
- [ ] Configure `ALLOWED_HOSTS` properly
- [ ] Use PostgreSQL (not SQLite)
- [ ] Enable HTTPS/SSL
- [ ] Set secure cookies (`SESSION_COOKIE_SECURE = True`)
- [ ] Configure CSRF protection
- [ ] Set up proper logging
- [ ] Use environment variables for secrets
- [ ] Configure proper file upload limits
- [ ] Set up database backups
- [ ] Configure email for password resets
- [ ] Add rate limiting
- [ ] Set up monitoring (Sentry, etc.)

---

## 📧 Email Configuration

For password resets and notifications, add to settings:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = 'Pawnder <noreply@pawnder.com>'
```

---

## 🗄️ Media Files in Production

For production, consider using:
- **AWS S3** (most popular)
- **DigitalOcean Spaces**
- **Cloudinary** (image-specific)

Install django-storages:
```bash
pip install django-storages boto3
```

---

## 📈 Monitoring & Maintenance

**Recommended Tools:**
- **Sentry** - Error tracking
- **New Relic** - Performance monitoring
- **Uptime Robot** - Uptime monitoring
- **Google Analytics** - User analytics

---

## 🎯 Recommended for Pawnder

**For Learning/Portfolio:** PythonAnywhere (Free)
**For Production:** Railway or DigitalOcean App Platform
**For Scale:** AWS with proper configuration

---

## 💡 Next Steps After Deployment

1. Set up custom domain
2. Configure SSL certificate (Let's Encrypt)
3. Set up automated backups
4. Configure email sending
5. Add monitoring
6. Set up CI/CD pipeline
7. Create staging environment

---

## 🆘 Troubleshooting Common Issues

**Static files not loading:**
```bash
python manage.py collectstatic --noinput
```

**Database connection errors:**
- Check DATABASE_URL is set correctly
- Verify database credentials
- Ensure database accepts connections

**502 Bad Gateway:**
- Check Gunicorn is running
- Verify socket/port configuration
- Check application logs

**Media files not uploading:**
- Check MEDIA_ROOT permissions
- Verify MEDIA_URL configuration
- Consider moving to S3

---

Need help with specific deployment? Let me know which platform you'd like to use!
