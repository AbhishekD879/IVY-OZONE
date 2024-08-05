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
class Test_C28896_Outcome_Suspensions_on_Next_Races(Common):
    """
    TR_ID: C28896
    NAME: Outcome Suspensions on 'Next Races'
    DESCRIPTION: This test case verifies Suspensions of outcomes on 'Next Races'
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

    def test_002_trigger_the_following_situation_for_eventoutcomestatuscode__s_forone_of_the_outcomes_of_win_or_each_way_market(self):
        """
        DESCRIPTION: Trigger the following situation for event:
        DESCRIPTION: **outcomeStatusCode = 'S'** for one of the outcomes of 'Win or Each Way' market
        EXPECTED: 
        """
        pass

    def test_003_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Verify outcomes for the event
        EXPECTED: Price/Odds button for outcome is displayed immediately as greyed out and becomes disabled but still displaying the prices
        """
        pass

    def test_004_trigger_the_following_situation_for_the_same_outcomeoutcomestatuscode__a(self):
        """
        DESCRIPTION: Trigger the following situation for the same outcome:
        DESCRIPTION: **outcomeStatusCode = 'A'**
        EXPECTED: Price/Odds button for outcome becomes active again
        """
        pass

    def test_005_trigger_the_following_situation_for_eventoutcomestatuscode__s_forone_of_the_outcomes_of_win_or_each_way_market(self):
        """
        DESCRIPTION: Trigger the following situation for event:
        DESCRIPTION: **outcomeStatusCode = 'S'** for one of the outcomes of 'Win or Each Way' market
        EXPECTED: Price/Odds buttons for outcome are displayed immediately as greyed out and become disabled but still displaying the prices
        """
        pass

    def test_006_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: Suspended outcome disappears from the 'Next Races' module after page reloading
        """
        pass
