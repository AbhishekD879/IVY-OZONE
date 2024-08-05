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
class Test_C904907_Reflection_on_Sport_Unsuspension_and_Price_change(Common):
    """
    TR_ID: C904907
    NAME: Reflection on <Sport> Unsuspension and Price change
    DESCRIPTION: This test case verifies Quick Bet reflection when selection is unsuspended and price is changed at same time
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

    def test_006_suspend_selectionmarketevent_in_backoffice_tool(self):
        """
        DESCRIPTION: Suspend selection/market/event in Backoffice tool
        EXPECTED: Changes are saved
        """
        pass

    def test_007_check_selection_is_suspended_in_quick_bet(self):
        """
        DESCRIPTION: Check selection is suspended in Quick Bet
        EXPECTED: * 'Your Selection/Market/Event has been Suspended' warning message is displayed on yellow(Coral)/cyan(Ladbrokes) background below 'QUICK BET' header
        EXPECTED: - Stake field becomes disabled
        EXPECTED: - 'LOGIN & PLACE BET' and 'Add to Betslip' buttons are disabled
        """
        pass

    def test_008_unsuspend_selectionmarketevent_in_backoffice_tool_and_change_price_for_selection_at_same_time(self):
        """
        DESCRIPTION: Unsuspend selection/market/event in Backoffice tool and change price for selection at same time
        EXPECTED: Changes are saved
        """
        pass

    def test_009_check_selection_is_unsuspended_and_new_price_is_displayed_in_quick_bet(self):
        """
        DESCRIPTION: Check selection is unsuspended and new price is displayed in Quick Bet
        EXPECTED: Old Odds are instantly changed to New Odds
        EXPECTED: * No warning message is displayed
        EXPECTED: * 'LOGIN & PLACE BET' and 'ADD TO BETSLIP' buttons are enabled(clickable)
        """
        pass

    def test_010_close_quick_bet(self):
        """
        DESCRIPTION: Close Quick Bet
        EXPECTED: * Quick Bet is closed
        EXPECTED: * Selection is unselected
        """
        pass

    def test_011_go_to_settings_and_switch_odds_format_to_decimal(self):
        """
        DESCRIPTION: Go to Settings and switch Odds format to Decimal
        EXPECTED: 
        """
        pass

    def test_012_repeat_steps_2_10(self):
        """
        DESCRIPTION: Repeat steps #2-10
        EXPECTED: * Results are the same
        EXPECTED: * Price is displayed in decimal format
        """
        pass

    def test_013_repeat_steps_2_11_for_logged_in_user(self):
        """
        DESCRIPTION: Repeat steps #2-11 for Logged In User
        EXPECTED: Results are the same, only 'PLACE BET' button is shown instead of 'LOGIN & PLACE BET'
        """
        pass
