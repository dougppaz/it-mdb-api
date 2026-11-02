import json
import sys


def parse(input_data: dict) -> list:
    """
    Parses raw TMDB multi-search input dictionary (containing search results and external ids map with integer keys)
    into a list of standardized search-item-v1 dictionaries.
    """
    search_data = input_data.get("search", {})
    results = search_data.get("results", [])
    external_ids_map = input_data.get("external_ids", {})

    parsed_items = []
    for item in results:
        media_type = item.get("media_type")
        if media_type not in ("movie", "tv"):
            continue

        tmdb_id = item.get("id")
        ext_ids = external_ids_map.get(tmdb_id, {})
        imdb_id = ext_ids.get("imdb_id")

        date_str = item.get("release_date") or item.get("first_air_date")
        year = int(date_str.split("-")[0]) if date_str and "-" in date_str else None

        parsed_items.append(
            {
                "id": str(tmdb_id) if tmdb_id is not None else None,
                "title": item.get("title") or item.get("name"),
                "original_title": item.get("original_title") or item.get("original_name"),
                "year": year,
                "overview": item.get("overview", ""),
                "tmdb_poster_path": item.get("poster_path"),
                "tmdb_backdrop_path": item.get("backdrop_path"),
                "imdb_id": str(imdb_id) if imdb_id is not None else None,
                "tmdb_id": int(tmdb_id) if tmdb_id is not None else None,
                "media_type": media_type,
            }
        )

    return parsed_items


if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            raw_input = json.load(f)
        if "external_ids" in raw_input:
            raw_input["external_ids"] = {
                int(k): v for k, v in raw_input["external_ids"].items()
            }
        result = parse(raw_input)
        print(json.dumps(result, ensure_ascii=False, indent=2))
