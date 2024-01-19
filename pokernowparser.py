from sqlbuilder import build_sql_database_framework
from reader import csv_to_df
import os

player = "smashthategg"

print(csv_to_df(player))

if not os.path.exists("./pokernow_sqlite.db"):
    build_sql_database_framework()
