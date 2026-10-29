import json
import sys


def parse(input_data: dict) -> dict:
    """
    Parses raw IMDb movie input dictionary into standardized movie schema.
    """
    find_data = input_data.get("find", {})
    movie_results = find_data.get("movie_results", [])
    movie = movie_results[0] if movie_results else input_data.get("movie", {})

    raw_id = movie.get("id") if movie.get("id") is not None else movie.get("tconst")
    title = movie.get("title") or movie.get("name") or movie.get("primaryTitle")
    original_title = movie.get("original_title") or movie.get("originalTitle")
    
    release_date = movie.get("release_date")
    year = int(release_date.split("-")[0]) if release_date else (int(movie.get("startYear", 0)) if movie.get("startYear") else None)
    
    overview = movie.get("overview", "") or movie.get("description", "")
    poster_path = movie.get("poster_path")
    backdrop_path = movie.get("backdrop_path")
    
    imdb_id = movie.get("imdb_id") or movie.get("tconst") or (str(raw_id) if raw_id is not None else None)
    tmdb_id = int(movie.get("id")) if movie.get("id") is not None else None

    return {
        "id": str(raw_id) if raw_id is not None else None,
        "title": title,
        "original_title": original_title,
        "year": year,
        "overview": overview,
        "tmdb_poster_path": poster_path,
        "tmdb_backdrop_path": backdrop_path,
        "imdb_id": str(imdb_id) if imdb_id is not None else None,
        "tmdb_id": tmdb_id,
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            raw_input = json.load(f)
        result = parse(raw_input)
        print(json.dumps(result, ensure_ascii=False, indent=2))
