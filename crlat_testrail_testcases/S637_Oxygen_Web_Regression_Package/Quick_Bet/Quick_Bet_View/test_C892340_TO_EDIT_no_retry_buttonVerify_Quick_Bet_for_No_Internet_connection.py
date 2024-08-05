import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.quick_bet
@vtest
class Test_C892340_TO_EDIT_no_retry_buttonVerify_Quick_Bet_for_No_Internet_connection(Common):
    """
    TR_ID: C892340
    NAME: TO EDIT (no retry button)Verify Quick Bet for No Internet connection
    DESCRIPTION: This test case verifies quick bet for logged in and logged user with no internet connection
    PRECONDITIONS: Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: User should be logged out
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_add_sport_race_selection_to_quick_bet(self):
        """
        DESCRIPTION: Add <Sport>/ <Race> selection to Quick Bet
        EXPECTED: Quick Bet is displayed at the bottom of the page
        EXPECTED: Added selection and all data are displayed in Quick Bet
        """
        pass

    def test_003_trigger_no_internet_connection_eg_disable_manually_any_internet_connection_to_devicenote_popup_window_should_be_triggered_after_10_seconds_connection_is_gone(self):
        """
        DESCRIPTION: Trigger no internet connection (e.g. disable manually any internet connection to device)
        DESCRIPTION: Note: Popup window should be triggered after 10 seconds connection is gone
        EXPECTED: A popup window should appear showing message "You are currently experiencing issues connecting to the internet.  Please check your internet connection and try again"
        """
        pass

    def test_004_tap_on_x_button(self):
        """
        DESCRIPTION: Tap on 'x' button
        EXPECTED: Observe that popup window is closed
        EXPECTED: After release of BMA-54870 result will be:
        EXPECTED: A popup window should appear showing message "You are currently experiencing issues connecting to the internet.  Please check your internet connection and try again"
        """
        pass

    def test_005_recover_back_internet_connection_and_refresh_page(self):
        """
        DESCRIPTION: Recover back internet connection and refresh page
        EXPECTED: Observe that page is reloaded
        EXPECTED: Quick Bet is displayed at the bottom of the page
        """
        pass

    def test_006_trigger_no_internet_connection_eg_disable_manually_any_internet_connection_to_devicenote_popup_window_should_be_triggered_after_10_seconds_connection_is_gone(self):
        """
        DESCRIPTION: Trigger no internet connection (e.g. disable manually any internet connection to device)
        DESCRIPTION: Note: Popup window should be triggered after 10 seconds connection is gone
        EXPECTED: A popup window should appear showing message "You are currently experiencing issues connecting to the internet.  Please check your internet connection and try again"
        """
        pass

    def test_007_tap_on_retry_button(self):
        """
        DESCRIPTION: Tap on 'Retry' button
        EXPECTED: Observe that page is not reloaded
        """
        pass

    def test_008_recover_back_internet_connection_and_refresh_page(self):
        """
        DESCRIPTION: Recover back internet connection and refresh page
        EXPECTED: Observe that page is reloaded
        EXPECTED: Quick Bet is displayed at the bottom of the page
        """
        pass

    def test_009_trigger_no_internet_connection_eg_disable_manually_any_internet_connection_to_devicenote_popup_window_should_be_triggered_after_10_seconds_connection_is_gone(self):
        """
        DESCRIPTION: Trigger no internet connection (e.g. disable manually any internet connection to device)
        DESCRIPTION: Note: Popup window should be triggered after 10 seconds connection is gone
        EXPECTED: A popup window should appear showing message "You are currently experiencing issues connecting to the internet.  Please check your internet connection and try again"
        """
        pass

    def test_010_recover_back_internet_connection_and_tap_on_retry_button(self):
        """
        DESCRIPTION: Recover back internet connection and tap on 'Retry' button
        EXPECTED: Observe that page is reloaded
        EXPECTED: Quick Bet is displayed at the bottom of the page
        """
        pass

    def test_011_repeat_step_2_10for_logged_in_user(self):
        """
        DESCRIPTION: Repeat Step #2-10
        DESCRIPTION: For logged in user
        EXPECTED: 
        """
        pass

    def test_012_enter_valid_value_on_stake_field(self):
        """
        DESCRIPTION: Enter valid value on 'Stake' field
        EXPECTED: 'PLACE BET' button becomes enabled
        """
        pass

    def test_013_trigger_no_internet_connection_eg_disable_manually_any_internet_connection_to_device(self):
        """
        DESCRIPTION: Trigger no internet connection (e.g. disable manually any internet connection to device)
        EXPECTED: A popup window should appear showing message "You are currently experiencing issues connecting to the internet.  Please check your internet connection and try again"
        """
        pass
