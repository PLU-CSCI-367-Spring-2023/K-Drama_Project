copy kdrama(name, year, aired_date, aired_on, episode, network, duration, content_rating, synopsis, casts, genre, tags, rank, rating)
from '/docker-entrypoint-initdb.d/seed_data/top100_kdrama.csv'
delimiter ','
csv header;

  