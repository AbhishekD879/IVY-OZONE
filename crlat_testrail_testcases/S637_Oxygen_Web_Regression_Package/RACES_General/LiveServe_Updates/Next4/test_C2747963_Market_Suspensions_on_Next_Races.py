import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C2747963_Market_Suspensions_on_Next_Races(Common):
    """
    TR_ID: C2747963
    NAME: Market Suspensions on 'Next Races'
    DESCRIPTION: This test case verifies Suspensions of market on 'Next Races'
    PRECONDITIONS: 'Next Races' module is present on <Race> Landing page
    PRECONDITIONS: **Updates are received in push notifications**
    """
    keep_browser_open = True

    def test_001_navigate_to_next_races_module(self):
        """
        DESCRIPTION: Navigate to 'Next Races' module
        EXPECTED: 
        """
        pass

    def test_002_trigger_the_following_situation_for_eventmarketstatuscode__s_forone_of_the_outcomes_of_win_or_each_way_market(self):
        """
        DESCRIPTION: Trigger the following situation for event:
        DESCRIPTION: **marketStatusCode = 'S'** for one of the outcomes of 'Win or Each Way' market
        EXPECTED: 
        """
        pass

    def test_003_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Verify outcomes for the event
        EXPECTED: All Price/Odds buttons of this event on Next Races are displayed immediately as greyed out and become disabled but still displaying the prices
        """
        pass

    def test_004_trigger_the_following_situation_for_the_same_marketmarketstatuscode__a(self):
        """
        DESCRIPTION: Trigger the following situation for the same market:
        DESCRIPTION: **marketStatusCode = 'A'**
        EXPECTED: Price/Odds buttons for outcomes of the event become active again
        """
        pass

    def test_005_trigger_the_following_situation_for_eventmarketstatuscode__s(self):
        """
        DESCRIPTION: Trigger the following situation for event:
        DESCRIPTION: **marketStatusCode = 'S'**
        EXPECTED: All Price/Odds buttons of this event on Next Races are displayed immediately as greyed out and become disabled but still displaying the prices
        """
        pass

    def test_006_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: Event with suspended 'Win or Each Way' market disappears from the 'Next Races' module after page reloading
        """
        pass
