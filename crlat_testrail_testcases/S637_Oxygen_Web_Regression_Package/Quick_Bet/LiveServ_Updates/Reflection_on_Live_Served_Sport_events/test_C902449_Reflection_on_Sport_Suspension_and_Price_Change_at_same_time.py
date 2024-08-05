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
class Test_C902449_Reflection_on_Sport_Suspension_and_Price_Change_at_same_time(Common):
    """
    TR_ID: C902449
    NAME: Reflection on <Sport> Suspension and Price Change at same time
    DESCRIPTION: This test case verifies Quick Bet reflection on Sports Price Changed and Suspension at same time
    PRECONDITIONS: 1. Price format should be Fractional
    PRECONDITIONS: 2. Link to backoffice tool for price changing/suspension: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: 3. Price updates are received in Quick Bet microservice:
    PRECONDITIONS: Development tool> Network> WS> quickbet/?EIO=3&transport=websocket
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_sport_icon_from_the_sports_ribbon(self):
        """
        DESCRIPTION: Tap <Sport> icon from the sports ribbon
        EXPECTED: <Sport> Landing page is opened
        """
        pass

    def test_003_go_to_the_in_play_tab(self):
        """
        DESCRIPTION: Go to the 'In-Play' tab
        EXPECTED: 'In-Play' page with list of events is opened
        """
        pass

    def test_004_go_to_the_event_details_page(self):
        """
        DESCRIPTION: Go to the event details page
        EXPECTED: Event details page is opened
        """
        pass

    def test_005_make_single_selections(self):
        """
        DESCRIPTION: Make single selections
        EXPECTED: Quick Bet is opened with selection added
        """
        pass

    def test_006_change_price_for_the_selection_and_suspend_it_in_backoffice_tool(self):
        """
        DESCRIPTION: Change price for the selection and suspend it in Backoffice tool
        EXPECTED: Changes are saved
        """
        pass

    def test_007_check_price_displaying_in_quick_bet(self):
        """
        DESCRIPTION: Check price displaying in Quick Bet
        EXPECTED: Old Odds are instantly changed to New Odds
        EXPECTED: * Stake field is greyed out(disabled)
        """
        pass

    def test_008_verify_warning_message_and_login__place_bet_button_displaying(self):
        """
        DESCRIPTION: Verify warning message and 'LOGIN & PLACE BET' button displaying
        EXPECTED: * 'Your Selection has been Suspended' warning message is displayed on yellow(Coral)/cyan(Ladbrokes) background below 'QUICK BET' header
        EXPECTED: * 'LOGIN & PLACE BET' button is disabled(greyed out)
        """
        pass

    def test_009_close_quick_bet(self):
        """
        DESCRIPTION: Close Quick Bet
        EXPECTED: * Quick Bet is closed
        EXPECTED: * Selection is unselected
        """
        pass

    def test_010_go_to_settings_and_switch_odds_format_to_decimal(self):
        """
        DESCRIPTION: Go to Settings and switch Odds format to Decimal
        EXPECTED: 
        """
        pass

    def test_011_repeat_steps_2_9(self):
        """
        DESCRIPTION: Repeat steps #2-9
        EXPECTED: Results are the same
        """
        pass

    def test_012_login_with_user_account_with_positive_balance(self):
        """
        DESCRIPTION: Login with user account with positive balance
        EXPECTED: 
        """
        pass

    def test_013_repeat_steps_2_11_for_logged_in_user(self):
        """
        DESCRIPTION: Repeat steps #2-11 for Logged In User
        EXPECTED: Results are the same, only 'LOGIN & PLACE BET' button name changes to 'PLACE BET'.
        """
        pass
