create table if not exists kdrama (
    name varchar not null,
    year int not null,
    cast varchar not null,
    genre varchar not null,
    genre_rating int not null,
    episode int not null,
    duration int not null,
    content_rating varchar not null,
    network varchar not null
)