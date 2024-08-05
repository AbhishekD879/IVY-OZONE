import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C26832988_Header_changed_while_navigating_through_the_sports(Common):
    """
    TR_ID: C26832988
    NAME: Header changed while navigating through the sports
    DESCRIPTION: TC verifies if back button is shown for user while navigating through the app
    PRECONDITIONS: App is installed.
    PRECONDITIONS: Some user exist in system.
    """
    keep_browser_open = True

    def test_001_start_the_app(self):
        """
        DESCRIPTION: Start the app
        EXPECTED: App main screen appears
        """
        pass

    def test_002_navigate_trough_the_app_go_to_some_sporteg_englend___some_league_eg_premiere_league___some_event___open_some_market_switch(self):
        """
        DESCRIPTION: Navigate trough the app Go to some sport(e.g. Englend) -> some league (e.g. Premiere League) -> some event -> open some market switch
        EXPECTED: Header is changed to Football -> Premiere League -> Event
        """
        pass
