# Deploy Pawnder to Render (100% FREE!)

Deploy your pet dating app to Render for free - no credit card required!

## ✨ Why Render?

- ✅ **100% Free** - No credit card needed
- ✅ **PostgreSQL Database** - Free tier included
- ✅ **Automatic Deployments** - Deploy on git push
- ✅ **HTTPS by Default** - Free SSL certificate
- ✅ **Easy Setup** - One-click deployment

---

## 🚀 Quick Deploy (10 Minutes)

### Step 1: Push Your Code to GitHub

```bash
# Navigate to your project
cd /Users/anilajacob/Documents/pawnder

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Ready for deployment to Render"

# Create a new repository on GitHub:
# 1. Go to https://github.com/new
# 2. Name it "pawnder"
# 3. Don't initialize with README
# 4. Click "Create repository"

# Connect your local repo to GitHub (replace YOUR-USERNAME)
git remote add origin https://github.com/YOUR-USERNAME/pawnder.git
git branch -M main
git push -u origin main
```

### Step 2: Sign Up on Render

1. Go to https://render.com
2. Click "Get Started for Free"
3. Sign up with your GitHub account (easiest)
4. Authorize Render to access your repositories

### Step 3: Deploy with Blueprint (Easiest Method)

1. **Dashboard:** Click "New" → "Blueprint"

2. **Connect Repository:**
   - Select your `pawnder` repository
   - Render will detect `render.yaml`
   - Click "Connect"

3. **Blueprint Setup:**
   - Service Name: `pawnder` (auto-filled)
   - Database Name: `pawnder_db` (auto-filled)
   - Click "Apply"

4. **Wait for Deployment:**
   - Render will:
     - Create PostgreSQL database (free)
     - Install dependencies
     - Run migrations
     - Collect static files
     - Start your app
   - This takes 3-5 minutes

5. **Done!** 🎉
   - Your app is live!
   - URL: `https://pawnder.onrender.com` (or similar)

### Step 4: Create Admin Account

After deployment, go to your Render dashboard:

1. Click on your `pawnder` service
2. Click "Shell" in the top right
3. Run these commands:

```bash
python manage.py createsuperuser
# Enter username, email, password

# Load sample data (optional)
python manage.py populate_sample_data
python manage.py ensure_all_photos
```

### Step 5: Access Your Live Site! 🎉

Your app is now live at: `https://pawnder.onrender.com`

- **Homepage:** Your live URL
- **Admin:** Your live URL + `/admin/`
- **Login:** Your live URL + `/login/`

---

## 📋 Alternative: Manual Deployment (If Blueprint Doesn't Work)

### Method 1: Web Service

1. **Dashboard:** Click "New" → "Web Service"

2. **Connect Repository:**
   - Connect your GitHub `pawnder` repository
   - Click "Connect"

3. **Configure:**
   ```
   Name: pawnder
   Region: Choose closest to you
   Branch: main
   Runtime: Python 3
   Build Command: ./build.sh
   Start Command: gunicorn pawnder_project.wsgi:application
   Plan: Free
   ```

4. **Environment Variables:**
   Click "Advanced" → Add:
   ```
   DJANGO_SETTINGS_MODULE = pawnder_project.production_settings
   DEBUG = False
   PYTHON_VERSION = 3.11.0
   SECRET_KEY = (click "Generate" to create a random key)
   ```

5. **Create Service** - Click "Create Web Service"

### Method 2: Add Database

1. **Dashboard:** Click "New" → "PostgreSQL"

2. **Configure:**
   ```
   Name: pawnder-db
   Database: pawnder
   User: pawnder_user
   Region: Same as your web service
   Plan: Free
   ```

3. **Create Database**

4. **Connect to Web Service:**
   - Go to your web service
   - Click "Environment"
   - Add variable:
     ```
     DATABASE_URL = (Copy "Internal Database URL" from database dashboard)
     ```

5. **Redeploy:** Click "Manual Deploy" → "Deploy latest commit"

---

## 🔧 Troubleshooting

### Build Failed

**Check logs in Render dashboard:**
- Click on your service
- Click "Logs"
- Look for error messages

