from app.core.database import SessionLocal
from app.models.enhanced_models import User, UserRole
from app.core.security import get_password_hash

db = SessionLocal()

try:
    # Admin
    admin = User(
        email='admin@imis.rw',
        hashed_password=get_password_hash('admin123'),
        full_name='Admin User',
        phone='+250788000000',
        role=UserRole.ADMIN
    )
    db.add(admin)
    
    # Loser
    loser = User(
        email='loser@imis.rw',
        hashed_password=get_password_hash('lost123'),
        full_name='Jean Mugabo',
        phone='+250788111111',
        role=UserRole.USER
    )
    db.add(loser)
    
    # Finder
    finder = User(
        email='finder@imis.rw',
        hashed_password=get_password_hash('found123'),
        full_name='Marie Uwase',
        phone='+250788222222',
        role=UserRole.USER
    )
    db.add(finder)
    
    db.commit()
    print('✅ Test accounts created successfully!')
    print('\nLogin credentials:')
    print('Admin:  admin@imis.rw / admin123')
    print('Loser:  loser@imis.rw / lost123')
    print('Finder: finder@imis.rw / found123')
    
except Exception as e:
    print(f'Error: {e}')
    db.rollback()
finally:
    db.close()
