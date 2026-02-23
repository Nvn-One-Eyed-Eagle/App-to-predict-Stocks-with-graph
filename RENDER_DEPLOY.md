# Render Deployment Guide

## Automatic Setup
This repo is configured for Render with:
- `runtime.txt` - Python 3.10.13 version
- `Procfile` - Gunicorn start command  
- `build.sh` - Build script for migrations & collectstatic

## Render Dashboard Setup

1. **Create a new Web Service** and connect your GitHub repo
2. **Set these Environment Variables:**
   - `SECRET_KEY` = (generate at https://djecrety.ir/)
   - `DEBUG` = `False`
   - `ALLOWED_HOSTS` = yourdomain.onrender.com

3. **Set the Build Command:**
   ```
   bash build.sh
   ```

4. **Deploy!**

That's it—Render will:
- Use Python 3.10.13 from `runtime.txt`
- Run `build.sh` during build (migrations + static collection)
- Start the app with `Procfile` command

## Troubleshooting
- If Python version is still wrong, double-check `runtime.txt` exists in repo root
- If collectstatic fails, ensure `STATIC_ROOT` is set in settings.py
- Check Render logs for detailed errors
