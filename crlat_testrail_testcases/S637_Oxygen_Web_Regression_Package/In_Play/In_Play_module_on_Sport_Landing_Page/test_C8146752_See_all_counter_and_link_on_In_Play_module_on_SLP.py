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
class Test_C8146752_See_all_counter_and_link_on_In_Play_module_on_SLP(Common):
    """
    TR_ID: C8146752
    NAME: 'See all' counter and link on 'In-Play' module on SLP
    DESCRIPTION: This test case verifies 'See all' counter and link redirection on 'In-Play' module on SLP
    DESCRIPTION: AUTOTEST [C10386557]
    PRECONDITIONS: 1) CMS config:
    PRECONDITIONS: * 'In-Play' module is enabled in CMS > System Configuration > Structure > Inplay Module
    PRECONDITIONS: * 'In-Play' module is created in CMS > Sports Pages > Sport Categories > specific sport e.g. Football
    PRECONDITIONS: * 'In-play' module is set to 'Active'
    PRECONDITIONS: * 'Inplay event count' is set to any digit e.g. 10
    PRECONDITIONS: 2) In-play events should be present for selected sport e.g. Football
    PRECONDITIONS: 3) To check value, displayed in counter open Dev Tools->Network->WS > featured-sports > FEATURED_STRUCTURE_CHANGED > InplayModule > 'totalEvents' attribute
    PRECONDITIONS: Load the app and navigate to <Sport> Landing page under test e.g. Football
    PRECONDITIONS: Open 'Matches' tab
    """
    keep_browser_open = True

    def test_001_verify_see_all_link_within_in_play_module(self):
        """
        DESCRIPTION: Verify 'See all' link within 'In-Play' module
        EXPECTED: 'See all' link is located in the header of 'In-Play' module
        """
        pass

    def test_002_verify_counter_within_see_all_link(self):
        """
        DESCRIPTION: Verify counter within 'See all' link
        EXPECTED: * Counter shows total number of in-play events for specific sport
        EXPECTED: * Value in Counter corresponds to 'totalEvents' attribute in WS (see preconditions)
        """
        pass

    def test_003_tap_on_see_all_link(self):
        """
        DESCRIPTION: Tap on 'See all' link
        EXPECTED: Navigation to In-play page with specific sport tab selected e.g. In-play > Football
        """
        pass
