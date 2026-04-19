import requests

WIKI_API_URL = "https://en.wikipedia.org/w/api.phpg"

def get_wikipedia_page_content(title):
    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "explaintext": True,
        "titles": title
    }

    try:
        response = requests.get(WIKI_API_URL, params=params, timeout=5)
        if response.status_code != 200:
            return "Request failed."

        data = response.json()

        pages = data.get("query", {}).get("pages", {})
        page = next(iter(pages.values()), {})

        if "missing" in page:
            return "Page not found."

        text = page.get("extract", "")
        if not text:
            return "No content found."

        return text[:1000]

    except requests.exceptions.RequestException:
        return "Network error."

if __name__ == "__main__":
    title = input("Enter the Wikipedia page title: ")
    content = get_wikipedia_page_content(title)
    print(content)