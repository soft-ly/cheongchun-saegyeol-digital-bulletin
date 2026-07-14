import urllib.request
import json
import xml.etree.ElementTree as ET
import re
import html
import os

# 1. Configuration
CHANNEL_ID = "UC56pX25Nm-DtOiY-MF0Z6wA"
RSS_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"
INDEX_HTML_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "index.html")

# Bible Books mapping dictionary
BIBLE_BOOKS_MAP = {
    # 구약 (Old Testament)
    "창세기": "Genesis", "창": "Genesis",
    "출애굽기": "Exodus", "출": "Exodus",
    "레위기": "Leviticus", "레": "Leviticus",
    "민수기": "Numbers", "민": "Numbers",
    "신명기": "Deuteronomy", "신": "Deuteronomy",
    "여호수아": "Joshua", "수": "Joshua",
    "사사기": "Judges", "사": "Judges",
    "룻기": "Ruth", "룻": "Ruth",
    "사무엘상": "1 Samuel", "삼상": "1 Samuel",
    "사무엘하": "2 Samuel", "삼하": "2 Samuel",
    "열왕기상": "1 Kings", "왕상": "1 Kings",
    "열왕기하": "2 Kings", "왕하": "2 Kings",
    "역대상": "1 Chronicles", "대상": "1 Chronicles",
    "역대하": "2 Chronicles", "대하": "2 Chronicles",
    "에스라": "Ezra", "스": "Ezra",
    "느헤미야": "Nehemiah", "느": "Nehemiah",
    "에스더": "Esther", "에": "Esther",
    "욥기": "Job", "욥": "Job",
    "시편": "Psalms", "시": "Psalms",
    "잠언": "Proverbs", "잠": "Proverbs",
    "전도서": "Ecclesiastes", "전": "Ecclesiastes",
    "아가": "Song of Solomon", "아": "Song of Solomon",
    "이사야": "Isaiah", "이사": "Isaiah",
    "예레미야": "Jeremiah", "렘": "Jeremiah",
    "예레미야애가": "Lamentations", "애": "Lamentations",
    "에스겔": "Ezekiel", "겔": "Ezekiel",
    "다니엘": "Daniel", "단": "Daniel",
    "호세아": "Hosea", "호": "Hosea",
    "요엘": "Joel", "욜": "Joel",
    "아모스": "Amos", "암": "Amos",
    "오바디야": "Obadiah", "옵": "Obadiah",
    "요나": "Jonah", "욘": "Jonah",
    "미가": "Micah", "미": "Micah",
    "나훔": "Nahum", "나": "Nahum",
    "하박국": "Habakkuk", "합": "Habakkuk",
    "스바냐": "Zephaniah", "습": "Zephaniah",
    "학개": "Haggai", "학": "Haggai",
    "스가랴": "Zechariah", "슥": "Zechariah",
    "말라기": "Malachi", "말": "Malachi",
    
    # 신약 (New Testament)
    "마태복음": "Matthew", "마": "Matthew",
    "마가복음": "Mark", "막": "Mark",
    "누가복음": "Luke", "눅": "Luke",
    "요한복음": "John", "요": "John",
    "사도행전": "Acts", "행": "Acts",
    "로마서": "Romans", "롬": "Romans",
    "고린도전서": "1 Corinthians", "고전": "1 Corinthians",
    "고린도후서": "2 Corinthians", "고후": "2 Corinthians",
    "갈라디아서": "Galatians", "갈": "Galatians",
    "에베소서": "Ephesians", "엡": "Ephesians",
    "빌립보서": "Philippians", "빌": "Philippians",
    "골로새서": "Colossians", "골": "Colossians",
    "데살로니가전서": "1 Thessalonians", "살전": "1 Thessalonians",
    "데살로니가후서": "2 Thessalonians", "살후": "2 Thessalonians",
    "디모데전서": "1 Timothy", "딤전": "1 Timothy",
    "디모데후서": "2 Timothy", "딤후": "2 Timothy",
    "디도서": "Titus", "딛": "Titus",
    "빌레몬서": "Philemon", "몬": "Philemon",
    "히브리서": "Hebrews", "히": "Hebrews",
    "야고보서": "James", "야": "James",
    "베드로전서": "1 Peter", "벧전": "1 Peter",
    "베드로후서": "2 Peter", "벧후": "2 Peter",
    "요한일서": "1 John", "요일": "1 John",
    "요한이서": "2 John", "요이": "2 John",
    "요한삼서": "3 John", "요삼": "3 John",
    "유다서": "Jude", "유": "Jude",
    "요한계시록": "Revelation", "계": "Revelation"
}

