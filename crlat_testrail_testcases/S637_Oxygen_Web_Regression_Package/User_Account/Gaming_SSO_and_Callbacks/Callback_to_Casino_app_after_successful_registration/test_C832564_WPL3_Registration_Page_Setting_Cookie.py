import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.user_account
@vtest
class Test_C832564_WPL3_Registration_Page_Setting_Cookie(Common):
    """
    TR_ID: C832564
    NAME: WPL3 Registration Page Setting Cookie
    DESCRIPTION: The WPL3 registration cookie must continue to be dropped upon successful registration – when a successful registration response back from OpenAPI is received
    DESCRIPTION: *Note: Breakpoints needs to prevent redirect to the mCasino, for checking cookies are set exactly after registration before redirect*
    PRECONDITIONS: User is logged out
    PRECONDITIONS: Clean cash
    """
    keep_browser_open = True

    def test_001_tap_on_casino_tab(self):
        """
        DESCRIPTION: Tap on Casino tab
        EXPECTED: User redirected to Casino side
        """
        pass

    def test_002_tapclick_on_join_us_button(self):
        """
        DESCRIPTION: Tap/click on 'Join us' button
        EXPECTED: User redirected to registration on the Coral side
        """
        pass

    def test_003_fill_all_fields_on_registration_with_valid_data___password_setting_needs_at_least_8_chars_with_upper_and_lowercase_at_least_one_number_and_one_symbol(self):
        """
        DESCRIPTION: Fill all fields on Registration with valid data - password setting needs at least 8 chars with upper and lowercase, at least one number and one symbol
        EXPECTED: All fields are filled
        """
        pass

    def test_004_press_on_ctrlplusshiftplusf_to_search_in_all_sources(self):
        """
        DESCRIPTION: Press on "Ctrl+shift+f" to search in all sources
        EXPECTED: Search tap is opened
        """
        pass

    def test_005_enter_portalwpl3_and_tap_enter(self):
        """
        DESCRIPTION: Enter "portalWPL3" and tap enter
        EXPECTED: The source code is found
        """
        pass

    def test_006_tap_on__to_open_code_in_full_format(self):
        """
        DESCRIPTION: Tap on {} to open code in full format
        EXPECTED: Code is opened
        """
        pass

    def test_007_add_breakpoint_on_the_next_to_settle_cookies_line(self):
        """
        DESCRIPTION: Add breakpoint on the next to settle cookies line
        EXPECTED: The check box is selected in the Breakpoints section
        EXPECTED: ![](index.php?/attachments/get/1303)
        """
        pass

    def test_008_tap_on_continue_button_on_the_registration_process(self):
        """
        DESCRIPTION: Tap on 'Continue' button on the registration process
        EXPECTED: Request for registration is sent
        EXPECTED: Loader on the button is present until response with success are received
        """
        pass

    def test_009_open_application_tab_in_the_developer_console(self):
        """
        DESCRIPTION: Open 'Application' tab in the Developer Console
        EXPECTED: Application storage and cash are shown
        """
        pass

    def test_010_open_cookies_and_tap_on_coral_site_link(self):
        """
        DESCRIPTION: Open 'Cookies' and tap on coral site link
        EXPECTED: Coral cookies are shown
        """
        pass

    def test_011_verify_that_cookie_are_set(self):
        """
        DESCRIPTION: Verify that cookie are set
        EXPECTED: Cookie has been dropped correctly when the following attribute is passed:
        EXPECTED: -  Name: portalWPL3
        EXPECTED: -  Value: true
        """
        pass

    def test_012_verify_that_user_redirected_to_the_gaming_after_successful_registration_and_cookies_are_set__tap_on_play_button_on_breakpoint_to_proceed(self):
        """
        DESCRIPTION: Verify that user redirected to the Gaming after successful registration and cookies are set:
        DESCRIPTION: - Tap on 'Play' button on breakpoint to proceed
        EXPECTED: User redirected to the Gaming
        """
        pass
