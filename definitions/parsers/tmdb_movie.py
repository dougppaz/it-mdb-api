import json
import sys


def parse(input_data: dict) -> dict:
    """
    Parses raw TMDB movie input dictionary into standardized movie schema.
    """
    movie = input_data.get("movie", {})
    return {
        "id": str(movie.get("id")) if movie.get("id") is not None else None,
        "title": movie.get("title") or movie.get("name"),
        "original_title": movie.get("original_title"),
        "year": int(movie.get("release_date", "0").split("-")[0]) if movie.get("release_date") else None,
        "overview": movie.get("overview", ""),
        "tmdb_poster_path": movie.get("poster_path"),
        "tmdb_backdrop_path": movie.get("backdrop_path")
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            raw_input = json.load(f)
        result = parse(raw_input)
        print(json.dumps(result, ensure_ascii=False, indent=2))
