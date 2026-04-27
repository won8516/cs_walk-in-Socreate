from playwright.sync_api import sync_playwright
from Socreate import run_tc01, run_tc02, run_tc03, run_tc04, run_tc05, run_tc06
import sys
sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(storage_state="session.json")
    page = context.new_page()

    page.goto("https://hshopfront.samsung.com/sg/mypage/myproducts/")
    page.wait_for_load_state("networkidle")

    run_tc01(page)
    run_tc02(page)
    run_tc03(page)
    run_tc04(page)
    run_tc05(page)
    run_tc06(page)

    print("모든 테스트 케이스 수행 완료. 5초 후 종료합니다.")
    page.wait_for_timeout(5000)
    browser.close()