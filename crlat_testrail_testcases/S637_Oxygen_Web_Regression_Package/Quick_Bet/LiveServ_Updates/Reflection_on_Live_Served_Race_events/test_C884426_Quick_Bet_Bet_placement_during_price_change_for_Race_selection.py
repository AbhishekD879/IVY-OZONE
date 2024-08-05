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
class Test_C884426_Quick_Bet_Bet_placement_during_price_change_for_Race_selection(Common):
    """
    TR_ID: C884426
    NAME: Quick Bet Bet placement during price change for <Race> selection
    DESCRIPTION: This test case verifies Quick Bet reflection on <Race> events simultaneously with bet placement when price is changed
    DESCRIPTION: AUTOTEST [C2012654]
    PRECONDITIONS: 1. User is logged in with positive balance
    PRECONDITIONS: 2. Price updates are received in Betslip microservice:
    PRECONDITIONS: Development tool> Network> WS> remotebetslip/?EIO=3&transport=websocket
    PRECONDITIONS: 3. Price updates can be received for LP priced selections
    """
    keep_browser_open = True

    def test_001_navigate_to_race_in_play_page(self):
        """
        DESCRIPTION: Navigate to <Race> In-play page
        EXPECTED: 
        """
        pass

    def test_002_navigate_to_event_details_page_and_select_any_selection(self):
        """
        DESCRIPTION: Navigate to event details page and select any selection
        EXPECTED: Selection is successfully added to Quick Bet
        """
        pass

    def test_003_enter_stake_value_for_selection(self):
        """
        DESCRIPTION: Enter stake value for selection
        EXPECTED: Stake value is entered
        """
        pass

    def test_004_in_backoffice_tool_change_price_for_selection_and_save_changes(self):
        """
        DESCRIPTION: In Backoffice tool change price for selection and save changes
        EXPECTED: 
        """
        pass

    def test_005_in_the_same_time_while_changes_in_backoffice_are_not_saved___tap_place_bet_button(self):
        """
        DESCRIPTION: In the same time while changes in Backoffice are not saved >  Tap 'PLACE BET' button
        EXPECTED: Old Odds are instantly changed to New Odds
        EXPECTED: NOTE: Price corresponds to value received in 'remotebetslip/?EIO=3&transport=websocket' response
        EXPECTED: * 'Price changed from 'n' to 'n'' warning message is displayed on yellow(Coral)/cyan(Ladbrokes) background below 'QUICK BET' header
        EXPECTED: 'ADD TO BETSLIP' and 'ACCEPT & PLACE BET' buttons are enabled
        EXPECTED: Bet is not placed.
        """
        pass

    def test_006_tap_on_accept__place_bet_button(self):
        """
        DESCRIPTION: Tap on 'ACCEPT & PLACE BET' button
        EXPECTED: * Spinner appears instead of label 'ACCEPT & PLACE BET'.
        EXPECTED: * Bet is placed successfully and Bet receipt is shown.
        """
        pass
