import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.virtual_sports
@vtest
class Test_C869705_Verify_Virtual_Sports_when_no_events_are_available(Common):
    """
    TR_ID: C869705
    NAME: Verify Virtual Sports when no events are available
    DESCRIPTION: This test case verifies Virtual Sports when there are no events available.
    PRECONDITIONS: 1. The CMS User is logged in.
    PRECONDITIONS: 2. Navigate to Virtual Sports section.
    PRECONDITIONS: 3. Select any Parent Sport.
    PRECONDITIONS: 4. Uncheck 'Active' checkbox.
    PRECONDITIONS: 5. Save the changes.
    PRECONDITIONS: 6. Repeat steps 3-5 for all Parent Sports.
    """
    keep_browser_open = True

    def test_001_open_virtual_sports_tab_on_fe(self):
        """
        DESCRIPTION: Open 'Virtual Sports' tab on FE.
        EXPECTED: - User is shown a message 'Sorry no Virtual Sports events are available at this time' on the page
        EXPECTED: - Back button and 'Virtual' tab name is displayed at the top
        """
        pass
