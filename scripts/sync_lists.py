import requests
import os
import json

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE = "https://api.themoviedb.org/3"
HEADERS = {"accept": "application/json"}

def fetch_tmdb(endpoint, params={}):
    params["api_key"] = TMDB_API_KEY
    params.setdefault("region", "AU")
    params.setdefault("language", "en-AU")
    print(f"🔍 Fetching: {endpoint} | Params: {params}")
    res = requests.get(f"{TMDB_BASE}{endpoint}", params=params, headers=HEADERS)
    try:
        data = res.json()
    except ValueError:
        return []
    if res.status_code != 200 or "results" not in data:
        return []
    return data["results"]

def fetch_imdb_id(tmdb_id, media_type):
    url = f"/{media_type}/{tmdb_id}/external_ids"
    res = requests.get(f"{TMDB_BASE}{url}", params={"api_key": TMDB_API_KEY}, headers=HEADERS)
    try:
        return res.json().get("imdb_id")
    except ValueError:
        return None

def format_items(results, media_type):
    items = []
    for r in results:
        imdb_id = fetch_imdb_id(r["id"], media_type)
        if not imdb_id:
            continue
        items.append({"title": r.get("name") or r.get("title"), "imdb_id": imdb_id, "type": media_type})
    return items

def fetch_items_for_list(defn):
    endpoint = defn.get("endpoint", f"/discover/{defn['type']}")
    params = defn.get("tmdb_params", {})
    results = fetch_tmdb(endpoint, params)
    return format_items(results, defn["type"])

def save_to_json(slug, media_type, items):
    path = f"catalogs/{slug}-{media_type}.json"
    with open(os.path.join(os.getcwd(), path), "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2)
    print(f"✅ Saved {len(items)} items to {path}")

def get_category_list():
    return [
        {"slug": "netflix", "tmdb_params": {"with_networks": "213", "sort_by": "vote_average.desc"}, "name": "Netflix", "type": "tv"},
        {"slug": "netflix", "tmdb_params": {"with_networks": "213", "sort_by": "vote_average.desc"}, "name": "Netflix", "type": "movie"},
        {"slug": "disney", "tmdb_params": {"with_networks": "2739", "sort_by": "vote_average.desc"}, "name": "Disney+", "type": "tv"},
        {"slug": "disney", "tmdb_params": {"with_networks": "2739", "sort_by": "vote_average.desc"}, "name": "Disney+", "type": "movie"},
        {"slug": "prime", "tmdb_params": {"with_networks": "1024", "sort_by": "vote_average.desc"}, "name": "Prime Video", "type": "tv"},
        {"slug": "prime", "tmdb_params": {"with_networks": "1024", "sort_by": "vote_average.desc"}, "name": "Prime Video", "type": "movie"},
        {"slug": "apple", "tmdb_params": {"with_networks": "2552", "sort_by": "vote_average.desc"}, "name": "Apple TV+", "type": "tv"},
        {"slug": "apple", "tmdb_params": {"with_networks": "2552", "sort_by": "vote_average.desc"}, "name": "Apple TV+", "type": "movie"},
        {"slug": "popular", "endpoint": "/tv/popular", "name": "Popular", "type": "tv"},
        {"slug": "popular", "endpoint": "/movie/popular", "name": "Popular", "type": "movie"},
    ]
