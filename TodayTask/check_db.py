import psycopg2

conn = psycopg2.connect(host='localhost', database='Essays', user='postgres', password='zavian')
cur = conn.cursor()
cur.execute('SELECT id, title FROM essays ORDER BY id')
rows = cur.fetchall()

if rows:
    for r in rows:
        print(f'ID: {r[0]}, Title: {r[1][:40]}')
else:
    print("No essays found in database")
    
conn.close()
