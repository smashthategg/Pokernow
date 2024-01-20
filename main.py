import os
from sqlbuilder import build_sql_database_framework
from reader import csv_to_df

print(csv_to_df())

if not os.path.exists("./pokernow_sqlite.db"):
    build_sql_database_framework()
