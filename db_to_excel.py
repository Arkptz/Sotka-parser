import sqlite3
import pandas as pd
from config import db_path, homeDir
cnx = sqlite3.connect(db_path)

df = pd.read_sql_query("SELECT * FROM Fabrics", cnx, index_col='id')
df['stol_styl_tabyret'] = df['stol_styl_tabyret'] ==1
df.to_excel(f'{homeDir}\\fabrics.xlsx')