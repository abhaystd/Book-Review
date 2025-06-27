mock_cache = {}

def get_books_cache():
    return mock_cache.get("books")

def set_books_cache(data):
    mock_cache["books"] = data

def clear_books_cache():
    mock_cache.pop("books", None)