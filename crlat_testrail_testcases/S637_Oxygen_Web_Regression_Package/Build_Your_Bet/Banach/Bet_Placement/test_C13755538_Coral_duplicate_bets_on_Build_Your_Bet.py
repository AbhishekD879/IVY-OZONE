import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.build_your_bet
@vtest
class Test_C13755538_Coral_duplicate_bets_on_Build_Your_Bet(Common):
    """
    TR_ID: C13755538
    NAME: Coral duplicate bets on Build Your Bet
    DESCRIPTION: 
    PRECONDITIONS: Build Your Bets events and markets should be available. If events are not available please ping BYB team in the Slack channel - coral_byb_others_pi12.
    """
    keep_browser_open = True

    def test_001_log_into_application_and_navigate_to_the_build_your_bet_tab_on_the_home_page_in_case_if_there_is_no_buil_your_bet_tab_navigate_to_the_football_page_and_find_an_event_with_build_your_bet_yellow_label(self):
        """
        DESCRIPTION: Log into application and navigate to the 'Build Your Bet' tab on the home page (In case if there is no 'Buil Your Bet tab' navigate to the Football page and find an event with 'Build Your Bet yellow label').
        EXPECTED: ![](index.php?/attachments/get/30737)
        """
        pass

    def test_002_tap_on_an_event_and_select_build_your_bet_tab(self):
        """
        DESCRIPTION: Tap on an event and select 'Build Your Bet' tab
        EXPECTED: Markets should be available
        EXPECTED: ![](index.php?/attachments/get/30738)
        """
        pass

    def test_003_select_1_selection_from_2_first_markets_type(self):
        """
        DESCRIPTION: Select 1 selection from 2 first markets type
        EXPECTED: Place bet button should be displayed
        EXPECTED: ![](index.php?/attachments/get/30739)
        """
        pass

    def test_004_scroll_to_the_bottom_of_the_page_and_turn_off_network_connection(self):
        """
        DESCRIPTION: Scroll to the bottom of the page and turn off network connection
        EXPECTED: 
        """
        pass

    def test_005_turn_on_network_connection(self):
        """
        DESCRIPTION: Turn on network connection
        EXPECTED: The page should be reloaded
        EXPECTED: Place bet button is displayed
        """
        pass

    def test_006_open_dev_tools___network_tab___ws_and_tap_place_bet_button(self):
        """
        DESCRIPTION: Open dev tools -> Network tab -> WS and tap 'Place Bet' button
        EXPECTED: BYB quick bet window is displayed
        EXPECTED: Connection to the Remote betslip is opened
        EXPECTED: ![](index.php?/attachments/get/30740)
        """
        pass

    def test_007_enter_stake_and_place_bet_make_sure_that_only_one_stake_request_50011_and_betplacement_response_51101_are_present(self):
        """
        DESCRIPTION: Enter stake and place bet
        DESCRIPTION: !!! Make sure that only one stake request (50011) and betPlacement response (51101) are present
        EXPECTED: ![](index.php?/attachments/get/30741)
        """
        pass

    def test_008_not_a_permanent_defect_so_please_repeat_steps_3_7_three___five_times(self):
        """
        DESCRIPTION: Not a permanent defect, so please repeat steps 3-7 three - five times
        EXPECTED: 
        """
        pass
