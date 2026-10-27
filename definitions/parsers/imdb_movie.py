import json
import sys


def parse(input_data: dict) -> dict:
    """
    Parses raw IMDb movie input dictionary into standardized movie schema.
    """
    movie = input_data.get("movie", {})
    return {
        "id": movie.get("tconst") or movie.get("id"),
        "title": movie.get("primaryTitle") or movie.get("title"),
        "original_title": movie.get("originalTitle"),
        "year": int(movie.get("startYear", 0)) if movie.get("startYear") else None,
        "overview": movie.get("description", ""),
        "tmdb_poster_path": None,
        "tmdb_backdrop_path": None,
        "imdb_id": movie.get("tconst") or (str(movie.get("id")) if movie.get("id") is not None else None),
        "tmdb_id": None,
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            raw_input = json.load(f)
        result = parse(raw_input)
        print(json.dumps(result, ensure_ascii=False, indent=2))
