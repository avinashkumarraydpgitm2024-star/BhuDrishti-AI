import re


def clean_landslide_type(value):
    if value is None:
        return "unknown"

    text = str(value).strip().lower()

    if not text or text in {"nan", "none", "missing", "unknown", "undetermined"}:
        return "unknown"

    text = text.replace("_", " ")
    text = re.sub(r"\s+", " ", text)

    return text


def categorize_landslide_type(value):
    text = clean_landslide_type(value)

    if text == "unknown":
        return "unknown"

    if "avalanche" in text:
        return "avalanche"

    if "flow" in text or "torrent" in text or "mudslide" in text:
        return "flow"

    if "fall" in text or "rockfall" in text:
        return "fall"

    if "spread" in text:
        return "spread"

    if "complex" in text or "combination" in text or "multiple failure" in text:
        return "complex"

    if "slide" in text or "slump" in text or "landslide" in text:
        return "slide"

    return "other"
