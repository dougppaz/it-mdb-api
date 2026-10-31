import json
import sys


def parse(input_data: dict) -> dict:
    """
    Parses raw TMDB TV show input dictionary into standardized schema format.
    """
    tv = input_data.get("tv", {})
    external_ids = input_data.get("external_ids", {})
    imdb_id = external_ids.get("imdb_id") or tv.get("imdb_id")
    raw_tmdb_id = tv.get("id") if tv.get("id") is not None else external_ids.get("id")

    first_air_date = tv.get("first_air_date")
    year = int(first_air_date.split("-")[0]) if first_air_date else None

    return {
        "id": str(tv.get("id")) if tv.get("id") is not None else None,
        "title": tv.get("name") or tv.get("title"),
        "original_title": tv.get("original_name") or tv.get("original_title"),
        "year": year,
        "overview": tv.get("overview", ""),
        "tmdb_poster_path": tv.get("poster_path"),
        "tmdb_backdrop_path": tv.get("backdrop_path"),
        "imdb_id": str(imdb_id) if imdb_id is not None else None,
        "tmdb_id": int(raw_tmdb_id) if raw_tmdb_id is not None else None,
    }


if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            raw_input = json.load(f)
        result = parse(raw_input)
        print(json.dumps(result, ensure_ascii=False, indent=2))
