import json
import sys


def parse(input_data: dict) -> dict:
    """
    Parses raw IMDb TV show input dictionary (from TMDB find) into standardized schema format.
    """
    find_data = input_data.get("find", {})
    tv_results = find_data.get("tv_results", [])
    tv = tv_results[0] if tv_results else input_data.get("tv", {})

    raw_id = tv.get("id") if tv.get("id") is not None else tv.get("tconst")
    title = tv.get("name") or tv.get("title") or tv.get("primaryTitle")
    original_title = tv.get("original_name") or tv.get("original_title") or tv.get("originalTitle")
    
    first_air_date = tv.get("first_air_date") or tv.get("release_date")
    year = int(first_air_date.split("-")[0]) if first_air_date else (int(tv.get("startYear", 0)) if tv.get("startYear") else None)
    
    overview = tv.get("overview", "") or tv.get("description", "")
    poster_path = tv.get("poster_path")
    backdrop_path = tv.get("backdrop_path")
    
    fallback_imdb_id = input_data.get("imdb_id")
    imdb_id = tv.get("imdb_id") or fallback_imdb_id or tv.get("tconst") or (str(raw_id) if raw_id is not None else None)
    tmdb_id = int(tv.get("id")) if tv.get("id") is not None else None

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
