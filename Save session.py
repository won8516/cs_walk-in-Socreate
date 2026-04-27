from playwright.sync_api import sync_playwright
import sys
sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # 1차 hshopfront 로그인 (자동)
    page.goto("http://hshopfront.samsung.com/sg/")
    page.click('input#username')
    page.fill('input#username', 'qauser')
    page.click('input#password')
    page.fill('input#password', 'qauser1!')
    page.click('button#submit-button')
    page.wait_for_load_state("networkidle")
    print("✅ 1차 hshopfront 로그인 완료")

    # 2차 삼성 계정 로그인 (수동)
    print("⏳ 브라우저에서 삼성 계정으로 직접 로그인 해주세요.")
    print("⏳ 로그인 완료 후 My Products 페이지로 이동해주세요.")

    # My Products 페이지 감지될 때까지 대기 (최대 120초)
    page.wait_for_url("**/mypage/myproducts/**", timeout=120000)
    print("✅ My Products 페이지 감지 완료")

    context.storage_state(path="session.json")
    print("✅ 세션 저장 완료 - 이제 tc_run.py 를 실행하세요")
    browser.close()