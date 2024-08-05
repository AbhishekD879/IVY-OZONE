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
class Test_C28476_SOFIYA_TO_EDIT_Verify_Event_Details_Page_of_unavailable_Sport_events(Common):
    """
    TR_ID: C28476
    NAME: SOFIYA TO EDIT Verify Event Details Page of unavailable <Sport> events
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True
