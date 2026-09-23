"""
능력별 키워드 규칙 — BR-A

이야기 본문에서 자기조절력·대인관계력·자기동기력에 해당하는
문단을 찾아 날짜·근거와 함께 후보로 뽑는다.
"""

import re

# 세 능력과 각각의 키워드
ABILITIES = {
    "자기조절력": [
        "취업", "폴더", "필기", "실기", "정보처리기사",
        "차곡차곡", "쌓", "K-Digital", "6개월",
    ],
    "대인관계력": [
        "조장", "자처", "경청", "들어주", "말을", "의사소통",
        "조원", "먼저",
    ],
    "자기동기력": [
        "먼저", "자처", "새로운 시도", "행동", "옮기",
    ],
}


def find_date(paragraph: str) -> str:
    """문단에서 날짜를 찾는다 (YYYY년 M월, YYYY-MM-DD 등)."""
    # 예: 2023년 2월, 2024년 1월
    m = re.search(r"(\d{4})년\s*(\d{1,2})월", paragraph)
    if m:
        return f"{m.group(1)}-{int(m.group(2)):02d}"
    # 예: 2026-08-11
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", paragraph)
    if m:
        return m.group(0)
    return ""


def match_candidates(story: str) -> dict:
    """
    이야기 본문을 문단 단위로 나누고,
    각 능력의 키워드가 있는 문단을 후보로 뽑는다.

    각 후보에는 날짜와 근거(매칭된 키워드)가 붙는다.
    """
    if not story.strip():
        return {ability: [] for ability in ABILITIES}

    # 빈 줄 기준으로 문단 분리
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", story) if p.strip()]

    result = {ability: [] for ability in ABILITIES}

    for p in paragraphs:
        date = find_date(p)
        for ability, keywords in ABILITIES.items():
            matched = [k for k in keywords if k in p]
            if matched:
                result[ability].append({
                    "date": date,
                    "matched": matched,
                    "text": p,
                })

    return result