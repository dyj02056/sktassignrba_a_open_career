# 계속 새로 쓰는 장치 — BR-A

리추얼 기록과 출석 숫자를 넣으면, 사이트의 **숫자 칸**과
**능력별 문단 후보**를 다시 만들어 주는 작은 장치입니다.

AI를 부르지 않고 규칙으로만 계산하므로, **같은 입력이면 같은 결과**가 나옵니다.

---

## 디렉토리 구조

```
device/
├── run.py              — 메인 스크립트
├── rules.py            — 능력별 키워드 규칙
├── README.md           — 이 문서
├── input/
│   ├── answers.json    — (자동 생성) 터미널 입력값
│   ├── ritual.json     — 리추얼 기록
│   └── story.md        — 자기소개 본편
└── output/             — (자동 생성)
    ├── numbers.json    — 사이트 숫자 칸
    └── candidates.json — 능력별 문단 후보
```

---

## 돌리는 방법 (3단계)

### 1. 준비

```bash
cd device
```

`input/` 폴더에 두 파일이 있어야 합니다:
- `input/ritual.json` — 리추얼 기록
- `input/story.md` — 자기소개 본편

### 2. 실행

```bash
python run.py
```

터미널에서 출석 숫자를 입력합니다.
**엔터만 누르면 기본값**이 들어갑니다.
입력한 값은 `input/answers.json` 에 저장됩니다.

> **Windows 터미널에서 한글이 깨져 보이면** 실행 전에 `chcp 65001` 을 먼저 실행하세요.
> (결과 파일 `output/*.json` 은 정상입니다.)

### 3. 결과 확인

```bash
cat output/numbers.json
cat output/candidates.json
```

- `output/numbers.json` — 사이트 숫자 칸에 들어갈 값
- `output/candidates.json` — 능력별 문단 후보 (날짜·근거 포함)

---

## 같은 입력, 같은 결과 (재실행)

한 번 입력한 값은 `input/answers.json` 에 저장됩니다.
**같은 결과를 다시 얻으려면** 저장된 값으로 재실행합니다:

```bash
python run.py --from-file
```

이러면 터미널 입력 없이 저장된 값으로 결과를 다시 만듭니다.
**같은 `answers.json` + 같은 `ritual.json` + 같은 `story.md` → 같은 결과.**

---

## 출력 예시

### numbers.json

```json
{
  "attendance": {
    "훈련일": 31,
    "재적일": 31,
    "출석": 30,
    "결석": 0,
    "지각": 1,
    "출석률": "96.8%",
    "출처": "내 출석 기록"
  },
  "ritual": {
    "아침": 31,
    "마무리": 30,
    "출처": "리추얼 기록"
  },
  "기간": "2026-08-11 ~ 2026-09-23"
}
```

### candidates.json

```json
{
  "자기조절력": [
    {
      "date": "2024-01",
      "matched": ["취업", "폴더"],
      "text": "2024년 1월, \"취업\"이라는 폴더를 만들고 ..."
    }
  ],
  "대인관계력": [ ... ],
  "자기동기력": [ ... ]
}
```

---

## 승인 규칙

장치가 만든 후보는 **자동으로 사이트에 들어가지 않습니다.**
`candidates.json` 을 사람이 읽고, **승인한 문단만** 사이트에 옮깁니다.

---

## 요구사항

- Python 3.8 이상
- 외부 라이브러리 없음 (표준 라이브러리만 사용)