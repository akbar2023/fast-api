from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'postgresql://akbar_render:yHsSMaPMloDONSY7QSXrKyerN63W2M6G@dpg-ci8rn3p8g3n3vm6clsv0-a.frankfurt-postgres.render.com/mobiles'



# equivalent à un "connect"
database_engine = create_engine(DATABASE_URL)
# equivalent à un "cursor"
SessionTemplate = sessionmaker(
    bind=database_engine, autocommit=False, autoflush=False)

# get_cursor is used by almost all endpoint in order to connect to the database
def get_cursor():
    db = SessionTemplate()
    try:
        yield db # yield est une operation python qui permet de récupérer quelques chose qui peut ne pas exister 
    finally:
        db.close()
