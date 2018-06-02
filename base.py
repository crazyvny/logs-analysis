import psycopg2
from datetime import date

connection = psycopg2.connect("dbname=news")
cursor = connection.cursor()
# Declaring a dummy tuple as tuple to string concation not possible.
a3 = ('dummy','tuple','views', '-')
def views():
    print("What are the most viewed artcles?\n")
    cursor.execute("""SELECT title, log.path, COUNT(log.path) AS hits, authors.name
        FROM articles
        JOIN authors
        ON articles.author = authors.id
        JOIN log
        ON log.path = CONCAT('/article/', articles.slug)
        GROUP BY title, path, authors.name
        ORDER BY hits DESC LIMIT 3""")
    a2 = cursor.fetchall()
    for a2 in a2:
       print a2[0], a3[3], a2[2], a3[2]
    print("\n")
views()

def articles():
    print("What are the most popular articles of all time?\n")
    cursor.execute("""SELECT title, path, COUNT(path) AS hits, authors.name
        FROM articles
        JOIN authors
        ON articles.author = authors.id
        JOIN log
        ON log.path = concat('/article/', articles.slug)
        WHERE log.status LIKE '200 OK'
        GROUP BY authors.name, articles.title, log.path
        ORDER BY hits DESC LIMIT 3;""")
    b2 = cursor.fetchall()
    for b2 in b2:
        print b2[3], a3[3], b2[2], a3[2]
    print("\n")
articles()

def errors():
    print("On which days more than 1% of the requests led to error?\n")
    cursor.execute("""select * from (
           select a.day,
           round(cast((100*b.hits) as numeric) / cast(a.hits as numeric), 2)
           as errp from
           (select date(time) as day, count(*) as hits
           from log group by day) as a
           inner join
           (select date(time) as day, count(*) as hits from log where status
           like '%404%' group by day) as b
           on a.day = b.day)
           as t where errp > 1.0""")
    c3 = cursor.fetchall()
    # Declaring a dummy tuple as tuple to string concation not possible.
    a4 = ('dummy', '--', 'tuple', '%', 'errors')
    for i,j in c3:
        print "{:%B %d, %Y}".format(i),a4[1],j,a4[3],a4[4]
errors()