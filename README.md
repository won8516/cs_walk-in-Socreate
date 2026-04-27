# Samsung CS Revamp - UI 자동화 테스트 가이드

## 📁 파일 구조

```
Socreate/
├── save_session.py   # 로그인 및 세션 저장
├── Socreate.py       # TC 함수 정의
├── tc_run.py         # TC 실행
├── dummy_test.jpg    # 파일 업로드용 더미 이미지 (자동 생성)
└── screenshots/      # 스크린샷 저장 폴더 (자동 생성)
```

---

## 🚀 실행 순서

### 1단계 - 세션 저장 (최초 1회 또는 세션 만료 시)

```bash
python save_session.py
```

1. 브라우저가 자동으로 열리고 hshopfront 1차 로그인이 자동으로 진행됩니다
2. 삼성 계정 로그인 화면이 나타나면 **직접 수동으로 로그인**해주세요
3. 로그인 완료 후 **My Products 페이지로 이동**하면 자동으로 `session.json`이 저장됩니다
4. 터미널에 `✅ 세션 저장 완료` 메시지가 나오면 완료

> ⚠️ 세션은 일정 시간이 지나면 만료됩니다. 403 에러 발생 시 1단계부터 다시 실행하세요.

---

### 2단계 - TC 실행

```bash
python tc_run.py
```

- `session.json`을 불러와 로그인 없이 자동으로 TC를 순서대로 실행합니다
- 실행 결과는 터미널에 출력되며, 스크린샷은 `screenshots/` 폴더에 저장됩니다

---

## 🌏 국가별 실행 방법

국가마다 로그인 계정과 URL이 다르므로 아래 절차를 따릅니다.

### 1. 국가별 세션 저장

`save_session.py` 에서 URL을 국가에 맞게 변경 후 실행합니다.

```python
# 싱가포르
page.goto("http://hshopfront.samsung.com/sg/")

# 호주로 변경 시
page.goto("http://hshopfront.samsung.com/au/")
```

세션 저장 경로도 국가별로 분리합니다.

```python
context.storage_state(path="session_sg.json")  # 싱가포르
context.storage_state(path="session_au.json")  # 호주
```

### 2. 국가별 TC 실행

`tc_run.py` 에서 COUNTRIES 딕셔너리에 국가를 추가하면 순서대로 자동 실행됩니다.

```python
COUNTRIES = {
    "sg": "https://hshopfront.samsung.com/sg/mypage/myproducts/",
    "au": "https://hshopfront.samsung.com/au/mypage/myproducts/",
    "uk": "https://hshopfront.samsung.com/uk/mypage/myproducts/",
}

with sync_playwright() as p:
    for country, url in COUNTRIES.items():
        print(f"\n========== {country.upper()} 테스트 시작 ==========")
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state=f"session_{country}.json")
        page = context.new_page()

        page.goto(url)
        page.wait_for_load_state("networkidle")

        run_tc01(page)
        run_tc02(page)
        run_tc03(page)
        run_tc04(page)
        run_tc05(page)
        run_tc06(page)

        print(f"========== {country.upper()} 테스트 완료 ==========")
        browser.close()
```

---

## 📋 TC 목록

| TC | 설명 | 스크린샷 |
|---|---|---|
| TC01 | My Products - Get support 버튼 클릭 | `TC01_Product_Selected.png` |
| TC02 | Get Support - Request a repair Get started 클릭 | `TC02_Get_Started_Result.png` |
| TC03 | Fix it yourself - Physical Damage 클릭 | `TC03_Physical_Damage_Selected.png` |
| TC04 | Select support option - Walk-in Select 클릭 | `TC04_Walk_In_Selected.png` |
| TC05 | Walk-in 페이지 UI 검증 | `TC05_1~4_*.png` |
| TC06 | Walk-in 서비스 신청 플로우 | `TC06_1~5_*.png` |

### TC06 상세

| 단계 | 설명 | 스크린샷 |
|---|---|---|
| 6-1 | 워런티 상태 확인 후 분기 처리 (Valid 스킵 / Expired 날짜+파일 입력+Submit) | `TC06_1_Warranty_Submit.png` |
| 6-2 | 첫 번째 서비스센터 Select 클릭 | `TC06_2_Service_Center_Selected.png` |
| 6-3 | Select date 필드 노출 및 캘린더 확인 | `TC06_3_Calendar_Opened.png` |
| 6-4 | 오늘+3일 날짜 선택 및 가용 시간 선택 | `TC06_4_Date_Time_Selected.png` |
| 6-5 | 증상 텍스트 입력 | `TC06_5_Symptoms_Filled.png` |

---

## ➕ 새로운 TC 추가 방법

### 1. `Socreate.py` 에 함수 추가

```python
def run_tc07(page):
    print("TC07 시작: ...")

    target_btn = page.locator('...')  # DevTools에서 확인한 로케이터

    try:
        target_btn.wait_for(state="visible", timeout=15000)
        target_btn.scroll_into_view_if_needed()
        target_btn.dispatch_event("click")
        print("✅ 클릭 완료")
    except Exception as e:
        print(f"⚠️ 1차 실패: {e}")
        try:
            page.get_by_role("button", name="...").click(force=True)
            print("✅ 클릭 완료 (Role/Name 방식)")
        except Exception:
            print("❌ 모든 클릭 시도 실패")

    page.wait_for_timeout(1000)
    take_screenshot(page, "TC07_Result.png")
    page.wait_for_load_state("networkidle")
```

### 2. `tc_run.py` import 및 호출 추가

```python
# import 추가
from Socreate import run_tc01, ..., run_tc07

# 실행 추가
run_tc07(page)
```

---

## 🔍 로케이터 찾는 방법 (DevTools)

1. Chrome에서 **F12** → Elements 탭 열기
2. 확인할 버튼/요소 위에서 **우클릭 → 검사**
3. HTML에서 아래 속성 우선순위로 로케이터 선택

```
1순위: id 속성         예) #receipt-file-upload
2순위: data-* 속성     예) data-symptom-code="physical-damage"
3순위: an-la 속성      예) an-la="get support:get started"
4순위: class 속성      예) .get-support__request
5순위: role/aria       예) get_by_role("button", name="...")
```

---

## ⚠️ 주의사항

- **i18n 환경** — 텍스트 내용이 아닌 요소의 존재 여부(`is_visible()`)로 검증합니다
- **세션 만료** — 403 에러 발생 시 `save_session.py`를 다시 실행해 세션을 갱신하세요
- **스크린샷 타이밍** — 클릭 후 `wait_for_timeout(1000)` → `take_screenshot` → `wait_for_load_state` 순서를 지킵니다
- **워런티 분기** — TC06 6-1은 워런티 Valid/Expired 상태에 따라 자동으로 분기 처리됩니다
- **더미 이미지** — TC06 실행 시 `dummy_test.jpg`가 없으면 자동으로 생성됩니다
- **신규 TC 로케이터** — 텍스트 기반 로케이터 대신 반드시 DevTools에서 확인한 속성 기반 로케이터를 사용하세요
- **커스텀 드롭다운** — `select` 태그가 아닌 커스텀 UI 드롭다운은 버튼 클릭 후 팝업 옵션을 선택해야 합니다
