copy kdrama(name, aired_date, week, year, episode, network, duration, content, synopsis, casts, genre, tags, rank, rating)
from '/docker-entrypoint-initdb.d/seed_data/top100_kdrama.csv'
delimiter ','
csv header;

  