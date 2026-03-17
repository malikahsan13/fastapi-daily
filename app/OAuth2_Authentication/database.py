from sqlmodel import SQLModel, create_engine

mysql_username = "root"
mysql_password = "123456"
mysql_host = "localhost"
mysql_port = "3306"
mysql_database = "oauth_test"

mysql_url = f"mysql+mysqlconnector://{mysql_username}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_database}"

engine = create_engine(mysql_url)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)