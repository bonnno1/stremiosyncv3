from scripts.sync_lists import get_category_list, fetch_items_for_list, save_to_json

def main():
    for category in get_category_list():
        print(f"⏳ Processing: {category['name']}")
        items = fetch_items_for_list(category)
        if not items:
            print(f"⚠️ No data returned for {category['slug']}")
            continue
        save_to_json(category['slug'], category['type'], items)

if __name__ == "__main__":
    main()
