import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C28517_Outcome_becomes_Suspended_Active_on_Sport_Event_Details_page(Common):
    """
    TR_ID: C28517
    NAME: Outcome becomes Suspended/Active on <Sport> Event Details page
    DESCRIPTION: This test case verifies suspension/unsuspension of outcome on <Sport> Event Details page
    PRECONDITIONS: **Updates are received via push notifications**
    """
    keep_browser_open = True

    def test_001_open_sport_event_details_page(self):
        """
        DESCRIPTION: Open <Sport> Event Details page
        EXPECTED: 
        """
        pass

    def test_002_trigger_the_following_situation_for_this_eventoutcomestatuscodes_for_one_of_outcomes_of_any_expanded_marketand_at_the_same_time_have_event_details_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Trigger the following situation for this event:
        DESCRIPTION: **outcomeStatusCode="S"** for one of outcomes of any expanded market
        DESCRIPTION: and at the same time have Event Details page opened to watch for updates
        EXPECTED: 
        """
        pass

    def test_003_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Verify outcomes for the event
        EXPECTED: Price/Odds button of changed outcome is displayed immediately as greyed out and becomes disabled on <Sports> Event Details page but still displaying the price. The rest outcomes and market types are not changed.
        """
        pass

    def test_004_change_attribute_for_this_eventoutcomestatuscodea_for_the_same_outcomeand_at_the_same_time_have_event_details_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Change attribute for this event:
        DESCRIPTION: **outcomeStatusCode="A"** for the same outcome
        DESCRIPTION: and at the same time have Event Details page opened to watch for updates
        EXPECTED: Price/Odds button of this outcome becomes active immediately, the rest outcomes and market types remain not changed
        """
        pass

    def test_005_verify_outcome_suspension_in_collapsed_market(self):
        """
        DESCRIPTION: Verify outcome suspension in collapsed market
        EXPECTED: If section is collapsed and outcome was suspended, then after expanding the section Price/Odds button of this outcome is shown as greyed out and disabled
        """
        pass
