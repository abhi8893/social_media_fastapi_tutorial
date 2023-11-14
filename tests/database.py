from app.config import settings
from sqlalchemy.engine import create_engine, URL as SQLAlchemyURL
from sqlalchemy.orm import sessionmaker


sqlalchemy_database_url_obj = SQLAlchemyURL.create(
  "postgresql",
  username=settings.database_username,
  password=settings.database_password,
  host=settings.database_hostname,
  database=f'{settings.database_name}_test',
  port=settings.database_port
)

if settings.db_ssl_require:
  extra_kwargs = dict(connect_args={'sslmode':'require'}, echo=True)
else:
  extra_kwargs = dict()

engine = create_engine(sqlalchemy_database_url_obj, **extra_kwargs)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

