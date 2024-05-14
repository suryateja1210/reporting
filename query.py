import mysql.connector
import streamlit as st

conn=mysql.connector.connect(
    host= '50.28.107.39',
    port='3306',
    user='narvee',
    passwd='Atc404$',
    db='narvee_ATS'
)

c=conn.cursor()

def view_all_data():
    c.execute('''select vendor,posted_on,job_title,job_location,category_skill,Employment_type from tbl_rec_requirement 
              order by posted_on desc ''')
    data=c.fetchall()
    return data