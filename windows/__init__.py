from . import months, years, songs, artists, albums

WINDOWS = {
    "Songs": songs.init,
    "Artists": artists.init,
    "Albums": albums.init,
    "Months": months.init,
    "Years": years.init,
}