**Common fixes:**
```bash
# If build.sh permission error
git update-index --chmod=+x build.sh
git commit -m "Make build.sh executable"
git push
```

### Static Files Not Loading

Render automatically serves static files via WhiteNoise. If issues:
1. Check logs for collectstatic errors
2. Verify `STATIC_ROOT` in production_settings.py
3. Redeploy

### Database Connection Error

1. Verify DATABASE_URL is set in environment variables
2. Check database is in same region as web service
3. Make sure migrations ran (check logs)

### App Shows "Application Error"

1. Check logs for Python errors
2. Verify all environment variables are set
3. Try manual deploy
4. Check SECRET_KEY is set

---

## 🎯 Post-Deployment Checklist

After your app is live:

- [ ] App loads successfully
- [ ] Admin panel works (`/admin/`)
- [ ] Can register new users
- [ ] Can add pets
- [ ] Database persists data
- [ ] Static files load (CSS shows)
- [ ] Can upload photos

---

## 💰 Render Free Tier Limits

**What You Get Free:**
- Web Service: 750 hours/month (enough for 1 app running 24/7)
- PostgreSQL: 1GB storage, 97 connections
- Bandwidth: 100GB/month
- Build Minutes: 500 minutes/month

**Limitations:**
- ⏱️ App spins down after 15 minutes of inactivity
- 🐌 First request after spin-down takes 30-60 seconds
- 📦 Database limited to 1GB
- 🔄 No automatic daily backups

**Upgrading:** You can upgrade anytime for $7-25/month to remove these limits

---

## 🔄 Automatic Deployments

Once set up, every push to main branch auto-deploys!

```bash
# Make changes locally
git add .
git commit -m "Update feature"
git push

# Render automatically:
# 1. Detects push
# 2. Builds your app
# 3. Runs migrations
# 4. Deploys new version
# ✅ Done in 2-3 minutes!
```

---

## 🌐 Custom Domain (Optional)

Add your own domain (e.g., pawnder.com):

1. **Render Dashboard:**
   - Go to your service
   - Click "Settings" → "Custom Domains"
   - Click "Add Custom Domain"
   - Enter your domain

2. **DNS Settings:**
   - Add CNAME record to your domain's DNS:
     ```
     CNAME: www → pawnder.onrender.com
     ```

3. **SSL Certificate:**
   - Render automatically generates SSL
   - Usually takes 5-10 minutes

---

## 📊 Monitoring Your App

**View Logs:**
- Render Dashboard → Your Service → "Logs"
- See real-time application logs
- Debug errors

**Metrics:**
- Dashboard shows CPU, memory usage
- Request counts
- Response times

**Shell Access:**
- Click "Shell" in dashboard
- Run Django management commands
- Access Python shell

---

## 🔐 Security Notes

Your app is secure by default:
- ✅ HTTPS enabled automatically
- ✅ SECRET_KEY is auto-generated
- ✅ DEBUG is False
- ✅ CSRF protection enabled
- ✅ Secure cookies configured

---

## 🆘 Need Help?

**Render Documentation:**
- https://render.com/docs/deploy-django

**Common Commands in Shell:**
```bash
# Create superuser
python manage.py createsuperuser

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Load sample data
python manage.py populate_sample_data

# Django shell
python manage.py shell
```

**Check Status:**
- Green = Deployed and running
- Yellow = Building/Deploying
- Red = Failed (check logs)

---

## 🎉 Success!

Your Pawnder app is now:
- ✅ Live on the internet
- ✅ Accessible from anywhere
- ✅ Running on free hosting
- ✅ Using PostgreSQL database
- ✅ Secured with HTTPS
- ✅ Auto-deploying on updates

**Share your live URL with friends and start matching pets!** 🐾

---

## 📱 What's Next?

1. **Add Real Data:** Register and add your actual pets
2. **Customize:** Update branding, colors, text
3. **Share:** Send URL to other pet owners
4. **Monitor:** Check logs and metrics regularly
5. **Upgrade:** Consider paid plan if you get traffic

Your pet dating platform is now live! 🚀
