from langchain_community.utilities import SQLDatabase

db = SQLDatabase.from_uri("sqlite:///novatech.db")


def get_database():
    return db


if __name__ == "__main__":
    print("Tables:")
    print(db.get_usable_table_names())

    print("\nDatabase Schema:")
    print(db.get_table_info())