"""Update the Worship tab of index.html with the latest sermon from the church YouTube channel.

Run weekly by .github/workflows/deploy.yml. Exits non-zero on any failure so the
workflow turns red (and GitHub emails the owner) instead of silently publishing
a broken page.
"""
import html
import json
import os
import re
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET

CHANNEL_ID = "UC56pX25Nm-DtOiY-MF0Z6wA"
RSS_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"
# Korean Revised Version (개역한글). The file's book names are Portuguese, so books
# are looked up by canonical order (index 0-65), never by name.
BIBLE_URL = "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/ko_krv.json"
INDEX_HTML_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "index.html")

# Canonical order, each book with its full name followed by abbreviations.
BOOKS = [
    ("창세기", "창"), ("출애굽기", "출"), ("레위기", "레"), ("민수기", "민"), ("신명기", "신"),
    ("여호수아", "수"), ("사사기", "삿"), ("룻기", "룻"), ("사무엘상", "삼상"), ("사무엘하", "삼하"),
    ("열왕기상", "왕상"), ("열왕기하", "왕하"), ("역대상", "대상"), ("역대하", "대하"), ("에스라", "스"),
    ("느헤미야", "느"), ("에스더", "에"), ("욥기", "욥"), ("시편", "시"), ("잠언", "잠"),
    ("전도서", "전"), ("아가", "아"), ("이사야", "사", "이사"), ("예레미야", "렘"), ("예레미야애가", "애"),
    ("에스겔", "겔"), ("다니엘", "단"), ("호세아", "호"), ("요엘", "욜"), ("아모스", "암"),
    ("오바댜", "오바디야", "옵"), ("요나", "욘"), ("미가", "미"), ("나훔", "나"), ("하박국", "합"),
    ("스바냐", "습"), ("학개", "학"), ("스가랴", "슥"), ("말라기", "말"),
    ("마태복음", "마"), ("마가복음", "막"), ("누가복음", "눅"), ("요한복음", "요"), ("사도행전", "행"),
    ("로마서", "롬"), ("고린도전서", "고전"), ("고린도후서", "고후"), ("갈라디아서", "갈"), ("에베소서", "엡"),
    ("빌립보서", "빌"), ("골로새서", "골"), ("데살로니가전서", "살전"), ("데살로니가후서", "살후"),
    ("디모데전서", "딤전"), ("디모데후서", "딤후"), ("디도서", "딛"), ("빌레몬서", "몬"), ("히브리서", "히"),
    ("야고보서", "약", "야"), ("베드로전서", "벧전"), ("베드로후서", "벧후"), ("요한일서", "요일"),
    ("요한이서", "요이"), ("요한삼서", "요삼"), ("유다서", "유"), ("요한계시록", "계"),
]
assert len(BOOKS) == 66

BOOK_INDEX = {}
for _i, _names in enumerate(BOOKS):
    for _n in _names:
        BOOK_INDEX.setdefault(_n, _i)  # first claim wins for ambiguous abbreviations ("사", "야")

# "고린도전서 12장", "히브리서 10:19-25", "고린도전서 10:31-11:1", "마태복음 8장 2-3절", "시편 23편"
SCRIPTURE_RE = re.compile(
    r"^\s*(?P<book>[가-힣]+)\s*(?P<ch>\d+)\s*(?:장|편|:)?\s*"
    r"(?:(?P<v1>\d+)\s*절?)?"
    r"(?:\s*-\s*(?:(?P<ch2>\d+)\s*:\s*)?(?P<v2>\d+)\s*절?)?"
    r"(?P<rest>.*)$"
)


class UpdateError(Exception):
    pass


def http_get(url, retries=3):
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read()
        except Exception as e:  # noqa: BLE001 - retry on any network error
            last = e
            time.sleep(2 * (attempt + 1))
    raise UpdateError(f"GET {url} failed: {last}")


