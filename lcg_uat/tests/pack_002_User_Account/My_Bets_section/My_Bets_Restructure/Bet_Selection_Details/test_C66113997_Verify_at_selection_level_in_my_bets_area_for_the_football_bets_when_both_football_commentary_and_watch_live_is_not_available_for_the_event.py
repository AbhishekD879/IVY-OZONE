import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C66113997_Verify_at_selection_level_in_my_bets_area_for_the_football_bets_when_both_football_commentary_and_watch_live_is_not_available_for_the_event(Common):
    """
    TR_ID: C66113997
    NAME: Verify at selection level in my bets area for the football bets when both football commentary and watch live is not available for the event
    DESCRIPTION: Verify at selection level in my bets area for the football bets when both football commentary and watch live is not available for the event
    PRECONDITIONS: Football bets on inplay events should be available in Open,Cashout,Settled tabs. Commentary  and streaming should not be available for the events showing in Open,Cash out,Settled tabs
    """
    keep_browser_open = True

    def test_000_load_oxygen_application(self):
        """
        DESCRIPTION: Load oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_001_login_to_the_application_with_valid_credentials(self):
        """
        DESCRIPTION: Login to the application with valid credentials
        EXPECTED: User is logged in
        """
        pass

    def test_002_tap_on_my_bets_item_on_top_menu(self):
        """
        DESCRIPTION: Tap on 'My bets' item on top menu
        EXPECTED: My bets page/Betslip widget is opened.By default user will be on open tab
        """
        pass

    def test_003_verify_football_bets_for_which_commentary_and_streaming_is_not_available_in_open_tab(self):
        """
        DESCRIPTION: Verify football bets for which commentary and Streaming is not available in open tab
        EXPECTED: Commentary and Watch live should not be displayed and no additional space should be displayed for the commentary and watch live
        """
        pass

    def test_004_verify_football_bets_for_which_commentary_and_streaming_is_available_in_cashout_tab(self):
        """
        DESCRIPTION: Verify football bets for which commentary and Streaming is available in Cashout tab
        EXPECTED: Commentary and Watch live should not be displayed and no additional space should be displayed for the commentary and watch live
        """
        pass
