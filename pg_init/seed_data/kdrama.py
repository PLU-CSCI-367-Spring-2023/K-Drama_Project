from psycopg2.extensions import cursor
from utils import parse_int

def populate_kdrama(cur: cursor, rows: list[dict[str, str]]):
    
    for row in rows:
        kdrama = (row['name'], parse_int(row['year']), parse_int(row['episode']), row['network'], row['content_rating'], row['cast'], parse_int(row['genre_rating']))
        cur.execute("""
            insert into kdrama(name, year, episode, network, content_rating, cast, genre_rating) 
            values(%s, %s, %s, %s, %s, %s, %s)
            on conflict do nothing
            """, kdrama)