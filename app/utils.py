from passlib.context import CryptContext

# Password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hash(x):
  return pwd_context.hash(x)  


def verify_password(orig, hashed):
  return pwd_context.verify(orig, hashed)