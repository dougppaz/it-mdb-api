import sys
import json

def parse(input_data: dict) -> dict:
    """
    Parses raw TMDB movie input dictionary into standardized movie schema.
    """
    return {
        "id": str(input_data.get("id")),
        "title": input_data.get("title") or input_data.get("name"),
        "original_title": input_data.get("original_title"),
        "year": int(input_data.get("release_date", "0").split("-")[0]) if input_data.get("release_date") else None,
        "genres": [genre.get("name") for genre in input_data.get("genres", []) if isinstance(genre, dict)],
        "overview": input_data.get("overview", ""),
        "rating": float(input_data.get("vote_average", 0.0)) if input_data.get("vote_average") else None
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            raw_input = json.load(f)
        result = parse(raw_input)
        print(json.dumps(result, ensure_ascii=False, indent=2))
