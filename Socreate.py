import os
from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta

# 국가별 설정
COUNTRY_CONFIG = {
    "sg": {"phone": "91234567"},    # 싱가포르 8자리
}


# 스크린샷 전용 함수
def take_screenshot(page, fileName):
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")
    path = f"screenshots/{fileName}"
    page.screenshot(path=path)
    print(f"📸 스크린샷 저장 완료: {path}")


def run_tc01(page):
    print("TC01 시작: 첫 번째 모바일 제품의 Support 버튼 클릭")

    # data-modelcategory="Phone" 인 첫 번째 제품의 Get support 버튼 클릭
    mobile_item = page.locator('[data-modelcategory="Phone"]').first
    mobile_item.wait_for(state="visible", timeout=5000)

    target_btn = mobile_item.locator('a[data-type="getSupport"]')

    try:
        target_btn.scroll_into_view_if_needed()
        target_btn.click()
        print("✅ 모바일 제품 선택 완료 (Get support 클릭 성공)")
    except Exception:
        print("⚠️ 일반 클릭 실패로 강제 클릭을 시도합니다.")
        target_btn.click(force=True)

    page.wait_for_timeout(1000)
    take_screenshot(page, "TC01_Product_Selected.png")
    page.wait_for_load_state("networkidle")


def run_tc02(page):
    print("TC02 시작: Request a repair 섹션의 Get started 버튼 클릭")

    repair_section = page.locator('.get-support__request')
    target_btn = repair_section.locator('button[an-la*="get started"]')

    try:
        target_btn.wait_for(state="visible", timeout=15000)
        target_btn.scroll_into_view_if_needed()

        print(f"🎯 매칭된 버튼 텍스트: {target_btn.inner_text()}")
        target_btn.dispatch_event("click")
        print("✅ Get started 클릭 완료 (Dispatch Event)")

    except Exception as e:
        print(f"⚠️ 1차 클릭 실패, 텍스트 직접 매칭 시도: {e}")
        try:
            page.get_by_role("button", name="Get started. Fix it yourself").click(force=True)
            print("✅ Get started 클릭 완료 (Role/Name 방식)")
        except Exception:
            print("❌ 모든 클릭 시도 실패. 버튼이 다른 레이어에 가려져 있는지 확인 필요")

    page.wait_for_timeout(1000)
    take_screenshot(page, "TC02_Get_Started_Result.png")
    page.wait_for_load_state("networkidle")


def run_tc03(page):
    print("TC03 시작: Fix it yourself - Physical Damage 클릭")

    target_btn = page.locator('button[data-symptom-code="physical-damage"]')

    try:
        target_btn.wait_for(state="visible", timeout=15000)
        target_btn.scroll_into_view_if_needed()

        print(f"🎯 매칭된 버튼 텍스트: {target_btn.inner_text()}")
        target_btn.dispatch_event("click")
        print("✅ Physical Damage 클릭 완료 (Dispatch Event)")

    except Exception as e:
        print(f"⚠️ 1차 클릭 실패, 텍스트 직접 매칭 시도: {e}")
        try:
            page.get_by_role("button", name="Physical Damage").click(force=True)
            print("✅ Physical Damage 클릭 완료 (Role/Name 방식)")
        except Exception:
            print("❌ 모든 클릭 시도 실패. 버튼이 다른 레이어에 가려져 있는지 확인 필요")

    page.wait_for_timeout(1000)
    take_screenshot(page, "TC03_Physical_Damage_Selected.png")
    page.wait_for_load_state("networkidle")


def run_tc04(page):
    print("TC04 시작: Select support option - Walk-in Select 클릭")

    target_btn = page.locator('a[an-la*="walk-in:select"]')

    try:
        target_btn.wait_for(state="visible", timeout=15000)
        target_btn.scroll_into_view_if_needed()

        print(f"🎯 매칭된 버튼 텍스트: {target_btn.inner_text()}")
        target_btn.dispatch_event("click")
        print("✅ Walk-in Select 클릭 완료 (Dispatch Event)")

    except Exception as e:
        print(f"⚠️ 1차 클릭 실패, Role/Name 방식 시도: {e}")
        try:
            page.get_by_role("link", name="Select. Walk-in").click(force=True)
            print("✅ Walk-in Select 클릭 완료 (Role/Name 방식)")
        except Exception:
            print("❌ 모든 클릭 시도 실패. 버튼 상태 확인 필요")

    page.wait_for_timeout(1000)
    take_screenshot(page, "TC04_Walk_In_Selected.png")
    page.wait_for_load_state("networkidle")


