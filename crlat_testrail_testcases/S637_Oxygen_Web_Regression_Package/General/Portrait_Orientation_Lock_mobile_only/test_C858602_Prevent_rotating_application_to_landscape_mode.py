import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C858602_Prevent_rotating_application_to_landscape_mode(Common):
    """
    TR_ID: C858602
    NAME: Prevent rotating application to landscape mode
    DESCRIPTION: This test case verifies that Pages of app remain in portrait view after rotating device to Landscape orientation
    DESCRIPTION: ** JIRA tickets:**
    DESCRIPTION: - BMA-18045 Prevent mobile devices from rotating to landscape
    DESCRIPTION: Exception: Landscape mode is prevented on Tablet Nexus 7 (767px ) - BMA-24166
    PRECONDITIONS: Screen rotate option is enabled on a mobile device
    """
    keep_browser_open = True

    def test_001_load_app_device_in_portrait_orientation(self):
        """
        DESCRIPTION: Load app (device in portrait orientation)
        EXPECTED: Home Page is loaded in portrait orientation
        """
        pass

    def test_002_rotate_device_to_landscape(self):
        """
        DESCRIPTION: Rotate device to Landscape
        EXPECTED: Page is displayed with animated mobile icon and text: "Please rotate your screen back in Portrait Mode. Please ensure you have 'screen rotate' option active."
        """
        pass

    def test_003_rotate_device_back_to_portrait(self):
        """
        DESCRIPTION: Rotate device back to Portrait
        EXPECTED: Page remains displayed in its previous state
        """
        pass

    def test_004_navigate_to__all_sports_a_z_sports__sports_page__race_page__event_details_page__lotto_jackpot_page__virtual_sports_page__in_play_page__promotions(self):
        """
        DESCRIPTION: Navigate to:
        DESCRIPTION: - All Sports (A-Z Sports)
        DESCRIPTION: - Sports Page
        DESCRIPTION: - Race Page
        DESCRIPTION: - Event Details Page
        DESCRIPTION: - Lotto/ Jackpot Page
        DESCRIPTION: - Virtual Sports Page
        DESCRIPTION: - In Play Page
        DESCRIPTION: - Promotions
        EXPECTED: Page is loaded in portrait orientation
        """
        pass

    def test_005_repeat_steps_2_3(self):
        """
        DESCRIPTION: Repeat steps #2-3
        EXPECTED: 
        """
        pass

    def test_006_scroll_pages_down__rotate_device_to_landscape__rotate_device_back_to_portrait(self):
        """
        DESCRIPTION: Scroll pages down > Rotate device to Landscape > Rotate device back to Portrait
        EXPECTED: Pages remain displayed in their previous state and keep their position
        """
        pass

    def test_007_navigate_to__log_in__registration_page__forgot_username__forgot_password__players_bets(self):
        """
        DESCRIPTION: Navigate to:
        DESCRIPTION: - Log in
        DESCRIPTION: - Registration Page
        DESCRIPTION: - Forgot Username
        DESCRIPTION: - Forgot Password
        DESCRIPTION: - Players bets
        EXPECTED: Page is loaded in portrait orientation
        """
        pass

    def test_008_repeat_steps_2_3(self):
        """
        DESCRIPTION: Repeat steps #2-3
        EXPECTED: 
        """
        pass

    def test_009_set_cursor_in_any_editable_fields_so_the_custom_mobile_keyboard_is_opened__rotate_device_to_landscape(self):
        """
        DESCRIPTION: Set cursor in any editable fields, so the custom mobile keyboard is opened > Rotate device to Landscape
        EXPECTED: - Keyboard is hidden
        EXPECTED: - Page is displayed with animated mobile icon and text: "Please rotate your screen back in Portrait Mode. Please ensure you have 'screen rotate' option active."
        """
        pass

    def test_010_login(self):
        """
        DESCRIPTION: Login
        EXPECTED: User is logged in
        """
        pass

    def test_011_navigate_to__deposit_page__withdraw_page__my_payments__cash_out__favourites(self):
        """
        DESCRIPTION: Navigate to:
        DESCRIPTION: - Deposit page
        DESCRIPTION: - Withdraw page
        DESCRIPTION: - My Payments
        DESCRIPTION: - Cash Out
        DESCRIPTION: - Favourites
        EXPECTED: Page is loaded in portrait orientation
        """
        pass

    def test_012_repeat_steps_2_3(self):
        """
        DESCRIPTION: Repeat steps #2-3
        EXPECTED: 
        """
        pass

    def test_013_trigger_dialogue_pop_ups_eg__log_in__log_out__limits_after_registration__first_deposit__confirm_deposit_limits__quick_deposit__verify_your_account__info_popup_for_multiples_on_the_betslip__info_popup_on_my_payments(self):
        """
        DESCRIPTION: Trigger dialogue pop-ups e.g.:
        DESCRIPTION: - Log In
        DESCRIPTION: - Log Out
        DESCRIPTION: - Limits (after Registration)
        DESCRIPTION: - First Deposit
        DESCRIPTION: - Confirm Deposit Limits
        DESCRIPTION: - Quick Deposit
        DESCRIPTION: - Verify Your Account
        DESCRIPTION: - Info popup for Multiples on the Betslip
        DESCRIPTION: - Info popup on My Payments
        EXPECTED: Dialogue pop-up is opened and is displayed in portrait orientation
        """
        pass

    def test_014_repeat_steps_2_3(self):
        """
        DESCRIPTION: Repeat steps #2-3
        EXPECTED: 
        """
        pass
