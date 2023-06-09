import csv
from flask import Flask, request, render_template
import psycopg2, random

from psycopg2.extras import RealDictCursor

conn = psycopg2.connect(
    #just uncomment the proper host
    "host=db dbname=postgres user=postgres password=postgres", #for docker users
    #"host=localhost dbname=final_project user=postgres password=postgres", #for Kirill
    cursor_factory=RealDictCursor)
app = Flask(__name__)


@app.route('/about')
def about():
    return render_template("about_us.html")

@app.route('/')
def welcome():
    return render_template("welcome.html")


#list of all names in the dataset. I know there is easier way using sql, but I had problems with RealDictRow
list_of_names = ["Move to Heaven", "Hospital Playlist", "Flower of Evil", "Hospital Playlist 2", "My Mister", "Prison Playbook",
 "Reply 1988", "It's Okay to Not Be Okay", "Mr. Queen", "Mother", "Signal", "Navillera", "Happiness", "Vincenzo",
 "Crash Landing on You", "SKY Castle", "Kingdom", "Mr. Sunshine", "Healer", "Stranger", "Goblin", "Hometown Cha-Cha-Cha", 
 "The Uncanny Counter", "D.P.", "Kingdom", "The Penthouse", "Weightlifting Fairy Kim Bok Joo", "The Devil Judge",
 "Life on Mars", "The Penthouse 2", "Beyond Evil", "Taxi Driver", "Six Flying Dragons", "The Guest", "Racket Boys", 
 "Youth of May", "Mouse", "Sweet Home", "18 Again", "Chicago Typewriter", "Defendant", "While You Were Sleeping", 
 "Dear My Friends", "Dr. Romantic 2", "Kill Me, Heal Me", "Arthdal Chronicles Part 2", "Misaeng", "Arthdal Chronicles Part 3", 
 "My Name", "Hotel del Luna", "Dr. Romantic", "The Fiery Priest", "Moon Lovers", "Descendants of the Sun", 
 "Hot Stove League", "Strong Woman Do Bong Soon", "Law School", "Live", "Tunnel", "Strangers from Hell", "It's Okay, That's Love", 
 "Eulachacha Waikiki", "The Bridal Mask", "Partners for Justice 2", "Jewel in the Palace", "My Father is Strange", 
 "Children of Nobody", "Go Back Couple", "Good Manager", "Stranger 2", "My Love from the Star", "Empress Ki", 
 "Age of Youth", "Mystic Pop-Up Bar", "Cruel City", "365", "Designated Survivor", "Just Between Lovers", "Squid Game", 
 "Avengers Social Club", "The Master's Sun", "Once Again", "Save Me", "Bad Guys", "Missing", "Rebel", "Nobody Knows", 
 "I Hear Your Voice", "Reply 1997", "Kairos", "Dali and the Cocky Prince", "Yumi's Cells", "Arthdal Chronicles Part 1", 
 "Beautiful World", "What's Wrong with Secretary Kim", "Vagabond", "Doctor John", "When the Camellia Blooms",
 "Because This Is My First Life", "Fight For My Way"]


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
            and ( %(casts)s is null or casts ilike %(casts)s )
            and ( %(genre)s is null or genre ilike %(genre)s )
        """

    params = {
        "name": f"%{name}%",
        "year": int(year) if year and year.isdigit() else 0 
        if year and not year.isdigit() else None,
        "casts": f"%{casts}%",
        "genre": f"%{genre}%",
        "rating": float(rating) if rating and rating.replace('.', '').isdigit() else 0
        if rating and not rating.isdigit() else None,
        "episode": int(episode) if episode and episode.isdigit() else 0
        if episode and not episode.isdigit() else None,
        "duration": int(duration) if duration and duration.isdigit() else 0
        if duration and not duration.isdigit() else None,
        "network": f"%{network}%",
        
        "sort_by": sort_by,
        "sort_dir" : sort_dir,
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


    def need_some_spiciness():
        index = random.randrange(0, 99)
        return list_of_names[index]
    
    
    return render_template("kdrama.html",
                           kdrama=results,
                           params=request.args,
                           get_sort_dir=get_sort_dir,
                           result_count =count,
                           spicy = need_some_spiciness()
                           )



@app.route("/synopsis")
def render_sets2():
    name = "%"+request.args.get("name", "")+"%"

    params = {
        "name": f"%{name}%"
    }

    syn_where_clause = """
        from kdrama
        where name ilike %(name)s
    """

# with conn.cursor() as cur:
#         cur.execute(f"""select name, synopsis
#                         {syn_where_clause} 
#                     """,
#                     params)
#         syn = list(cur.fetchall())

    with conn.cursor() as cur:
        cur.execute(f"""select synopsis
                        {syn_where_clause} 
                    """,
                    params)
        syn = list(cur.fetchall())

        thingy = []
        for k,v in syn[0].items():
            if k == 'synopsis':
                thingy.append(v)
        clean_syn = thingy[0]


    with conn.cursor() as cur:
        cur.execute(f"select count(*) as count {syn_where_clause}", params)
        count = cur.fetchone()["count"]
    

    return render_template("kdrama.html",
                           params=request.args,
                           result_count = count,
                           summary = clean_syn)