def parse_scripture(scripture_str):
    """Parses Book, Chapter, Start Verse, End Verse from a scripture string."""
    scripture_str = scripture_str.strip()
    # Matches: "마태복음 8:2-3", "마태복음 8장 2-3절"
    match = re.search(r'([1-3]?\s*[a-zA-Z가-힣\s]+?)\s*(\d+)\s*(?:장|:)\s*(\d+)(?:\s*(?:-|~)\s*(\d+))?', scripture_str)
    if match:
        book_raw = match.group(1).strip()
        chapter = int(match.group(2))
        start_v = int(match.group(3))
        end_v = int(match.group(4)) if match.group(4) else None
        return book_raw, chapter, start_v, end_v
    
    # Matches: "고린도전서 1장", "고린도전서 1"
    match_chap = re.search(r'([1-3]?\s*[a-zA-Z가-힣\s]+?)\s*(\d+)\s*장?', scripture_str)
    if match_chap:
        book_raw = match_chap.group(1).strip()
        chapter = int(match_chap.group(2))
        return book_raw, chapter, None, None
        
    return None

def fetch_and_format_bible(scripture_str):
    """Fetches scripture text from online JSON repository and formats it with HTML tags."""
    parsed = parse_scripture(scripture_str)
    if not parsed:
        print(f"Could not parse scripture query: {scripture_str}")
        return scripture_str  # Return original string as fallback
    
    book_raw, chapter, start_v, end_v = parsed
    
    # Map raw book name to English book name
    english_book = BIBLE_BOOKS_MAP.get(book_raw)
    if not english_book:
        for k, v in BIBLE_BOOKS_MAP.items():
            if k.lower() == book_raw.lower() or book_raw.replace(" ", "") in k:
                english_book = v
                break
                
    if not english_book:
        print(f"Unknown Bible book: {book_raw}")
        return scripture_str
        
    url = "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/ko_ko.json"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8-sig'))
            
            target_book = None
            for b in data:
                if b['name'].lower() == english_book.lower():
                    target_book = b
                    break
                    
            if not target_book:
                print(f"Book not found in Bible data: {english_book}")
                return scripture_str
                
            chapters = target_book['chapters']
            if chapter < 1 or chapter > len(chapters):
                print(f"Chapter {chapter} out of range (max {len(chapters)})")
                return scripture_str
                
            chapter_verses = chapters[chapter - 1]
            
            formatted_verses = []
            if start_v is None:
                # Whole chapter
                for i, v_text in enumerate(chapter_verses):
                    v_clean = html.unescape(v_text).strip()
                    formatted_verses.append(f"{i+1} {v_clean}")
            elif end_v is None:
                # Single verse
                if start_v < 1 or start_v > len(chapter_verses):
                    print(f"Verse {start_v} out of range in chapter {chapter}")
                    return scripture_str
                v_clean = html.unescape(chapter_verses[start_v - 1]).strip()
                formatted_verses.append(f"{start_v} {v_clean}")
            else:
                # Verse range
                if start_v < 1 or end_v > len(chapter_verses) or start_v > end_v:
                    print(f"Verse range {start_v}-{end_v} invalid/out of range")
                    return scripture_str
                for idx in range(start_v, end_v + 1):
                    v_clean = html.unescape(chapter_verses[idx - 1]).strip()
                    formatted_verses.append(f"{idx} {v_clean}")
                    
            # Join with <br><br> and indent for index.html aesthetics
            return "<br><br>\n                ".join(formatted_verses)
            
    except Exception as e:
        print(f"Error fetching Bible text: {e}")
        return scripture_str

def clean_description_to_summary(description):
    """Processes raw YouTube video description and extracts clean sermon summary paragraphs."""
    if not description:
        return ""
        
    lines = description.splitlines()
    clean_lines = []
    
    # Filter phrases that indicate contact info, donation, or other metadata
    filter_keywords = [
        "http", "instagram", "naver", "pf.kakao", "youtube", "계좌", "농협", "카카오", 
        "헌금", "온라인", "문의", "안내", "위치", "보은", "목사", "일시", "예배", "등록",
        "찬양인도", "반주", "촬영", "사진", "편집", "디자인", "본문", "설교자"
    ]
    
    for line in lines:
        line_strip = line.strip()
        if not line_strip:
            clean_lines.append("")
            continue
            
        # Check if line should be filtered out
        should_filter = False
        for kw in filter_keywords:
            if kw in line_strip or kw in line_strip.replace(" ", ""):
                should_filter = True
                break
                
        if not should_filter:
            clean_lines.append(line_strip)
            
    # Reassemble paragraphs
    paragraphs = []
    current_para = []
    for line in clean_lines:
        if line == "":
            if current_para:
                paragraphs.append(" ".join(current_para))
                current_para = []
        else:
            current_para.append(line)
            
    if current_para:
        paragraphs.append(" ".join(current_para))
        
    # Format paragraphs into HTML p tags
    html_paragraphs = []
    for p in paragraphs:
        # Avoid empty paragraphs or single character lines
        if len(p) > 5:
            html_paragraphs.append(f'<p style="margin-bottom: 12px;">{p}</p>')
            
    # Add a concluding signature/prayer if not empty
    if html_paragraphs:
        return "\n                ".join(html_paragraphs)
    else:
        return '<p style="margin-bottom: 12px;">이번 주일 설교 말씀입니다. 예배 영상과 성경 봉독을 통해 은혜로운 시간 되시길 바랍니다.</p>'

