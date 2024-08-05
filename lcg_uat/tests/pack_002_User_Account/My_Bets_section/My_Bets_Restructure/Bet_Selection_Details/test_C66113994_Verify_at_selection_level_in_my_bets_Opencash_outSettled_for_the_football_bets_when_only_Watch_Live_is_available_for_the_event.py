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
class Test_C66113994_Verify_at_selection_level_in_my_bets_Opencash_outSettled_for_the_football_bets_when_only_Watch_Live_is_available_for_the_event(Common):
    """
    TR_ID: C66113994
    NAME: Verify at selection level in my bets (Open,cash out,Settled) for the football bets when only Watch Live is available for the event
    DESCRIPTION: This testcase verifies at selection level in my bets (Open,Cashout,settled) for the football bets when only Watch Live is available for the event
    PRECONDITIONS: Sports and racing bets on events which offers streaming should be available in Open ,cash out settled tab
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

    def test_003_verify_watch_icon_for_the_events_which_offers_streaming_in_open_tab(self):
        """
        DESCRIPTION: Verify watch icon for the events which offers streaming in open tab
        EXPECTED: Watch icon should be displayed at bet selection area
        """
        pass

    def test_004_verify_watch_icon_for_the_events_which_offers_streaming_in_cash_out_tab(self):
        """
        DESCRIPTION: Verify watch icon for the events which offers streaming in Cash out tab
        EXPECTED: Watch icon should be displayed at bet selection area
        """
        pass

    def test_005_verify_watch_icon_for_the_events_which_offers_streaming_in_cash_out_tab(self):
        """
        DESCRIPTION: Verify watch icon for the events which offers streaming in Cash out tab
        EXPECTED: Watch icon should be displayed at bet selection area
        """
        pass

    def test_006_repeat_3_6_for_races(self):
        """
        DESCRIPTION: Repeat 3-6 for races
        EXPECTED: Result should be same
        """
        pass
