# jwst-timing.github.io

Website of the JWST Timing Consortium: <https://jwst-timing.github.io>

GitHub Pages builds the site with Jekyll automatically whenever you push to
`master`. There is nothing to install or compile. Changes usually go live within
a minute or two (progress is shown under the repository's **Actions** tab).

## Add a publication

1. Open `_data/publications.yml` (you can edit it directly on github.com with the pencil icon).
2. Copy an existing block and paste it **at the top** (the list is newest first).
3. Edit the fields and commit.

```yaml
- year: 2027
  authors: Surname, A. B., et al.
  title: "Title of the paper"        # use quotes if the title contains a colon
  journal: MNRAS, 550, 123
  doi: 10.1093/mnras/xxxxx            # optional, links to the journal
  arxiv: 2701.01234                   # optional
  url: https://...                    # optional, for anything without a DOI
  summary: One plain-language sentence about the result.   # optional
```

The newest three papers also appear under "Recent results" on the home page
(change `home_recent` in `_config.yml` to show more or fewer).

## Add or update a team member

Edit `_data/team.yml`. `role` is optional (e.g. `PI`, `co-PI`).

## Other edits

| What | Where |
|---|---|
| Contact details, navigation menu | `_config.yml` |
| Header / footer (shared by every page) | `_includes/header.html`, `_includes/footer.html` |
| Page text | `index.html`, `calibration.html`, `instruments.html` |
| Colours and fonts | `assets/css/site.css` (variables at the top) |

## Previewing locally (optional)

Either install Jekyll (`gem install jekyll`, then `jekyll serve`), or use the
lightweight stand-in, which needs only Python:

```sh
pip install 'python-liquid>=2' pyyaml
python3 tools/preview.py
python3 -m http.server -d _preview 8000   # open http://localhost:8000
```
