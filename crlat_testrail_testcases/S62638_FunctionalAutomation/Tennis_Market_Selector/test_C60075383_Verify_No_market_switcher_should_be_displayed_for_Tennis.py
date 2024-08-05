import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C60075383_Verify_No_market_switcher_should_be_displayed_for_Tennis(Common):
    """
    TR_ID: C60075383
    NAME: Verify No market switcher should be displayed for Tennis
    DESCRIPTION: This test case verifies undisplaying of market switcher should be displayed for Tennis
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Tennis Landing page -> Matches, Inplay and Competitions  tab
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) Markets should be created in OB system
    PRECONDITIONS: 2) To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 3. Toggle should not be configured in CMS
    """
    keep_browser_open = True

    def test_001_navigate_to_tennis___click_on_matches_tab(self):
        """
        DESCRIPTION: Navigate to Tennis -> Click on Matches Tab
        EXPECTED: Market Switcher dropdown should be displayed
        """
        pass

    def test_002_navigate_to_tennis___click_on_inplay_tab(self):
        """
        DESCRIPTION: Navigate to Tennis -> Click on Inplay Tab
        EXPECTED: Market Switcher dropdown should be displayed
        """
        pass

    def test_003_navigate_to_tennis___click_on_competition_tab(self):
        """
        DESCRIPTION: Navigate to Tennis -> Click on Competition Tab
        EXPECTED: Market Switcher dropdown should be displayed
        """
        pass
