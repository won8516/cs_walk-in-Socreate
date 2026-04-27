from playwright.sync_api import sync_playwright #브라우저 자동화 도구
from Socreate import run_tc01, run_tc02, run_tc03, run_tc04 
import sys
sys.stdout.reconfigure(encoding='utf-8')
def main(): #프로그램의 시작점
    # Playwright 실행
    

    with sync_playwright() as p:# playwright 엔진 실행, with -> 끝나면 자동 정리
        browser = p.chromium.launch(headless=False) # 브라우저 실행 , headless=False → 실제 브라우저 창 보이게
        context = browser.new_context()
        page = context.new_page()


        # 메인 페이지 이동
        page.goto("http://hshopfront.samsung.com/sg/")

        # hshopfront 로그인
        page.click('input#username')
        page.fill('input#username', 'qauser')
        page.click('input#password')
        page.fill('input#password', 'qauser1!')
        page.click('button#submit-button')

        page.locator('a[an-la="cookie bar:accept"]').click()
       
        page.wait_for_timeout(2000)#2초 대기
        #쿠키 동의 팝업 클릭 (있을 때만 클릭하도록 수정)
        if page.locator("#truste-consent-button").is_visible(timeout=5000):
            page.click("#truste-consent-button")
            
        else:
            print("쿠키 동의 팝업이 나타나지 않아 건너뜁니다.")

        #human icon 마우스 오버 
        login_btn = page.locator('a.loginBtn:visible, button[an-la="login"]:visible').first
        login_btn.hover()
        page.wait_for_timeout(1000) 
        
        # Sign in 클릭 
        sign_in_link = page.locator('a.loginBtn:visible, a.nv00-gnb-v4__utility-menu--sign-in:visible').last
        sign_in_link.click()
        
        page.wait_for_load_state("networkidle")
    
        # 이메일 입력
        page.fill("#account", "csrevamp_sg3@teml.net")
        page.locator('button[data-log-id="next"]').click()
        page.fill("#password", "csrevamp1!")
        page.locator('button[data-log-id="signin"]').click()
        page.wait_for_timeout(5000) 

         # 첫 번째 팝업 (비밀번호 변경 권고) - Not now 클릭
        not_now_btn_1 = page.locator('button[data-log-id="not-now"]').first
        try:
            not_now_btn_1.wait_for(state="visible", timeout=3000)
            not_now_btn_1.click()
            print("첫 번째 'Not now' 버튼 클릭 완료")
        except Exception:
            print("첫 번째 팝업이 나타나지 않아 건너뜁니다.")

        # 두 번째 팝업 (2단계 인증 권고) - Not now 클릭
        page.wait_for_timeout(1000)  # 팝업 전환 대기
        not_now_btn_2 = page.locator('button[data-log-id="not-now"]').first
        try:
            not_now_btn_2.wait_for(state="visible", timeout=3000)
            not_now_btn_2.click()
            print("두 번째 'Not now' 버튼 클릭 완료")
        except Exception:
            print("두 번째 팝업이 나타나지 않아 건너뜁니다.")
        
        page.wait_for_timeout(3000)#3초 대기

        #My products 페이지로 이동
        page.goto("https://hshopfront.samsung.com/sg/mypage/myproducts/")
        # Privacy policy
        try:
            page.click('button.cta.cta--contained.cta--black.login-leave-btn', timeout=1000)
        except:
            pass

      
         
        # My products 페이지로 이동
        page.goto("https://hshopfront.samsung.com/sg/mypage/myproducts/")
        page.wait_for_load_state("networkidle")

        ##✅ 로그인섹션 저장
        context.storage_state(path="session.json")
        print("✅ 세션 저장 완료")

        # Socreate.py의 함수들을 순서대로 호출
        run_tc01(page)  # 첫 번째 제품 선택
        run_tc02(page)  # Get started 클릭
        run_tc03(page)  # UI/API 정렬 및 레이아웃 검증
        run_tc04(page)  # walk-in 클릭
    

        # 모든 테스트 완료 후 브라우저가 바로 닫히지 않게 5초 대기 
        print("모든 테스트 케이스 수행 완료. 5초 후 종료합니다.")
        page.wait_for_timeout(5000)

        # 브라우저 종료 (main 함수 마지막)
        context.close()
        browser.close()

# 프로그램의 진짜 시작점
if __name__ == "__main__":
    main()