def parse_scripture(text):
    """Return (book_index, chapter, v_start, ch_end, v_end) or None. Verse fields may be None."""
    text = text.replace("–", "-").replace("—", "-").replace("~", "-").replace("∼", "-")
    m = SCRIPTURE_RE.match(text)
    if not m or m["book"] not in BOOK_INDEX:
        return None
    ch = int(m["ch"])
    v1 = int(m["v1"]) if m["v1"] else None
    v2 = int(m["v2"]) if m["v2"] else None
    ch2 = int(m["ch2"]) if m["ch2"] else ch
    if v1 is not None and v2 is None and "이하" in m["rest"]:
        v2 = 10_000  # "11장 17절 이하" -> to the end of the chapter
    return BOOK_INDEX[m["book"]], ch, v1, ch2, v2


def format_scripture(scripture):
    """Fetch the verses and return HTML. Raises UpdateError on any problem."""
    parsed = parse_scripture(scripture)
    if not parsed:
        raise UpdateError(f"cannot parse scripture reference: {scripture!r}")
    book_i, ch, v1, ch2, v2 = parsed

    data = json.loads(http_get(BIBLE_URL).decode("utf-8-sig"))
    if len(data) != 66:
        raise UpdateError(f"unexpected Bible data: {len(data)} books")
    chapters = data[book_i]["chapters"]

    def verses_of(c, lo, hi):
        if c < 1 or c > len(chapters):
            raise UpdateError(f"chapter {c} out of range for {scripture!r}")
        verses = chapters[c - 1]
        lo = lo or 1
        hi = min(hi or len(verses), len(verses))
        if lo > hi:
            raise UpdateError(f"bad verse range in {scripture!r}")
        return [(i, html.escape(html.unescape(verses[i - 1]).strip())) for i in range(lo, hi + 1)]

    if v1 is None:
        picked = verses_of(ch, None, None)
    elif ch2 == ch:
        picked = verses_of(ch, v1, v2 or v1)
    else:  # cross-chapter, e.g. 10:31-11:1
        picked = verses_of(ch, v1, None) + verses_of(ch2, 1, v2)
    return "<br><br>\n                ".join(f"{n} {t}" for n, t in picked)


def split_title(full_title):
    """'제목｜본문 | 설교자' -> (title, scripture, preacher), or None if not a full sermon video."""
    parts = [p.strip() for p in re.split(r"[|｜]", full_title) if p.strip()]
    if len(parts) < 2:
        return None
    scripture = next((p for p in parts[1:] if parse_scripture(p)), None)
    if not scripture:
        return None
    preacher = next((p for p in parts[1:] if p != scripture), "")
    return parts[0], scripture, preacher


SKIP_KEYWORDS = ("http", "instagram", "naver", "pf.kakao", "youtube", "계좌", "농협", "카카오", "문의")
LABEL_LINE_RE = re.compile(r"^[가-힣 ]{2,8}\s*[:：]")  # "찬양인도 : …", "촬영 : …"


def clean_description_to_summary(description):
    paragraphs, current = [], []
    for raw in (description or "").splitlines():
        line = raw.strip()
        if line and (any(k in line.lower() for k in SKIP_KEYWORDS) or LABEL_LINE_RE.match(line)):
            continue
        if line:
            current.append(line)
        elif current:
            paragraphs.append(" ".join(current))
            current = []
    if current:
        paragraphs.append(" ".join(current))
    paragraphs = [p for p in paragraphs if len(p) > 5]
    if not paragraphs:
        paragraphs = ["이번 주일 설교 말씀입니다. 예배 영상과 성경 봉독을 통해 은혜로운 시간 되시길 바랍니다."]
    return "\n                ".join(f'<p style="margin-bottom: 12px;">{html.escape(p)}</p>' for p in paragraphs)


def replace_between(content, name, replacement):
    start_marker, end_marker = f"<!-- {name}_START -->", f"<!-- {name}_END -->"
    s = content.find(start_marker)
    e = content.find(end_marker, s + len(start_marker)) if s != -1 else -1
    if s == -1 or e == -1:
        raise UpdateError(f"marker pair {name} not found in index.html")
    return content[: s + len(start_marker)] + replacement + content[e:]


