# cPanel Database Setup for IMIS

## 1. Create PostgreSQL Database in cPanel

### Step 1: Create Database
1. Go to cPanel → **PostgreSQL Databases**
2. Create a new database:
   - Database Name: `imis_production` (or your preferred name)
   - Click "Create Database"
3. Note the full database name (usually: `cpanel_username_imis_production`)

### Step 2: Create Database User
1. In the same PostgreSQL Databases section
2. Create a new user:
   - Username: `imis_user`
   - Password: Generate a strong password (save it securely!)
   - Click "Create User"
3. Note the full username (usually: `cpanel_username_imis_user`)

### Step 3: Add User to Database
1. In "Add User to Database" section:
   - Select User: `imis_user`
   - Select Database: `imis_production`
   - Click "Add"
2. Grant ALL PRIVILEGES to the user

### Step 4: Configure Remote Access
1. Go to cPanel → **Remote Database Access**
2. Add your server IP or `%` for testing:
   - Host: `%` (all IPs) or your specific server IP
   - Comment: "IMIS Backend Server"
   - Click "Add Host"

## 2. Get Database Connection Details

You'll need these details for your `.env` file:

```
Host: Your cPanel domain or server IP (e.g., server123.hostingprovider.com)
Port: 5432 (default PostgreSQL port)
Database: cpanel_username_imis_production
Username: cpanel_username_imis_user
Password: [the password you created]
```

## 3. Create Production .env File

Create `backend/.env` with this format:

```env
# Database Connection
DATABASE_URL=postgresql://USERNAME:PASSWORD@HOST:5432/DATABASE_NAME

# Example:
# DATABASE_URL=postgresql://cpanel_user_imis:SecurePass123@server.host.com:5432/cpanel_user_imis_production

# Security
SECRET_KEY=GENERATE_RANDOM_SECRET_KEY_HERE
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# MTN Mobile Money
MTN_MOMO_ENABLED=true
MTN_MOMO_ENVIRONMENT=production
MTN_MOMO_BASE_URL=https://proxy.momoapi.mtn.co.rw
MTN_MOMO_SUBSCRIPTION_KEY=92e0ee9794d34ac8bb166d2cd3b99a69
MTN_MOMO_API_USER=24a14d7b-57b2-46a6-ba5c-4c17f628eb9e
MTN_MOMO_API_KEY=2ac93c3f60304fdaa6f9ad2f591f0834
MTN_MOMO_TARGET_ENVIRONMENT=mtnrwanda
MTN_MOMO_ACCOUNT=FRI:41414644/MM

# Payment Settings
UNLOCK_FEE=1000.0
COMMISSION_RATE=0.10
PAYMENT_TIMEOUT_SECONDS=300

# Frontend URL (your domain)
FRONTEND_URL=https://yourdomain.com

# CORS
ALLOWED_ORIGINS=https://yourdomain.com
```

## 4. Initialize Database Tables

After configuring the database, run this command to create tables:

```bash
cd backend
python init_db.py
```

## 5. Verify Database Connection

Test the connection:

```bash
cd backend
python test_db.py
```

## 6. Seed Initial Data (Optional)

Add sample data for testing:

```bash
cd backend
python seed_data.py
```

## Troubleshooting

### Connection Refused
- Check if PostgreSQL port (5432) is open in firewall
- Verify Remote Database Access has your IP added
- Confirm database credentials are correct

### SSL Connection Error
- The database.py file already has `sslmode: disable` configured
- If issues persist, try: `DATABASE_URL=postgresql://user:pass@host:5432/db?sslmode=disable`

### Authentication Failed
- Double-check username and password
- Ensure user has ALL PRIVILEGES on the database
- Verify the full username includes cPanel prefix

## Next Steps

After database setup:
1. ✅ Database configured
2. 📦 Deploy backend application
3. 🌐 Deploy frontend application
4. 🔗 Connect frontend to backend API
5. 🧪 Test the complete system
