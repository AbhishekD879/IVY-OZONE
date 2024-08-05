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
class Test_C9697584_See_all_counter_updating_on_In_Play_module_on_SLP(Common):
    """
    TR_ID: C9697584
    NAME: 'See all' counter updating on 'In-Play' module on SLP
    DESCRIPTION: This test case verifies 'See all' counter updating when undisplaying/displaying back live events on 'In-Play' module on SLP
    DESCRIPTION: AUTOTEST [C10564960]
    PRECONDITIONS: 1) CMS config:
    PRECONDITIONS: * 'In-Play' module is enabled in CMS > System Configuration > Structure > Inplay Module
    PRECONDITIONS: * 'In-Play' module is created in CMS > Sports Pages > Sport Categories > specific sport e.g. Football
    PRECONDITIONS: * 'In-play' module is set to 'Active'
    PRECONDITIONS: * 'Inplay event count' is set to any digit e.g. 10
    PRECONDITIONS: 2) In-play events should be present for selected sport e.g. Football
    PRECONDITIONS: 3) To check value, displayed in counter open Dev Tools->Network->WS > featured-sports > InplayModule response > 'totalEvents' attribute
    PRECONDITIONS: Load the app and navigate to <Sport> Landing page under test e.g. Football
    PRECONDITIONS: Open 'Matches' tab
    """
    keep_browser_open = True

    def test_001_trigger_completionexpiration_of_in_play_event_of_sport_under_test_eg_footballnote_event_completionexpiration_means_that_event_is_not_present_on_siteserver_anymore_attribute_displayedn_is_set_for_event_(self):
        """
        DESCRIPTION: Trigger completion/expiration of in-play event of <sport> under test e.g. Football
        DESCRIPTION: NOTE: Event completion/expiration means that event is not present on SiteServer anymore (attribute 'displayed="N"' is set for event )
        EXPECTED: * Completed/expired event is removed from front-end automatically
        EXPECTED: * Counter next to 'See all' link is updated automatically
        EXPECTED: * Updated value in Counter corresponds to 'totalEvents' attribute in WS (see preconditions)
        """
        pass

    def test_002_trigger_starting_of_event_in_play_event_of_sport_under_test_eg_football(self):
        """
        DESCRIPTION: Trigger starting of event in-play event of <sport> under test e.g. Football
        EXPECTED: * Started event appears on front-end (after refresh)
        EXPECTED: * Counter next to 'See all' link is updated automatically (without refresh)
        EXPECTED: * Updated value in Counter corresponds to 'totalEvents' attribute in WS (see preconditions)
        """
        pass
