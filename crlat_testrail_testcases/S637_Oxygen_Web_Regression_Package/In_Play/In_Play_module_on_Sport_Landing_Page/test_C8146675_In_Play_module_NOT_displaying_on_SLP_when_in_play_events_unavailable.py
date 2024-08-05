import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C8146675_In_Play_module_NOT_displaying_on_SLP_when_in_play_events_unavailable(Common):
    """
    TR_ID: C8146675
    NAME: 'In-Play' module NOT displaying on SLP when in-play events unavailable
    DESCRIPTION: This test case verifies that 'In-Play' module is NOT displayed on SLP when set to 'active' in CMS but there are no in-play events available
    PRECONDITIONS: 1) CMS config:
    PRECONDITIONS: - 'In-Play' module is enabled in CMS > System Configuration > Structure > Inplay Module
    PRECONDITIONS: - 'In-Play' module is created in CMS > Sports Pages > Sport Categories > specific sport e.g. Football
    PRECONDITIONS: - 'In-play' module is set to 'Active'
    PRECONDITIONS: - 'Inplay event count' is set to any digit e.g. 10
    PRECONDITIONS: 2) NO in-play events should be present for selected sport e.g. Football
    PRECONDITIONS: 3) To check data regarding 'In-play' module, open Dev Tools->Network->WS > featured-sports
    PRECONDITIONS: 1. Load the app and navigate to <Sport> Landing page under test e.g. Football
    PRECONDITIONS: 2. Open 'Matches' tab
    """
    keep_browser_open = True

    def test_001_verify_in_play_module_availability(self):
        """
        DESCRIPTION: Verify 'In-play' module availability
        EXPECTED: * 'In-play' module is NOT displayed on 'Matches' tab
        EXPECTED: * 'In-play' module is NOT listed within "FEATURED_STRUCTURE_CHANGED" in 'featured-sports' (see preconditions)
        """
        pass
