import requests, json, re, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from bs4 import BeautifulSoup

def check_camp(name, url):
    res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(res.text, 'html.parser')
    print(f'\n=== {name} ===')

    # "인턴십 기회" 텍스트 주변 HTML
    tag = soup.find(string=lambda t: t and '인턴십 기회' in t)
    if tag:
        p = tag.parent
        for _ in range(4):
            p = p.parent
        print('[인턴십] 주변 HTML:')
        print(str(p)[:1000])

    # "프론트엔드" 텍스트 - RSC 안에만 있으면 script 태그에서 못 찾음
    # tags 필드 RSC에서 직접 추출
    parts = []
    for script in soup.find_all('script'):
        raw = (script.string or '').strip()
        if 'self.__next_f.push' not in raw:
            continue
        m = re.search(r'self\.__next_f\.push\(\[1,"(.+?)"\]\s*\)', raw, re.DOTALL)
        if m:
            try:
                parts.append(json.loads('"' + m.group(1) + '"'))
            except:
                parts.append(m.group(1).replace('\\"', '"'))
    full = '\n'.join(parts)

    # camp 오브젝트 파싱
    def extract_camp(rsc):
        marker = '"camp":{'
        idx = rsc.find(marker)
        if idx == -1: return None
        brace_start = idx + len('"camp":')
        depth, in_str, esc = 0, False, False
        for i in range(brace_start, len(rsc)):
            ch = rsc[i]
            if esc: esc = False; continue
            if ch == '\\' and in_str: esc = True; continue
            if ch == '"': in_str = not in_str; continue
            if in_str: continue
            if ch == '{': depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    try: return json.loads(rsc[brace_start:i+1])
                    except: return None
        return None

    camp = extract_camp(full)
    if camp:
        for f in ['tags', 'jobOpportunityValues', 'jobOpportunityText', 'jobSearchingServiceValues']:
            v = camp.get(f, '(없음)')
            print(f'  {f}: {json.dumps(v, ensure_ascii=False)[:200]}')

check_camp('likelion(채용연계)', 'https://boottent.com/camps/likelion-aiplus_20260427141930')
check_camp('kacnet(비채용)', 'https://boottent.com/camps/kacnet-javascript_20250429101938')
