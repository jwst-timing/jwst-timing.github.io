#!/usr/bin/env python3
"""Optional local preview without installing Jekyll.

GitHub Pages builds the real site with Jekyll on every push; you do not need
this. It is a small stand-in that understands the subset of Jekyll this site
uses (front matter, layouts, includes, _data, _config.yml).

    pip install 'python-liquid>=2' pyyaml
    python3 tools/preview.py          # builds into _preview/
    python3 -m http.server -d _preview 8000   # then open http://localhost:8000
"""
import datetime, re, shutil, sys
from pathlib import Path

import yaml
from liquid import Environment, DictLoader

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / (sys.argv[1] if len(sys.argv) > 1 else "_preview")

INCLUDE_RE = re.compile(r"{%-?\s*include\s+([\w./-]+)(.*?)-?%}")
ARG_RE = re.compile(r"(\w+)=(\S+)")


def jekyll_to_liquid(src: str) -> str:
    """Rewrite Jekyll-style includes ({% include x.html a=b %}) for python-liquid."""
    def sub(m):
        args = "".join(f", {k}: {v}" for k, v in ARG_RE.findall(m.group(2)))
        return "{% include '" + m.group(1) + "'" + args + " %}"
    return INCLUDE_RE.sub(sub, src)


def split_front_matter(text: str):
    if text.startswith("---"):
        _, fm, body = text.split("---", 2)
        return yaml.safe_load(fm) or {}, body
    return None, text


def main():
    config = yaml.safe_load((ROOT / "_config.yml").read_text())
    site = dict(config)
    site["time"] = datetime.datetime.now()
    site["data"] = {p.stem: yaml.safe_load(p.read_text()) for p in (ROOT / "_data").glob("*.yml")}

    templates = {}
    for p in (ROOT / "_includes").iterdir():
        # Jekyll exposes include parameters as include.x; python-liquid passes them as x.
        templates[p.name] = jekyll_to_liquid(p.read_text()).replace("include.", "")
    env = Environment(loader=DictLoader(templates))
    layouts = {p.stem: split_front_matter(p.read_text())[1] for p in (ROOT / "_layouts").glob("*.html")}

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copytree(ROOT / "assets", OUT / "assets")

    skip = set(config.get("exclude", [])) | {"_preview"}
    for page_path in ROOT.glob("*.html"):
        if page_path.name in skip:
            continue
        fm, body = split_front_matter(page_path.read_text())
        if fm is None:
            shutil.copy(page_path, OUT / page_path.name)
            continue
        page = dict(fm, url="/" + page_path.name)
        content = env.parse(jekyll_to_liquid(body)).render(dict(site=site, page=page))
        if "layout" in fm:
            content = env.parse(jekyll_to_liquid(layouts[fm["layout"]])).render(
                dict(site=site, page=page, content=content))
        (OUT / page_path.name).write_text(content)
        print("built", page_path.name)


if __name__ == "__main__":
    main()
