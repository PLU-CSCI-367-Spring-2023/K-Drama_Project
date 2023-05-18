import csv
from flask import Flask, request
from flask import Flask, request, render_template
import psycopg2
from psycopg2.extras import RealDictCursor

conn = psycopg2.connect(
    "host=db dbname=postgres user=postgres password=postgres",
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

    params = {
        "name": f"%{name}%",
        "year": int(year) if year else None,
        "casts": f"%{casts}%",
        "genre": f"%{genre}%",
        "rating": int(rating) if rating else None,
        "episode": int(episode) if episode else None,
        "duration": int(duration) if duration else None,
        "rating": int(rating) if rating else None,
        "network": f"%{network}%"
    }

   
    from_where_clause = f"""
        from kdrama
    """


    # with conn.cursor() as cur:
    #     #set_num
    #     cur.execute(f"select s.set_num as set_num {from_where_clause}", params)
    #     results_set_num = list(cur.fetchall())
        
    #     #listing all set_names and theme_names limit 100
    #     cur.execute(f"select s.name as set_name, t.name as theme_name, s.num_parts as part_count, s.set_num as set_num, s.year as year {from_where_clause}", params)
    #     sets = list(cur.fetchall())
  
       
    #     #count counter
    #     cur.execute(f"select count(*) as count {from_where_clause_count}", params)
    #     count = cur.fetchone()["count"]
    
    with conn.cursor() as cur:
        cur.execute(f"""select name, year, casts, genre, episode, duration, rating, network
                        {from_where_clause} 
                    """,
                    params)
        results = list(cur.fetchall())

    return render_template("kdrama.html", 
                           kdrama=results,
                           params=request.args)