def run_tc05(page):
    print("TC05 시작: Walk-in 페이지 UI 검증")

    # 1. 디바이스 정보 검증
    print("\n[1] 디바이스 정보 검증")
    try:
        device_section = page.locator('.walk-in__device')
        device_section.wait_for(state="visible", timeout=10000)
        assert device_section.is_visible(), "디바이스 정보 섹션 없음"
        print("✅ 디바이스 정보 섹션 노출 확인")

        warranty = page.locator('.walk-in__device').locator('[class*="warranty"], [id*="warranty"]').first
        warranty.wait_for(state="visible", timeout=5000)
        assert warranty.is_visible(), "워런티 정보 영역 없음"
        print("✅ 워런티 정보 영역 노출 확인")

        toggle_btn = page.locator('.walk-in__device button.warranty-info-btn').first
        toggle_btn.wait_for(state="visible", timeout=5000)
        is_expanded = toggle_btn.get_attribute("aria-expanded")
        if is_expanded == "false":
            toggle_btn.click()
            page.wait_for_timeout(1000)
            print("✅ 워런티 토글 클릭 완료")
        else:
            print("✅ 워런티 이미 열려있음 - 클릭 스킵")

    except Exception as e:
        print(f"❌ 디바이스 정보 검증 실패: {e}")

    device_section = page.locator('.walk-in__device')
    device_section.scroll_into_view_if_needed()
    page.wait_for_timeout(500)
    take_screenshot(page, "TC05_1_Device_Info.png")

    # 2. Book an appointment - 지도 및 서비스센터 목록 검증
    print("\n[2] Book an appointment 섹션 검증")
    try:
        appointment_section = page.locator('.walk-in__appointment')
        appointment_section.wait_for(state="visible", timeout=10000)
        appointment_section.scroll_into_view_if_needed()
        page.wait_for_timeout(1000)
        assert appointment_section.is_visible(), "Book an appointment 섹션 없음"
        print("✅ Book an appointment 섹션 노출 확인")

        map_area = page.locator('iframe, .gm-style, #map').first
        map_area.wait_for(state="visible", timeout=10000)
        assert map_area.is_visible(), "지도 없음"
        print("✅ 지도 로드 확인")

        service_list = page.locator('.walk-in__appointment').locator('ul, ol, [class*="list"], [class*="result"]').first
        service_list.wait_for(state="visible", timeout=5000)
        assert service_list.is_visible(), "서비스센터 목록 없음"
        print("✅ 서비스센터 목록 노출 확인")

    except Exception as e:
        print(f"❌ Book an appointment 검증 실패: {e}")

    appointment_section = page.locator('.walk-in__appointment')
    appointment_section.scroll_into_view_if_needed()
    page.wait_for_timeout(500)
    take_screenshot(page, "TC05_2_Appointment.png")

    # 3. Contact information 자동입력 검증
    print("\n[3] Contact information 검증")
    try:
        contact_section = page.locator('.walk-in__contact')
        contact_section.wait_for(state="visible", timeout=10000)
        contact_section.scroll_into_view_if_needed()
        page.wait_for_timeout(500)
        assert contact_section.is_visible(), "Contact information 섹션 없음"
        print("✅ Contact information 섹션 노출 확인")

        first_name = page.locator('.myd29-contact-firstname input').first
        assert first_name.input_value() != "", "First Name 자동입력 안됨"
        print("✅ First Name 자동입력 확인")

        last_name = page.locator('.myd29-contact-lastname input').first
        assert last_name.input_value() != "", "Last Name 자동입력 안됨"
        print("✅ Last Name 자동입력 확인")

        email = page.locator('.myd29-contact-email input').first
        assert email.input_value() != "", "Email 자동입력 안됨"
        print("✅ Email 자동입력 확인")

        mobile_label = page.locator('.myd29-contact-number label').first
        mobile_label.wait_for(state="visible", timeout=5000)
        assert mobile_label.is_visible(), "Mobile 힌트 요소 없음"
        print("✅ Mobile 힌트 텍스트 요소 노출 확인")

    except Exception as e:
        print(f"❌ Contact information 검증 실패: {e}")

    contact_section = page.locator('.walk-in__contact')
    contact_section.scroll_into_view_if_needed()
    page.wait_for_timeout(500)
    take_screenshot(page, "TC05_3_Contact_Info.png")

    # 4. What problem 텍스트 입력칸 힌트 검증
    print("\n[4] What problem 섹션 검증")
    try:
        symptoms_section = page.locator('.walk-in__symptoms')
        symptoms_section.wait_for(state="visible", timeout=10000)
        symptoms_section.scroll_into_view_if_needed()
        page.wait_for_timeout(500)
        assert symptoms_section.is_visible(), "What problem 섹션 없음"
        print("✅ What problem 섹션 노출 확인")

        textarea = page.locator('.walk-in__symptoms textarea').first
        textarea.wait_for(state="visible", timeout=5000)
        assert textarea.is_visible(), "텍스트 입력칸 없음"
        print("✅ 텍스트 입력칸 노출 확인")

        textarea_label = page.locator('.walk-in__symptoms label.text-field-v2__hint').first
        textarea_label.wait_for(state="visible", timeout=5000)
        assert textarea_label.is_visible(), "텍스트 입력칸 힌트 요소 없음"
        print("✅ 텍스트 입력칸 힌트 요소 노출 확인")

    except Exception as e:
        print(f"❌ What problem 섹션 검증 실패: {e}")

    symptoms_section = page.locator('.walk-in__symptoms')
    symptoms_section.scroll_into_view_if_needed()
    page.wait_for_timeout(500)
    take_screenshot(page, "TC05_4_Symptoms.png")
    page.wait_for_load_state("networkidle")
    print("\n✅ TC05 완료: Walk-in 페이지 UI 검증 종료")


