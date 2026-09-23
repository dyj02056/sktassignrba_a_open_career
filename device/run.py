#!/usr/bin/env python3
"""
계속 새로 쓰는 장치 — BR-A

리추얼 기록과 터미널 입력(출석 숫자)을 받아
사이트의 숫자 칸과 능력별 문단 후보를 다시 만든다.

같은 입력이면 같은 결과가 나온다 (AI 호출 없음, 규칙 기반).
"""

import json
import sys
import io
from pathlib import Path

# Windows 터미널 인코딩 강제 (한글 깨짐 방지)
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

from rules import match_candidates


BASE = Path(__file__).parent
INPUT = BASE / "input"
OUTPUT = BASE / "output"
ANSWERS = INPUT / "answers.json"

# 터미널에서 받을 항목
QUESTIONS = [
    ("훈련일", "int", 31),
    ("재적일", "int", 31),
    ("출석", "int", 30),
    ("결석", "int", 0),
    ("지각", "int", 1),
    ("출석률", "str", "96.8%"),
]

def ask(questions):
    """터미널에서 값을 받는다. 엔터만 누르면 기본값."""
    answers = {}
    print("\n=== Attendance numbers (Enter = default) ===\n")
    for label, kind, default in questions:
        raw = input(f"{label} [{default}]: ").strip()
        if raw == "":
            answers[label] = default
        elif kind == "int":
            answers[label] = int(raw)
        else:
            answers[label] = raw
    return answers


def save_answers(answers):
    INPUT.mkdir(exist_ok=True)
    ANSWERS.write_text(
        json.dumps(answers, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"\n입력값을 저장했습니다: {ANSWERS}")


def load_answers():
    if not ANSWERS.exists():
        print(f"[오류] {ANSWERS} 가 없습니다. 먼저 run.py 를 실행하세요.")
        sys.exit(1)
    return json.loads(ANSWERS.read_text(encoding="utf-8"))


def build_numbers(answers, ritual):
    """숫자 칸을 다시 만든다."""
    days = ritual.get("days", [])
    open_count = sum(1 for d in days if d.get("open"))
    close_count = sum(1 for d in days if d.get("close"))

    return {
        "attendance": {
            "훈련일": answers["훈련일"],
            "재적일": answers["재적일"],
            "출석": answers["출석"],
            "결석": answers["결석"],
            "지각": answers["지각"],
            "출석률": answers["출석률"],
            "출처": "내 출석 기록",
        },
        "ritual": {
            "아침": open_count,
            "마무리": close_count,
            "출처": "리추얼 기록",
        },
        "기간": "2026-08-11 ~ 2026-09-23",
    }


def main():
    use_file = "--from-file" in sys.argv

    if use_file:
        answers = load_answers()
        print(f"저장된 입력값을 불러왔습니다: {ANSWERS}")
    else:
        answers = ask(QUESTIONS)
        save_answers(answers)

    # 리추얼 기록 읽기
    ritual_path = INPUT / "ritual.json"
    if not ritual_path.exists():
        print(f"[오류] {ritual_path} 가 없습니다.")
        sys.exit(1)
    ritual = json.loads(ritual_path.read_text(encoding="utf-8"))

    # 이야기 본문 읽기
    story_path = INPUT / "story.md"
    story = story_path.read_text(encoding="utf-8") if story_path.exists() else ""

    # 숫자 생성
    numbers = build_numbers(answers, ritual)

    # 능력별 문단 후보 생성
    candidates = match_candidates(story)

    # 출력
    OUTPUT.mkdir(exist_ok=True)
    (OUTPUT / "numbers.json").write_text(
        json.dumps(numbers, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (OUTPUT / "candidates.json").write_text(
        json.dumps(candidates, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("\n결과를 저장했습니다:")
    print(f"  - {OUTPUT / 'numbers.json'}")
    print(f"  - {OUTPUT / 'candidates.json'}")
    print(
        f"\n숫자: 출석률 {numbers['attendance']['출석률']}, "
        f"리추얼 아침 {numbers['ritual']['아침']}·마무리 {numbers['ritual']['마무리']}"
    )


if __name__ == "__main__":
    main()