"""Offline source checks only; no browser, HTTP, credentials, or publication."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent
PRIVATE = "https://rainier-nas.tail03f55a.ts.net:8444/"


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()
        self.meta = {}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        assert tag not in {"script", "form", "input", "iframe", "object", "embed"}
        assert not any(key.startswith("on") for key in attrs)
        if "id" in attrs:
            assert attrs["id"] not in self.ids
            self.ids.add(attrs["id"])
        if tag == "meta":
            self.meta[attrs.get("name", attrs.get("http-equiv", "")).lower()] = attrs.get("content")
        if "href" in attrs:
            self.links.append(attrs["href"])
        assert "src" not in attrs, "The public pages make no external resource requests."


if __name__ == "__main__":
    assert (ROOT / "CNAME").read_text().strip() == "rainier.app"
    assert (ROOT / ".nojekyll").is_file()
    pages = {}
    for name in ("index.html", "household.html"):
        page = Page()
        page.feed((ROOT / name).read_text())
        assert "main" in page.ids
        assert page.meta["referrer"] == "no-referrer"
        assert "default-src 'none'" in page.meta["content-security-policy"]
        assert "form-action 'none'" in page.meta["content-security-policy"]
        for href in page.links:
            value = urlsplit(href)
            assert not value.query and not value.username and not value.password
            if value.scheme:
                assert href in {PRIVATE, "mailto:contact@rainier.app"}
            elif value.fragment:
                assert not value.path and value.fragment in page.ids
            else:
                assert value.path in {"index.html", "household.html", "privacy.html", "terms.html", "site.css"}
                assert (ROOT / value.path).is_file()
        pages[name] = page
    assert PRIVATE in pages["household.html"].links
    assert PRIVATE not in pages["index.html"].links
    print("Public welcome/access source checks passed; private sign-in remains separate.")
