import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.bet_history_open_bets
@vtest
class Test_C22934980_Verify_My_Bets_counter_UI(Common):
    """
    TR_ID: C22934980
    NAME: Verify My Bets counter UI
    DESCRIPTION: This test case verifies counter displaying when there are one, two and three symbols ( 20+) to display
    DESCRIPTION: Automated test: [C58637904]
    PRECONDITIONS: * Load Oxygen/Roxanne Application
    PRECONDITIONS: * Make sure 'BetsCounter' config is turned on in CMS > System configurations
    PRECONDITIONS: * 'My Bets' option is present and active in the top 5 list in Menus > Footer menus in CMS
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    """
    keep_browser_open = True

    def test_001__log_in_with_user_with_one_open_bet__unsettled_bet_available_verify_my_bets_counter_displaying(self):
        """
        DESCRIPTION: * Log in with user with one open bet ( unsettled bet) available
        DESCRIPTION: * Verify My Bets counter displaying
        EXPECTED: Coral: BetsCounter is displayed as a yellow round circle in top right corner of My Bets Footer Menu item with 1 digit ( 12 px)
        EXPECTED: Ladbrokes: BetsCounter is displayed as a red round circle in top right corner of My Bets Footer Menu item with 1 digit ( 12 px)
        """
        pass

    def test_002_log_out(self):
        """
        DESCRIPTION: Log out
        EXPECTED: My Bets counter is not displayed anymore
        """
        pass

    def test_003__log_in_with_user_with_10_open_bet__unsettled_bet_available_verify_my_bets_counter_displaying(self):
        """
        DESCRIPTION: * Log in with user with 10 open bet ( unsettled bet) available
        DESCRIPTION: * Verify My Bets counter displaying
        EXPECTED: Coral: BetsCounter is displayed as a yellow round circle in top right corner of My Bets Footer Menu item with '10' digit ( 12 px)
        EXPECTED: Ladbrokes: BetsCounter is displayed as a red round circle in top right corner of My Bets Footer Menu item with '10' digit ( 12 px)
        """
        pass

    def test_004__log_out(self):
        """
        DESCRIPTION: * Log out
        EXPECTED: My Bets counter is not displayed anymore
        """
        pass

    def test_005__log_in_with_user_with_20_plus_open_bet__unsettled_bet_available_verify_my_bets_counter_displaying(self):
        """
        DESCRIPTION: * Log in with user with 20 + open bet ( unsettled bet) available
        DESCRIPTION: * Verify My Bets counter displaying
        EXPECTED: Coral: BetsCounter is displayed as a yellow round circle in top right corner of My Bets Footer Menu item with '20+' digit ( 8 px)
        EXPECTED: Ladbrokes: BetsCounter is displayed as a red round circle in top right corner of My Bets Footer Menu item with '20+' digit ( 10 px)
        """
        pass

    def test_006__log_out(self):
        """
        DESCRIPTION: * Log out
        EXPECTED: My Bets counter is not displayed anymore
        """
        pass
