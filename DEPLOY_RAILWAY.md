# Deploy Pawnder to Railway (Easiest Option)

Railway is the easiest modern platform to deploy Django. Follow these steps:

## ⚡ Quick Deploy (5 minutes)

### Step 1: Prepare Your Code

Your project is already set up! These files are ready:
- ✅ `Procfile` - Tells Railway how to run your app
- ✅ `runtime.txt` - Specifies Python version
- ✅ `requirements-prod.txt` - Production dependencies

### Step 2: Push to GitHub

```bash
# Initialize git (if not done)
cd /Users/anilajacob/Documents/pawnder
git init

# Add all files
git add .

# Make first commit
git commit -m "Initial Pawnder project"

# Create a GitHub repository at github.com
# Then connect it:
git remote add origin https://github.com/YOUR-USERNAME/pawnder.git
git branch -M main
git push -u origin main
```

### Step 3: Deploy on Railway

1. **Sign up** at https://railway.app (free with GitHub)

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `pawnder` repository
   - Railway will auto-detect it as a Python app

3. **Add PostgreSQL Database**
   - In your project, click "New"
   - Select "Database" → "Add PostgreSQL"
   - Railway automatically connects it!

4. **Set Environment Variables**
   Click on your web service → "Variables" tab → Add:

   ```
   SECRET_KEY=your-generated-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=*.railway.app
   DJANGO_SETTINGS_MODULE=pawnder_project.production_settings
   ```

   To generate SECRET_KEY, run locally:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

5. **Deploy!**
   - Railway automatically deploys
   - Wait 2-3 minutes for build
   - Check deployment logs

### Step 4: Run Initial Setup

After first deployment, run these commands in Railway's terminal (or use Railway CLI):

```bash
# Install Railway CLI (optional but useful)
npm install -g @railway/cli

# Login
railway login

# Link to your project
railway link

# Run migrations
railway run python manage.py migrate

# Create superuser
railway run python manage.py createsuperuser

# Collect static files
railway run python manage.py collectstatic --noinput

# Load sample data (optional)
railway run python manage.py populate_sample_data
```

### Step 5: Access Your App

Railway provides a URL like: `pawnder-production.up.railway.app`

- Click "Settings" → "Domains" → "Generate Domain"
- Visit your site!

---

## 🎯 Post-Deployment Checklist

- [ ] App loads successfully
- [ ] Static files work (CSS displays)
- [ ] Can login to admin panel
- [ ] Can register new users
- [ ] Can add pets with photos
- [ ] Database persists data

---

## 💰 Railway Pricing

- **Free:** $5 credit per month (good for small projects)
- **Pay as you go:** ~$5-20/month for most Django apps
- **No credit card** required to start

---

## 🔧 Troubleshooting

**App won't start:**
- Check logs in Railway dashboard
- Verify all environment variables are set
- Make sure `requirements-prod.txt` has all dependencies

**Static files not loading:**
```bash
railway run python manage.py collectstatic --noinput
```

**Database errors:**
- Railway sets `DATABASE_URL` automatically
- Make sure migrations ran successfully

**Need to access shell:**
```bash
railway run python manage.py shell
```

---

## 🚀 Automatic Deployments

Once set up, every push to your `main` branch automatically deploys!

```bash
# Make changes locally
git add .
git commit -m "Update feature"
git push

# Railway automatically deploys!
```

---

## 📱 Custom Domain (Optional)

Railway supports custom domains:

1. Go to Settings → Domains
2. Click "Custom Domain"
3. Add your domain (e.g., pawnder.com)
4. Update your DNS with provided CNAME
5. SSL certificate auto-generated!

---

## 🆘 Need Help?

- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- Check deployment logs in Railway dashboard

---

That's it! Your pet dating app is now live! 🐾
