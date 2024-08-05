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
class Test_C58669272_Verify_QuickBet_Bet_Placement_immediately_after_connection_reestablishment(Common):
    """
    TR_ID: C58669272
    NAME: Verify QuickBet Bet Placement immediately after connection reestablishment
    DESCRIPTION: This test case verifies the QuickBet behaviour when user tries to place a bet immediately after connection reestablishment
    PRECONDITIONS: **Pre-conditions:**
    PRECONDITIONS: 1. QuickBet should be enabled in CMS > System Configuration > quickBet
    PRECONDITIONS: 2. Event with Banach markets should be available in the app
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Log in with user with positive balance and QuickBet enabled in user settings
    PRECONDITIONS: 2. Tap on any selection of any event
    PRECONDITIONS: 3. Enter any value into 'stake' field
    """
    keep_browser_open = True

    def test_001_for_mobileturn_wifi_off_and_on_and_immediately_tap_place_bet_buttonin_emulator_mode_in_chrome__devtools__network__offlineonline_mode_could_be_also_used(self):
        """
        DESCRIPTION: **For mobile:**
        DESCRIPTION: Turn wifi off and on and immediately tap 'Place bet' button
        DESCRIPTION: (in emulator mode in Chrome > Devtools > Network > Offline/Online mode could be also used)
        EXPECTED: * QuickBet gets reloaded preserving value in 'stake' field
        EXPECTED: * Bet is NOT placed
        EXPECTED: * Balance remains unchanged
        """
        pass

    def test_002_for_mobiletap_place_bet_button_again(self):
        """
        DESCRIPTION: **For mobile:**
        DESCRIPTION: Tap 'Place bet' button again
        EXPECTED: * Bet is placed
        EXPECTED: * Bet receipt is displayed with correct data
        """
        pass

    def test_003_for_mobileclose_bet_receipt_and_navigate_to_my_bets__open_bets(self):
        """
        DESCRIPTION: **For mobile:**
        DESCRIPTION: Close bet receipt and navigate to 'My bets' > 'Open bets'
        EXPECTED: * Bet from step 1 is NOT shown on 'My bets' > 'Open bets'
        EXPECTED: * Bet from step 2 is shown
        """
        pass

    def test_004_for_mobile_and_desktopnavigate_to_event_details_page_that_has_banach_markets__bet_builderbyb_tab(self):
        """
        DESCRIPTION: **For mobile and desktop:**
        DESCRIPTION: Navigate to event details page that has Banach markets > 'Bet builder'/'BYB' tab
        EXPECTED: 
        """
        pass

    def test_005_for_mobile_and_desktop_add_any_two_selections_to_dashboard_tapclick_on_place_bet_button(self):
        """
        DESCRIPTION: **For mobile and desktop:**
        DESCRIPTION: * Add any two selections to dashboard
        DESCRIPTION: * Tap/click on 'Place bet' button
        EXPECTED: QuickBet is opened
        """
        pass

    def test_006_for_mobile_and_desktop_enter_any_value_into_stake_field_turn_wifi_off_and_on_and_immediately_tap_place_bet_buttonin_emulator_mode_in_chrome__devtools__network__offlineonline_mode_could_be_also_used(self):
        """
        DESCRIPTION: **For mobile and desktop:**
        DESCRIPTION: * Enter any value into 'stake' field
        DESCRIPTION: * Turn wifi off and on and immediately tap 'Place bet' button
        DESCRIPTION: (in emulator mode in Chrome > Devtools > Network > Offline/Online mode could be also used)
        EXPECTED: * Bet is NOT placed
        EXPECTED: * Balance remains unchanged
        EXPECTED: * QuickBet gets reloaded and dashboard is shown
        """
        pass

    def test_007_for_mobile_and_desktoptap_place_bet_button_on_the_dashboard(self):
        """
        DESCRIPTION: **For mobile and desktop:**
        DESCRIPTION: Tap 'Place bet' button on the dashboard
        EXPECTED: QuickBet is opened
        """
        pass

    def test_008_for_mobile_and_desktopenter_any_value_into_stake_field_and_tapclick_on_place_bet_button(self):
        """
        DESCRIPTION: **For mobile and desktop:**
        DESCRIPTION: Enter any value into 'stake' field and tap/click on 'Place bet' button
        EXPECTED: * Bet is placed
        EXPECTED: * Bet receipt is displayed with correct data
        """
        pass

    def test_009_for_mobile_and_desktopclose_bet_receipt_and_navigate_to_my_bets__open_bets(self):
        """
        DESCRIPTION: **For mobile and desktop:**
        DESCRIPTION: Close bet receipt and navigate to 'My bets' > 'Open bets'
        EXPECTED: * Bet from step 6 is NOT shown on 'My bets' > 'Open bets'
        EXPECTED: * Bet from step 8 is shown
        """
        pass
