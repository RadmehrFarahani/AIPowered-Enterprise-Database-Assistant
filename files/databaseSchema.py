from langchain_community.utilities import SQLDatabase


db = SQLDatabase.from_uri(
    "sqlite:///novatech.db"
)


print(
    db.get_usable_table_names()
)