from sqlmodel import SQLModel, create_engine

mysql_username = "root"
mysql_password = "12345"
mysql_host = "localhost"
mysql_port = 3306
mysql_database = "testdb"

mysql_url = f"mysql+mysqlconnector://{mysql_username}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_database}"

engine = create_engine(mysql_url, echo=True)


def create_db_and_table():
    SQLModel.metadata.create_all(engine)
