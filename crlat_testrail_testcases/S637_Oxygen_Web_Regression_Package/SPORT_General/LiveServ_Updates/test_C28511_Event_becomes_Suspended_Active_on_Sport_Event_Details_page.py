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
class Test_C28511_Event_becomes_Suspended_Active_on_Sport_Event_Details_page(Common):
    """
    TR_ID: C28511
    NAME: Event becomes Suspended/Active on <Sport> Event Details page
    DESCRIPTION: This test case verifies Event Details Page after event is suspended and unsuspended
    DESCRIPTION: AUTOTEST [C647555]
    PRECONDITIONS: **Updates are received via push notifications**
    """
    keep_browser_open = True

    def test_001_open_event_details_page(self):
        """
        DESCRIPTION: Open Event Details page
        EXPECTED: 
        """
        pass

    def test_002_suspend_event_in_tieventstatuscodesand_at_the_same_time_have_event_details_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Suspend event in TI:
        DESCRIPTION: **eventStatusCode="S"**
        DESCRIPTION: and at the same time have Event Details page opened to watch for updates
        EXPECTED: All Price/Odds buttons of this event are displayed immediately as greyed out and become disabled, but still displaying the prices
        """
        pass

    def test_003_make_event_active_again_in_tieventstatuscodeaand_at_the_same_time_have_event_details_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Make event Active again in TI:
        DESCRIPTION: **eventStatusCode="A" **
        DESCRIPTION: and at the same time have Event Details page opened to watch for updates
        EXPECTED: All Price/Odds buttons of this event are no more disabled, they become active immediately
        """
        pass
