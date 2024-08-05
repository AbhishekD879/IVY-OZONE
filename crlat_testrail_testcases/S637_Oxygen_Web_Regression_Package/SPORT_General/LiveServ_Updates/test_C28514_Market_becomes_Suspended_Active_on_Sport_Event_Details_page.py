import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@vtest
class Test_C28514_Market_becomes_Suspended_Active_on_Sport_Event_Details_page(Common):
    """
    TR_ID: C28514
    NAME: Market becomes Suspended/Active on <Sport>  Event Details page
    DESCRIPTION: AUTOTEST: [C13122031]
    PRECONDITIONS: **Updates are received via push notifications**
    """
    keep_browser_open = True

    def test_001_open_sportdetails_page(self):
        """
        DESCRIPTION: Open <Sport> Details page
        EXPECTED: 
        """
        pass

    def test_002_trigger_the_following_situation_for_this_eventmarketstatuscodes_for_one_of_its_market_typesand_at_the_same_time_have_event_details_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Trigger the following situation for this event:
        DESCRIPTION: **marketStatusCode="S"** for one of its market types
        DESCRIPTION: and at the same time have Event Details page opened to watch for updates
        EXPECTED: * All Price/Odds buttons of changed market type are displayed immediately as greyed out and become disabled on <Sports> Details page but still displaying the prices.
        EXPECTED: * The rest market types are not changed.
        """
        pass

    def test_003_change_attribute_for_this_eventmarketstatuscodea_for_the_same_market_typeand_at_the_same_time_have_event_details_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Change attribute for this event:
        DESCRIPTION: **marketStatusCode="A"** for the same market type
        DESCRIPTION: and at the same time have Event Details page opened to watch for updates
        EXPECTED: * All Price/Odds buttons  of the market are no more disabled, they become active immediately
        EXPECTED: * The rest market types remain not changed
        """
        pass
