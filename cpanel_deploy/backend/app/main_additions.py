@app.get("/api-info")
def api_info():
    """Get comprehensive API information"""
    return {
        "api_name": "IMIS - Ishakiro Information Management System",
        "version": "3.0.0",
        "description": "Complete Lost & Found Platform for Rwanda",
        "features": {
            "core": [
                "User Authentication with JWT",
                "Report Lost/Found Items",
                "AI-Powered Matching (70% text + 30% location)",
                "Secure In-App Messaging",
                "Geolocation with Auto-Detect",
                "Commission Tracking (10% default)",
                "Admin Dashboard with Analytics",
                "English & Kinyarwanda Support",
                "WCAG 2.1 Accessibility Compliant",
                "Fully Responsive Design"
            ],
            "technical": [
                "RESTful API with OpenAPI docs",
                "Database migrations support",
                "Role-based access control",
                "Password hashing with bcrypt",
                "CORS configuration",
                "Health check endpoints",
                "Error handling & validation",
                "Pagination support",
                "Audit logging",
                "Payment processing"
            ],
            "payment": [
                "MTN Mobile Money integration",
                "Airtel Money integration",
                "Bank transfer support",
                "1,000 RWF unlock fee",
                "10% commission system",
                "Payment verification",
                "Refund processing"
            ]
        },
        "endpoints": {
            "authentication": {
                "POST /auth/register": "Register new user",
                "POST /auth/login": "User login"
            },
            "items": {
                "GET /items": "List items with advanced filtering",
                "POST /items": "Create new item",
                "GET /items/{id}": "Get item details",
                "PUT /items/{id}": "Update item",
                "DELETE /items/{id}": "Delete item",
                "GET /items/{id}/matches": "Get AI matches",
                "POST /items/{id}/rematch": "Force rematch"
            },
            "messages": {
                "GET /messages/conversations": "Get conversations",
                "POST /messages": "Send message",
                "GET /messages/conversation/{item_id}/{user_id}": "Get conversation messages",
                "PUT /messages/{id}/read": "Mark message as read"
            },
            "payments": {
                "POST /payments/initiate": "Initiate payment",
                "GET /payments/verify/{id}": "Verify payment",
                "GET /payments/contact/{item_id}": "Get contact info after payment",
                "GET /payments/my-payments": "Get payment history"
            },
            "admin": {
                "GET /admin/stats": "System statistics",
                "GET /admin/users": "Manage users",
                "GET /admin/payments": "Payment oversight",
                "GET /admin/commissions": "Commission tracking"
            }
        },
        "tech_stack": {
            "backend": "FastAPI (Python)",
            "database": "PostgreSQL",
            "ai_ml": "scikit-learn (TF-IDF, Cosine Similarity)",
            "authentication": "JWT tokens",
            "payments": "Mobile Money APIs"
        },
        "deployment": {
            "backend": "Render (recommended)",
            "database": "Render PostgreSQL",
            "cost": "$0/month development, $14-34/month production"
        }
    }

@app.get("/test-credentials")
def test_credentials():
    """Get test credentials for development"""
    return {
        "admin": {
            "email": "admin@imis.rw",
            "password": "admin123",
            "role": "Full system access"
        },
        "loser": {
            "email": "loser@imis.rw",
            "password": "lost123",
            "name": "Jean Mugabo",
            "item": "Lost Black iPhone 13"
        },
        "finder": {
            "email": "finder@imis.rw",
            "password": "found123",
            "name": "Marie Uwase",
            "item": "Found Black iPhone"
        },
        "user": {
            "email": "user1@imis.rw",
            "password": "password123",
            "name": "User One"
        },
        "instructions": {
            "1": "Use these credentials to test the system",
            "2": "Login as 'loser' to report lost items",
            "3": "Login as 'finder' to report found items",
            "4": "See AI matching in action",
            "5": "Test payment system with 1,000 RWF",
            "6": "Use admin account for dashboard access"
        }
    }