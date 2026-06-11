from app.core.database import SessionLocal
from app.core.security import hash_password
from app.core.config import settings
from app.models.users import User
import logging

logger = logging.getLogger(__name__)

def create_admin():
    db = SessionLocal()

    existing = db.query(User).filter(User.email == settings.SUPERADMIN_EMAIL).first()
    if existing:
        logger.info("Admin already exists!")
        return

    admin = User(
        username=settings.SUPERADMIN_USERNAME,
        email=settings.SUPERADMIN_EMAIL,
        hashed_password=hash_password(settings.SUPERADMIN_PASSWORD),
        is_admin=True
    )
    db.add(admin)
    db.commit()
    logger.info("Admin created successfully!")
    db.close()


if __name__ == "__main__":
    create_admin()

