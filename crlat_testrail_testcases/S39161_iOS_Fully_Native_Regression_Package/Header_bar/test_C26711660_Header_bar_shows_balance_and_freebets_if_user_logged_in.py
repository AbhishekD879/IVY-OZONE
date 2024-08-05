import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.user_account
@vtest
class Test_C26711660_Header_bar_shows_balance_and_freebets_if_user_logged_in(Common):
    """
    TR_ID: C26711660
    NAME: Header bar shows balance and freebets if user logged in
    DESCRIPTION: TC verifies if balance is shown for user while navigating through the app
    PRECONDITIONS: Some user with freebets should exist
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+Manually+Add+Freebet+Token+to+Account
    PRECONDITIONS: Some user with balance should exist
    PRECONDITIONS: App is installed
    """
    keep_browser_open = True

    def test_001_start_the_app(self):
        """
        DESCRIPTION: Start the app
        EXPECTED: App main screen appears. Login and register buttons are shown
        """
        pass

    def test_002_login_with_user_that_have_balance(self):
        """
        DESCRIPTION: Login with user that have balance
        EXPECTED: User logged in, balance is shown
        """
        pass

    def test_003_navigate_trough_the_app_go_to_some_sporteg_englend___some_league_eg_premiere_league___some_event___open_some_market_switch(self):
        """
        DESCRIPTION: Navigate trough the app Go to some sport(e.g. Englend) -> some league (e.g. Premiere League) -> some event -> open some market switch
        EXPECTED: Balance is shown while navigating throgh the app
        """
        pass

    def test_004_logout_and_login_with_user_that_have_free_bets(self):
        """
        DESCRIPTION: Logout and Login with user that have free bets
        EXPECTED: User logged in, balance with freebets is shown
        """
        pass

    def test_005_navigate_trough_the_app_go_to_some_sporteg_englend___some_league_eg_premiere_league___some_event___open_some_market_switch(self):
        """
        DESCRIPTION: Navigate trough the app Go to some sport(e.g. Englend) -> some league (e.g. Premiere League) -> some event -> open some market switch
        EXPECTED: Balance with freebets is shown while navigating throgh the app
        """
        pass
