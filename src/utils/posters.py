import requests


def get_poster_url(movie_title: str):
    url = "https://en.wikipedia.org/w/api.php"

    params = {
        "action": "query",
        "generator": "search",
        "gsrsearch": f"{movie_title} film",
        "gsrlimit": 1,
        "prop": "pageimages",
        "piprop": "thumbnail",
        "pithumbsize": 500,
        "format": "json",
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=5
        )

        response.raise_for_status()

        data = response.json()

        pages = data.get("query", {}).get("pages", {})

        if pages:
            page = next(iter(pages.values()))

            thumbnail = page.get("thumbnail")

            if thumbnail:
                return thumbnail.get("source")

    except requests.RequestException:
        pass

    return None