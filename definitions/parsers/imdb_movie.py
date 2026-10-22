import sys
import json

def parse(input_data: dict) -> dict:
    """
    Parses raw IMDb movie input dictionary into standardized movie schema.
    """
    return {
        "id": input_data.get("tconst") or input_data.get("id"),
        "title": input_data.get("primaryTitle") or input_data.get("title"),
        "original_title": input_data.get("originalTitle"),
        "year": int(input_data.get("startYear", 0)) if input_data.get("startYear") else None,
        "genres": input_data.get("genres", "").split(",") if isinstance(input_data.get("genres"), str) else input_data.get("genres", []),
        "overview": input_data.get("description", ""),
        "rating": float(input_data.get("averageRating", 0.0)) if input_data.get("averageRating") else None
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            raw_input = json.load(f)
        result = parse(raw_input)
        print(json.dumps(result, ensure_ascii=False, indent=2))
