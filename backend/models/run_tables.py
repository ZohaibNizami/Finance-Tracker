from backend.database import engine, Base
from backend.models import user, transaction  
from backend.models import topups, withdrawal
from backend.models.PasswordResetToken import PasswordResetToken

Base.metadata.create_all(bind=engine)
print("Tables created successfully")