def run_tc06(page, country="sg"):
    print(f"TC06 시작: Walk-in 서비스 신청 플로우 (국가: {country.upper()})")

    # 국가별 전화번호 설정
    phone = COUNTRY_CONFIG.get(country, {}).get("phone", "")

    # 쿠키 팝업 처리 (있을 때만)
    try:
        cookie_btn = page.locator('button:has-text("Accept")').first
        cookie_btn.wait_for(state="visible", timeout=3000)
        cookie_btn.click()
        page.wait_for_timeout(500)
        print("✅ 쿠키 팝업 Accept 완료")
    except Exception:
        print("쿠키 팝업 없음, 건너뜁니다.")

    # 6-1. 워런티 열고 날짜/파일 입력 후 Submit
    print("\n[6-1] 워런티 정보 입력 및 Submit")
    try:
        warranty_section = page.locator('.walk-in__device')
        warranty_section.wait_for(state="visible", timeout=10000)
        warranty_section.scroll_into_view_if_needed()

        is_expired = warranty_section.locator('.expired').count() > 0

        if is_expired:
            print("⚠️ 워런티 만료 상태 - 날짜/파일 입력 진행")

            # 워런티 토글 - 폼이 안 보일 때만 클릭
            toggle_btn = warranty_section.locator('button.warranty-info-btn').first
            toggle_btn.wait_for(state="visible", timeout=5000)

            # aria-expanded 대신 실제 폼 영역 노출 여부로 확인
            warranty_info = page.locator('.walk-in__device__warranty-info')
            if not warranty_info.is_visible():
                toggle_btn.click()
                page.wait_for_timeout(1000)
                print("✅ 워런티 토글 클릭 완료")
            else:
                print("✅ 워런티 이미 열려있음 - 클릭 스킵")
            today = datetime.now()

            day_input = page.locator('.myd29-purchased-day .text-field-v2__input-wrap input').first
            day_input.wait_for(state="visible", timeout=5000)
            day_input.fill(str(today.day))
            print(f"✅ Day 입력: {today.day}")

            month_btn = page.locator('.myd29-purchased-month button.select-text-field__select').first
            month_btn.wait_for(state="visible", timeout=5000)
            month_btn.click()
            page.wait_for_timeout(500)

            month_value = str(today.month).zfill(2)
            month_option = page.locator(
                f'.myd29-purchased-month .select-popup__option[data-month="{month_value}"]'
            ).first
            month_option.wait_for(state="visible", timeout=5000)
            month_option.click()
            page.wait_for_timeout(500)
            print(f"✅ Month 입력: {month_value}")

            year_input = page.locator('.myd29-purchased-year .text-field-v2__input-wrap input').first
            year_input.wait_for(state="visible", timeout=5000)
            year_input.fill(str(today.year))
            print(f"✅ Year 입력: {today.year}")

            dummy_img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dummy_test.jpg")
            if not os.path.exists(dummy_img_path):
                with open(dummy_img_path, "wb") as f:
                    f.write(bytes([
                        0xFF, 0xD8, 0xFF, 0xE0, 0x00, 0x10, 0x4A, 0x46,
                        0x49, 0x46, 0x00, 0x01, 0x01, 0x00, 0x00, 0x01,
                        0x00, 0x01, 0x00, 0x00, 0xFF, 0xDB, 0x00, 0x43,
                        0x00, 0x08, 0x06, 0x06, 0x07, 0x06, 0x05, 0x08,
                        0xFF, 0xD9
                    ]))

            file_input = page.locator('#receipt-file-upload')
            file_input.set_input_files(dummy_img_path)
            page.wait_for_timeout(1000)
            print("✅ 파일 업로드 완료")

            submit_btn = page.locator('.walk-in__device button:has-text("Submit")').first
            submit_btn.wait_for(state="visible", timeout=5000)
            submit_btn.scroll_into_view_if_needed()
            submit_btn.dispatch_event("click")
            page.wait_for_timeout(1500)
            print("✅ Submit 클릭 완료")

        else:
            print("✅ 워런티 유효 상태 - 날짜/파일 입력 스킵")

    except Exception as e:
        print(f"❌ 6-1 실패: {e}")

    warranty_section = page.locator('.walk-in__device')
    warranty_section.scroll_into_view_if_needed()
    page.wait_for_timeout(500)
    take_screenshot(page, "TC06_1_Warranty_Submit.png")

    # 6-2. Book an appointment - 첫 번째 장소 Select 클릭
    print("\n[6-2] 첫 번째 서비스센터 Select 클릭")
    try:
        appointment_section = page.locator('.walk-in__appointment')
        appointment_section.wait_for(state="visible", timeout=10000)
        appointment_section.scroll_into_view_if_needed()
        page.wait_for_timeout(500)

        first_result = page.locator('[data-asc-index="0"]').first
        first_result.wait_for(state="visible", timeout=10000)
        first_result.dispatch_event("click")
        page.wait_for_timeout(1000)
        print("✅ 첫 번째 서비스센터 클릭 완료")

        select_btn = page.locator('.gm-style [role="dialog"] a, .gm-style-iw a').first
        select_btn.wait_for(state="visible", timeout=5000)
        select_btn.dispatch_event("click")
        page.wait_for_timeout(1000)
        print("✅ Select 클릭 완료")

    except Exception as e:
        print(f"❌ 6-2 실패: {e}")

    appointment_section = page.locator('.walk-in__appointment')
    appointment_section.scroll_into_view_if_needed()
    page.wait_for_timeout(500)
    take_screenshot(page, "TC06_2_Service_Center_Selected.png")

    # 6-3. Select date 필드 노출 확인 및 캘린더 클릭
    print("\n[6-3] Select date 필드 노출 및 캘린더 확인")
    try:
        date_input = page.locator('#appointment-date-input')
        date_input.wait_for(state="visible", timeout=10000)
        date_input.scroll_into_view_if_needed()
        page.wait_for_timeout(500)
        assert date_input.is_visible(), "Select date 필드 없음"
        print("✅ Select date 필드 노출 확인")

        date_input.click()
        page.wait_for_timeout(1000)

        calendar = page.locator('.flatpickr-calendar')
        calendar.wait_for(state="visible", timeout=5000)
        assert calendar.is_visible(), "캘린더 노출 안됨"
        print("✅ 캘린더 노출 확인")

    except Exception as e:
        print(f"❌ 6-3 실패: {e}")

    date_input = page.locator('#appointment-date-input')
    date_input.scroll_into_view_if_needed()
    page.wait_for_timeout(500)
    take_screenshot(page, "TC06_3_Calendar_Opened.png")
    
    # 6-4. 예약 가능한 첫 번째 날짜 선택 후 시간 선택
    print("\n[6-4] 예약 가능한 첫 번째 날짜 선택 및 시간 선택")
    try:
        # 예약 가능한 첫 번째 날짜 자동 선택
        available_day = page.locator(
            '.flatpickr-day:not(.flatpickr-disabled):not(.prevMonthDay):not(.nextMonthDay)'
        ).first
        available_day.wait_for(state="visible", timeout=5000)
        available_day.click()
        page.wait_for_timeout(2000)
        print("✅ 예약 가능한 첫 번째 날짜 선택 완료")

        time_picker = page.locator('.walk-in__appointment__select-form-item').nth(1)
        time_picker.wait_for(state="visible", timeout=5000)
        time_picker.scroll_into_view_if_needed()
        page.wait_for_timeout(2000)
        time_picker.click()
        page.wait_for_timeout(1000)
        print("✅ Select time 클릭 완료")

        time_option = page.locator(
            '.myd29-appointment-time-select button.select-popup__option:not([disabled])'
        ).first
        time_option.wait_for(state="visible", timeout=10000)
        time_option.click()
        page.wait_for_timeout(1000)
        print("✅ 시간 선택 완료")

    except Exception as e:
        print(f"❌ 6-4 실패: {e}")

    page.wait_for_timeout(500)
    take_screenshot(page, "TC06_4_Date_Time_Selected.png")

    # 6-5. Contact information - 전화번호 입력
    print("\n[6-5] 전화번호 입력 및 증상 텍스트 입력")
    try:
        contact_section = page.locator('.walk-in__contact')
        contact_section.scroll_into_view_if_needed()
        page.wait_for_timeout(500)

        mobile_input = page.locator('.myd29-contact-number input').first
        mobile_input.wait_for(state="visible", timeout=5000)
        mobile_input.fill(phone)
        page.wait_for_timeout(500)
        print(f"✅ 전화번호 입력 완료: {phone}")

    except Exception as e:
        print(f"❌ 전화번호 입력 실패: {e}")

    # 전화번호 입력 후 contact 섹션 스크린샷
    contact_section = page.locator('.walk-in__contact')
    contact_section.scroll_into_view_if_needed()
    page.wait_for_timeout(500)
    take_screenshot(page, "TC06_5_Contact_Filled.png")

    try:
        # 증상 텍스트 입력
        symptoms_section = page.locator('.walk-in__symptoms')
        symptoms_section.wait_for(state="visible", timeout=10000)
        symptoms_section.scroll_into_view_if_needed()
        page.wait_for_timeout(500)

        textarea = page.locator('.walk-in__symptoms textarea').first
        textarea.wait_for(state="visible", timeout=5000)
        textarea.click()
        textarea.fill("This is a test ticket, please do not cancel it.")
        page.wait_for_timeout(500)
        print("✅ 증상 텍스트 입력 완료")

    except Exception as e:
        print(f"❌ 증상 입력 실패: {e}")

    # 증상 입력 후 symptoms 섹션 스크린샷
    symptoms_section = page.locator('.walk-in__symptoms')
    symptoms_section.scroll_into_view_if_needed()
    page.wait_for_timeout(500)
    take_screenshot(page, "TC06_6_Symptoms_Filled.png")
    page.wait_for_load_state("networkidle")
    print("\n✅ TC06 완료: Walk-in 서비스 신청 플로우 종료")