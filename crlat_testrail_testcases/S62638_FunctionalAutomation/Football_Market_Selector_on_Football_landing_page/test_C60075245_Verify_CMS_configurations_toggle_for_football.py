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
class Test_C60075245_Verify_CMS_configurations_toggle_for_football(Common):
    """
    TR_ID: C60075245
    NAME: Verify CMS configurations toggle for football
    DESCRIPTION: This test case verifies displaying of CMS configurations toggle for football
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Football Landing page -> Matches, Inplay and Competitions  tab
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following templateMarketNames:
    PRECONDITIONS: * |Match Betting| - "Match Result"
    PRECONDITIONS: * |To Qualify| - "To Qualify"
    PRECONDITIONS: * |Total Goals Over/Under| - "Total Goals Over/Under 2.5"
    PRECONDITIONS: * |Both Teams to Score| - "Both Teams to Score"
    PRECONDITIONS: * |To Win Not to Nil| - "To Win and Both Teams to Score" **Ladbrokes removed from OX 100.3**
    PRECONDITIONS: * |Match Result and Both Teams To Score| - "Match Result & Both Teams To Score" **Ladbrokes added from OX 100.3**
    PRECONDITIONS: * |Draw No Bet| - "Draw No Bet"
    PRECONDITIONS: * |First-Half Result| - "1st Half Result"
    PRECONDITIONS: 2) To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_go_to_cms___navigate_to_system_configurations___config___marketswitcher_and_make_sure_that_allsports_toggle_is_checked_along_with_football_toggle(self):
        """
        DESCRIPTION: Go to CMS -> Navigate to System Configurations -> Config -> MarketSwitcher and make sure that 'AllSports' toggle is checked along with football toggle
        EXPECTED: Market Switcher dropdown should be displayed in Matches, Inplay and Competitions Tab
        """
        pass

    def test_002_go_to_cms_and_make_sure_that_allsports_toggle_is_unchecked_and_football_toggle_is_checked(self):
        """
        DESCRIPTION: Go to CMS and make sure that 'AllSports' toggle is unchecked and football toggle is checked
        EXPECTED: Market Switcher dropdown should not be displayed in Matches, Inplay and Competitions Tab
        """
        pass

    def test_003_go_to_cms_and_make_sure_that_allsports_toggle_is_unchecked_and_football_toggle_is_unchecked(self):
        """
        DESCRIPTION: Go to CMS and make sure that 'AllSports' toggle is unchecked and football toggle is unchecked
        EXPECTED: Market Switcher dropdown should not be displayed in Matches, Inplay and Competitions Tab
        """
        pass
