#!/usr/bin/env python3
"""원티드 API → jobs.html 공고 자동 업데이트"""
import urllib.request, json, re
from datetime import date, datetime

def fetch_jobs(limit=30):
    url = f"https://www.wanted.co.kr/api/v4/jobs?country=kr&job_sort=job.latest_order&limit={limit}&offset=0"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read())["data"]
    except Exception as e:
        print(f"API 오류: {e}")
        return []

jobs = fetch_jobs(30)
print(f"공고 {len(jobs)}개 가져옴")

if not jobs:
    print("공고 없음 - 기존 파일 유지")
    exit(0)

# jobs 데이터 변환
result = []
for j in jobs:
    due = j.get("due_time")
    if due:
        try: due_str = datetime.fromisoformat(due[:10]).strftime("%m.%d 마감")
        except: due_str = "날짜 확인"
    else:
        due_str = "상시채용"
    result.append({
        "company": j.get("company", {}).get("name", ""),
        "title": j.get("position", ""),
        "due": due_str,
        "url": f"https://www.wanted.co.kr/wd/{j.get('id','')}",
    })

# jobs.html 내 STATIC_JOBS 교체
with open("jobs.html", "r", encoding="utf-8") as f:
    content = f.read()

jobs_json = json.dumps(result, ensure_ascii=False)
content = re.sub(r'const STATIC_JOBS = .*?;', f'const STATIC_JOBS = {jobs_json};', content)

with open("jobs.html", "w", encoding="utf-8") as f:
    f.write(content)

today = date.today().strftime("%Y.%m.%d")
print(f"jobs.html 업데이트 완료 ({today}, {len(result)}개 공고)")