def replace_between(content, start_marker, end_marker, replacement):
    """Helper function to find and replace substring between markers."""
    start_idx = content.find(start_marker)
    if start_idx == -1:
        print(f"Warning: Marker '{start_marker}' not found")
        return content
    end_idx = content.find(end_marker, start_idx + len(start_marker))
    if end_idx == -1:
        print(f"Warning: Marker '{end_marker}' not found")
        return content
    return content[:start_idx + len(start_marker)] + replacement + content[end_idx:]

def main():
    print("Fetching YouTube RSS feed...")
    req = urllib.request.Request(RSS_URL, headers={'User-Agent': 'Mozilla/5.0'})
    
    try:
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()
            
        root = ET.fromstring(xml_data)
        namespaces = {
            'atom': 'http://www.w3.org/2005/Atom',
            'yt': 'http://www.youtube.com/xml/schemas/2015',
            'media': 'http://search.yahoo.com/mrss/'
        }
        
        entries = root.findall('atom:entry', namespaces)
        if not entries:
            print("No video entries found in RSS feed")
            return
            
        latest_entry = entries[0]
        video_id = latest_entry.find('yt:videoId', namespaces).text
        full_title = latest_entry.find('atom:title', namespaces).text
        published = latest_entry.find('atom:published', namespaces).text
        
        media_group = latest_entry.find('media:group', namespaces)
        description = ""
        if media_group is not None:
            description = media_group.find('media:description', namespaces).text
            
        print(f"Latest video ID: {video_id}")
        print(f"Latest title: {full_title}")
        print(f"Published date: {published}")
        
        # Read index.html
        if not os.path.exists(INDEX_HTML_PATH):
            print(f"Error: index.html not found at path: {INDEX_HTML_PATH}")
            return
            
        with open(INDEX_HTML_PATH, "r", encoding="utf-8") as f:
            html_content = f.read()
            
        # Check if the video is already featured
        if f'data-video-id="{video_id}"' in html_content:
            print("Worship tab is already up-to-date with this video. Skipping update.")
            return
            
        # Parse title: "제목 | 본문구절 | 설교자"
        parts = [p.strip() for p in full_title.split("|")]
        title = parts[0]
        scripture_meta = parts[1] if len(parts) > 1 else ""
        preacher = parts[2] if len(parts) > 2 else "설교자"
        
        print(f"Parsed Title: {title}")
        print(f"Parsed Scripture: {scripture_meta}")
        print(f"Parsed Preacher: {preacher}")
        
        # Fetch Bible Text
        bible_text = scripture_meta
        if scripture_meta:
            bible_text = fetch_and_format_bible(scripture_meta)
            
        # Format Sermon Summary
        sermon_summary = clean_description_to_summary(description)
        
        # Generate video wrapper block
        video_block = f"""
            <div class="video-wrapper" id="sermon-video-container" data-video-id="{video_id}" onclick="playSermonVideo(this)" style="position: relative; width: 100%; aspect-ratio: 16 / 9; border-radius: 16px; overflow: hidden; box-shadow: 0 12px 32px rgba(0, 0, 0, 0.3); background-color: #000; cursor: pointer;">
              <!-- High-resolution thumbnail image from i.ytimg.com CDN -->
              <img src="https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg" 
                   onerror="this.src='https://i.ytimg.com/vi/{video_id}/hqdefault.jpg'" 
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
            
        # Replace content between markers
        updated_content = html_content
        updated_content = replace_between(updated_content, "<!-- SERMON_TITLE_START -->", "<!-- SERMON_TITLE_END -->", title)
        updated_content = replace_between(updated_content, "<!-- SERMON_SUBTITLE_START -->", "<!-- SERMON_SUBTITLE_END -->", f"{preacher} | {scripture_meta}")
        updated_content = replace_between(updated_content, "<!-- SERMON_VIDEO_START -->", "<!-- SERMON_VIDEO_END -->", video_block)
        updated_content = replace_between(updated_content, "<!-- SCRIPTURE_META_START -->", "<!-- SCRIPTURE_META_END -->", scripture_meta)
        updated_content = replace_between(updated_content, "<!-- SCRIPTURE_QUOTE_START -->", "<!-- SCRIPTURE_QUOTE_END -->", f"\n                {bible_text}\n                ")
        updated_content = replace_between(updated_content, "<!-- SERMON_SUMMARY_START -->", "<!-- SERMON_SUMMARY_END -->", f"\n                {sermon_summary}\n                ")
        
        # Write back to index.html
        with open(INDEX_HTML_PATH, "w", encoding="utf-8") as f:
            f.write(updated_content)
            
        print("index.html successfully updated with the latest sermon info!")
        
    except Exception as e:
        print(f"Error executing auto update: {e}")

if __name__ == "__main__":
    main()
