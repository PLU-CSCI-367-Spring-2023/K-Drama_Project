import csv
from flask import Flask, request, render_template
import psycopg2

from psycopg2.extras import RealDictCursor

conn = psycopg2.connect(
    #just uncomment the proper host
    "host=db dbname=postgres user=postgres password=postgres", #//for docker users
    #"host=localhost dbname=final_project user=postgres password=postgres", #for Kirill
    cursor_factory=RealDictCursor)
app = Flask(__name__)


@app.route('/')
def hello_world():
    return "Hello, World!"

@app.route("/home")
def render_sets():
    name = request.args.get("name", "")
    year = request.args.get('year')
    casts = request.args.get("casts", "")
    genre = request.args.get("genre", "")
    episode = request.args.get('episode')
    duration = request.args.get('duration')
    rating = request.args.get('content')
    network = request.args.get("network", "")
    sort_by = request.args.get("sort_by", "name")
    sort_dir = request.args.get("sort_dir", "asc")
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 100, type=int)

    #optional query params
    from_where_clause = f"""
            from kdrama 
            where %(name)s is null or name ilike %(name)s
            and ( %(year)s is null or year = %(year)s )
            and ( %(episode)s is null or episode = %(episode)s )
            and ( %(duration)s is null or duration = %(duration)s )
            and ( %(rating)s is null or rating = %(rating)s )
            and ( %(network)s is null or network ilike %(network)s )
        """

    params = {
        "name": f"%{name}%",
        "year": int(year) if year else None,
        "casts": f"%{casts}%",
        "genre": f"%{genre}%",
        "rating": float(rating) if rating else None,
        "episode": int(episode) if episode else None,
        "duration": int(duration) if duration else None,
        "content": float(rating) if rating else None,
        "network": f"%{network}%",
        "sort_by": sort_by,
        "sort_dir" : sort_dir,
        "page" : page,
        "limit" : limit
    }

 
        
    #     #listing all set_names and theme_names limit 100
    #     cur.execute(f"select s.name as set_name, t.name as theme_name, s.num_parts as part_count, s.set_num as set_num, s.year as year {from_where_clause}", params)
    #     sets = list(cur.fetchall())

        
    def get_sort_dir(col):
        if col== sort_by:
            return "desc" if sort_dir == "asc" else "asc"
        else:
            return "asc"

 
    #count counter  
    with conn.cursor() as cur:
        cur.execute(f"""select name, year, casts, genre, episode, duration, rating, network
                        {from_where_clause} 
                        order by {sort_by} {sort_dir} 
                        limit %(limit)s 
                    """,
                    params)
        results = list(cur.fetchall())

        cur.execute(f"select count(*) as count {from_where_clause}", params)
        count = cur.fetchone()["count"]
         
    return render_template("kdrama.html",
                           kdrama=results,
                           params=request.args,
                           get_sort_dir=get_sort_dir,
                           result_count =count
                           )
@app.route("/synopsis")
def render_sets2():
    name = request.args.get("name", "")

    params = {
        "name": f"%{name}%"
    }

    syn_where_clause = """
        from kdrama
        where name ilike %(name)s
    """

    with conn.cursor() as cur:
        cur.execute(f"""select synopsis
                        {syn_where_clause} 
                    """,
                    params)
        syn = list(cur.fetchall())

    with conn.cursor() as cur:
        cur.execute(f"select count(*) as count {syn_where_clause}", params)
        count = cur.fetchone()["count"]
    

    return render_template("kdrama.html",
                           params=request.args,
                           result_count = count,
                           summary = syn)

