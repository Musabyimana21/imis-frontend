# 🗄️ IMIS Database Deployment Checklist

## ✅ Step-by-Step Guide

### 1️⃣ In cPanel - Create Database

- [ ] Go to **PostgreSQL Databases**
- [ ] Create database: `imis_production`
- [ ] Note full name: `cpanel_username_imis_production`

### 2️⃣ In cPanel - Create User

- [ ] Create user: `imis_user`
- [ ] Generate strong password
- [ ] Note full username: `cpanel_username_imis_user`
- [ ] Save password securely

### 3️⃣ In cPanel - Grant Permissions

- [ ] Add user to database
- [ ] Grant **ALL PRIVILEGES**

### 4️⃣ In cPanel - Remote Access

Current Access Hosts:
- 31.170.162.81
- 130.0.15

- [ ] Add your server IP OR `%` (all IPs)
- [ ] Comment: "IMIS Backend Server"

### 5️⃣ On Your Computer - Configure

Run the setup script:
```bash
SETUP_CPANEL_DATABASE.bat
```

OR manually:
```bash
python setup_cpanel_db.py
```

This will:
- [ ] Generate secure SECRET_KEY
- [ ] Create DATABASE_URL
- [ ] Save to `.env.cpanel` file
- [ ] Test connection (optional)

### 6️⃣ Deploy Configuration

- [ ] Copy `backend/.env.cpanel` to `backend/.env` on server
- [ ] Update `FRONTEND_URL` with your domain
- [ ] Update `ALLOWED_ORIGINS` with your domain

### 7️⃣ Initialize Database

On your server:
```bash
cd backend
python init_db.py
```

- [ ] Tables created successfully

### 8️⃣ Verify Setup

```bash
cd backend
python test_db.py
```

- [ ] Connection successful
- [ ] Tables exist

### 9️⃣ Seed Data (Optional)

```bash
cd backend
python seed_data.py
```

- [ ] Sample data added

## 📋 Information You Need

### From cPanel:
- Database Host: `_________________`
- Database Port: `5432` (default)
- Database Name: `_________________`
- Database User: `_________________`
- Database Password: `_________________`

### Your Domain:
- Frontend URL: `https://_________________`
- Backend API URL: `https://_________________/api`

## 🔧 Troubleshooting

### ❌ Connection Refused
1. Check Remote Database Access has your IP
2. Verify port 5432 is open
3. Test with: `telnet your-host.com 5432`

### ❌ Authentication Failed
1. Double-check username/password
2. Verify user has privileges
3. Check for cPanel username prefix

### ❌ SSL Error
Already configured in `database.py`:
```python
connect_args = {"sslmode": "disable"}
```

## 📞 Need Help?

1. Check `CPANEL_DATABASE_SETUP.md` for detailed guide
2. Run `python setup_cpanel_db.py` for interactive setup
3. Test connection with option 2 in setup script

## ✅ Ready for Next Step?

Once database is configured:
- ✅ Database setup complete
- ⏭️ Next: Deploy backend application
- ⏭️ Then: Deploy frontend application
- ⏭️ Finally: Test complete system

---

**Current Status:** 🗄️ Database Configuration Phase
**Next Phase:** 🚀 Backend Deployment
