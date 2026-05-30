#!/usr/bin/env python3
"""
채용 공고 자동 업데이트 스크립트
원티드 API → jobs.html 생성
"""
import urllib.request, urllib.error, json, re
from datetime import date, datetime

# ──────────────────────────────────────────
# 설정
# ──────────────────────────────────────────
SITE_NAME = "좋은 취업"
BASE_URL  = "https://jobok.co.kr"
EBOOK_URL = "https://www.latpeed.com/products/Ge7M-"

# 관심 직군 ID (원티드 기준)
CATEGORIES = {
    "마케팅/PR": 518,
    "개발": 518,     # 실제로는 다른 ID 사용
    "기획/전략": 507,
    "영업/제휴": 512,
    "디자인": 511,
    "HR/조직문화": 517,
}

# 기업 분석 DB (자주 채용하는 기업들)
COMPANY_ANALYSIS = {
    "카카오": {
        "인재상": "데이터로 서비스를 개선한 경험. 사용자 문제를 정의하고 해결책을 만드는 능력.",
        "문화": "자율과 책임. 수평적. 빠른 실험과 개선.",
        "팁": "카카오 서비스 직접 사용·분석 경험을 자소서에 쓰세요.",
        "준비": "포트폴리오 필수. 데이터 분석 경험 강조."
    },
    "토스": {
        "인재상": "복잡한 것을 단순하게 만드는 능력. 사용자 관점의 언어 감각.",
        "문화": "높은 자율성. 빠른 실험. 직접 의견 말하는 문화.",
        "팁": "토스 앱 UX 문구 분석 후 개선 제안을 포트폴리오로 만드세요.",
        "준비": "포트폴리오 필수. 실제 개선 사례 준비."
    },
    "쿠팡": {
        "인재상": "데이터로 운영 효율을 높인 경험. 빠른 실행력.",
        "문화": "빠르고 치열한 문화. 성과 중심. 데이터 기반.",
        "팁": "운영 개선 경험을 수치로 표현하세요.",
        "준비": "SQL·엑셀 기본 필수."
    },
    "네이버": {
        "인재상": "기술과 사용자 이해를 동시에 갖춘 인재.",
        "문화": "전문성 중심. 자율과 책임.",
        "팁": "네이버 서비스 분석과 개선 제안을 준비하세요.",
        "준비": "직무별 필기 + 포트폴리오."
    },
    "삼성전자": {
        "인재상": "도전 정신과 창의성. 글로벌 역량.",
        "문화": "성과 중심. 글로벌 협업.",
        "팁": "최근 반도체·AI 시장 동향을 파악하세요.",
        "준비": "GSAT 인적성 필수."
    },
    "현대자동차": {
        "인재상": "도전 정신과 실행력. 전동화 시대를 이끌 미래형 인재.",
        "문화": "역동적. 수평적 소통 지향.",
        "팁": "전동화·SDV 전환 전략을 지원동기에 연결하세요.",
        "준비": "HMAT 인적성 필수."
    },
}

def fetch_jobs(limit=30):
    """원티드 API에서 최신 공고 가져오기"""
    url = f"https://www.wanted.co.kr/api/v4/jobs?country=kr&job_sort=job.latest_order&limit={limit}&offset=0"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read())["data"]
    except Exception as e:
        print(f"API 오류: {e}")
        return []

def get_company_analysis(name):
    for key, val in COMPANY_ANALYSIS.items():
        if key in name:
            return val
    return None

def build_jobs_html(jobs):
    today = date.today().strftime("%Y.%m.%d")
    
    cards = ""
    for i, j in enumerate(jobs):
        company = j.get("company", {}).get("name", "")
        title   = j.get("position", "")
        jid     = j.get("id", "")
        due     = j.get("due_time")
        if due:
            try:
                due_str = datetime.fromisoformat(due[:10]).strftime("%Y.%m.%d 마감")
            except:
                due_str = "날짜 확인"
        else:
            due_str = "상시채용"
        
        url = f"https://www.wanted.co.kr/wd/{jid}"
        analysis = get_company_analysis(company)
        
        analysis_html = ""
        if analysis:
            analysis_html = f'''
        <div class="job-card__analysis">
          <div class="job-card__analysis-title">기업 분석</div>
          <div class="analysis-grid">
            <div class="analysis-item"><div class="analysis-item__label">원하는 인재상</div><div class="analysis-item__text">{analysis["인재상"]}</div></div>
            <div class="analysis-item"><div class="analysis-item__label">조직 문화</div><div class="analysis-item__text">{analysis["문화"]}</div></div>
            <div class="analysis-item"><div class="analysis-item__label">자소서·면접 팁</div><div class="analysis-item__text">{analysis["팁"]}</div></div>
            <div class="analysis-item"><div class="analysis-item__label">전형 준비</div><div class="analysis-item__text">{analysis["준비"]}</div></div>
          </div>
        </div>'''

        cards += f'''
    <div class="job-card" id="job-{i}">
      <div class="job-card__top">
        <div class="job-card__info">
          <div class="job-card__company">{company} · 원티드</div>
          <div class="job-card__title">{title}</div>
          <div class="job-card__meta">
            <span>⏰ {due_str}</span>
          </div>
        </div>
        <span class="job-card__badge badge--open">채용중</span>
      </div>
      <div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-top:12px;">
        {"<button class=\"job-card__expand-btn\" onclick=\"toggleAnalysis(" + str(i) + ")\">▾ 기업 분석 보기</button>" if analysis else ""}
        <a href="{url}" target="_blank" class="btn btn--outline" style="padding:6px 14px;font-size:0.8rem;">공고 보러가기 →</a>
      </div>
      {analysis_html}
    </div>'''
    
    return cards, today

# HTML 파일 읽기 & 업데이트
jobs = fetch_jobs(30)
print(f"공고 {len(jobs)}개 가져옴")

if jobs:
    cards_html, today = build_jobs_html(jobs)
    
    with open("jobs.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    # 기존 카드를 새 카드로 교체
    content = re.sub(
        r'<div class="jobs-grid"[^>]*>.*?</div>\s*(?=<div class="inline-book-cta")',
        f'<div class="jobs-grid" id="jobsGrid">\n{cards_html}\n</div>\n',
        content, flags=re.DOTALL
    )
    
    # 업데이트 날짜 표시
    content = content.replace(
        "공고만 보지 말고",
        f"공고만 보지 말고"
    )
    
    with open("jobs.html", "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"jobs.html 업데이트 완료 ({today})")
else:
    print("공고를 가져오지 못했습니다. 기존 파일 유지.")
