copy kdrama(name, year, episode, network, duration, content, synopsis, casts, genre, rating)
from '/docker-entrypoint-initdb.d/seed_data/top100_kdrama.csv'
delimiter ','
csv header;

  