VIDEO_BLOCK = """
            <div class="video-wrapper" id="sermon-video-container" data-video-id="{vid}" onclick="playSermonVideo(this)" style="position: relative; width: 100%; aspect-ratio: 16 / 9; border-radius: 16px; overflow: hidden; box-shadow: 0 12px 32px rgba(0, 0, 0, 0.3); background-color: #000; cursor: pointer;">
              <!-- High-resolution thumbnail image from i.ytimg.com CDN -->
              <img src="https://i.ytimg.com/vi/{vid}/maxresdefault.jpg"
                   onerror="this.src='https://i.ytimg.com/vi/{vid}/hqdefault.jpg'"
                   alt="Sermon Thumbnail"
                   style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; display: block; border: 0;" />

              <!-- Soft darken overlay -->
              <div class="video-cover-overlay" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.15); z-index: 1;"></div>

              <!-- Centered Play Button -->
              <div class="video-play-btn" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); z-index: 2; width: 64px; height: 64px; background: rgba(255, 255, 255, 0.95); color: #3f6355; border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3); transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);">
                <svg viewBox="0 0 24 24" width="28" height="28" fill="currentColor" style="transform: translateX(2px);">
                  <polygon points="6 3 20 12 6 21 6 3"></polygon>
                </svg>
              </div>
            </div>
            """


# Only the Sunday service goes on the bulletin; other services upload full sermons too.
OTHER_SERVICE_KEYWORDS = ("금요", "수요", "새벽")


def find_latest_sermon(root):
    ns = {"atom": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015",
          "media": "http://search.yahoo.com/mrss/"}
    for entry in root.findall("atom:entry", ns):
        title = entry.findtext("atom:title", default="", namespaces=ns)
        split = split_title(title)
        if not split:  # shorts / clips have no "｜본문 | 설교자" part
            continue
        group = entry.find("media:group", ns)
        desc = group.findtext("media:description", default="", namespaces=ns) if group is not None else ""
        if any(k in title + desc for k in OTHER_SERVICE_KEYWORDS):
            print(f"Skipping non-Sunday service: {title}")
            continue
        return entry.findtext("yt:videoId", namespaces=ns), title, split, desc
    raise UpdateError("no Sunday full-sermon video (title with 본문 and 설교자) found in the RSS feed")


def main():
    print("Fetching YouTube RSS feed...")
    root = ET.fromstring(http_get(RSS_URL))
    video_id, full_title, (title, scripture, preacher), description = find_latest_sermon(root)
    print(f"Latest sermon: {video_id} | {full_title}")

    with open(INDEX_HTML_PATH, encoding="utf-8") as f:
        content = f.read()
    if f'data-video-id="{video_id}"' in content:
        print("Already up to date.")
        return

    try:
        quote = format_scripture(scripture)
    except UpdateError as e:
        # A Bible-text outage must not block the new video; show the reference only.
        print(f"::warning::Bible text unavailable, showing reference only: {e}")
        quote = html.escape(scripture)

    esc = html.escape
    subtitle = f"{esc(preacher)} | {esc(scripture)}" if preacher else esc(scripture)
    content = replace_between(content, "SERMON_TITLE", esc(title))
    content = replace_between(content, "SERMON_SUBTITLE", subtitle)
    content = replace_between(content, "SERMON_VIDEO", VIDEO_BLOCK.format(vid=video_id))
    content = replace_between(content, "SCRIPTURE_META", esc(scripture))
    content = replace_between(content, "SCRIPTURE_QUOTE", f"\n                {quote}\n                ")
    content = replace_between(content, "SERMON_SUMMARY", f"\n                {clean_description_to_summary(description)}\n                ")

    with open(INDEX_HTML_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print("index.html updated.")


if __name__ == "__main__":
    try:
        main()
    except (UpdateError, ET.ParseError, OSError, ValueError) as e:
        print(f"::error::{e}")
        sys.exit(1)
