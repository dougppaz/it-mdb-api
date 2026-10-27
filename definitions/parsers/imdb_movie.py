import json
import sys


def parse(input_data: dict) -> dict:
    """
    Parses raw IMDb movie input dictionary into standardized movie schema.
    """
    return {
        "id": input_data.get("tconst") or input_data.get("id"),
        "title": input_data.get("primaryTitle") or input_data.get("title"),
        "original_title": input_data.get("originalTitle"),
        "year": int(input_data.get("startYear", 0)) if input_data.get("startYear") else None,
        "overview": input_data.get("description", ""),
        "tmdb_poster_path": None,
        "tmdb_backdrop_path": None
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            raw_input = json.load(f)
        result = parse(raw_input)
        print(json.dumps(result, ensure_ascii=False, indent=2))
