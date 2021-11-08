#!/bin/python3


import psycopg2
import jinja2
# Establish a connection to the database by creating a cursor object
# The PostgreSQL server must be accessed through the PostgreSQL APP or Terminal Shell

# conn = psycopg2.connect("dbname=suppliers port=5432 user=postgres password=postgres")

# Or:
conn = psycopg2.connect(host="db.shishko.info", port = 5432, database="literature", user="websrv", password="websrv")

# Create a cursor object
cur = conn.cursor()

# A sample query of all data from the "vendors" table in the "suppliers" database
cur.execute("""SELECT * FROM magazines""")
query_results = cur.fetchall()
print(query_results)

# Close the cursor and connection to so the server can allocate
# bandwidth to other requests
cur.close()
conn.close()

title = 'Hi this is my title'
outputfile = '/home/linux/myproject/templates/index.html'
subs = jinja2.Environment(
              loader=jinja2.FileSystemLoader('./templates/')
              ).get_template('index.html').render(title=title,results=query_results)
# lets write the substitution to a file
with open(outputfile,'w') as f: f.write(subs)
