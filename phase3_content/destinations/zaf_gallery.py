"""Posts to the ZAF Consultancy website's public gallery page.

Goes through a scoped API route + its own secret (ZAF_GALLERY_API_URL,
ZAF_GALLERY_API_KEY) — deliberately never touches the live ZAF Portal
database directly.

Not implemented yet — waiting on that API route to exist on the ZAF
Portal side.
"""


def post(image_url, caption):
    raise NotImplementedError("ZAF gallery API route not built yet")
