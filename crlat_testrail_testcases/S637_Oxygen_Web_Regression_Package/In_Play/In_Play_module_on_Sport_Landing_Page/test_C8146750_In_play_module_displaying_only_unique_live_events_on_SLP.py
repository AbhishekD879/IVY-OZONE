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
class Test_C8146750_In_play_module_displaying_only_unique_live_events_on_SLP(Common):
    """
    TR_ID: C8146750
    NAME: 'In-play' module displaying only unique live events on SLP
    DESCRIPTION: This test case verifies that only unique live events are displayed within 'In-play' module on SLP (i.e. if some live events are present in e.g. Highlight carousel, they won't be duplicated within 'In-play' module)
    PRECONDITIONS: 1) CMS config1:
    PRECONDITIONS: - 'In-Play' module is enabled in CMS > System Configuration > Structure > Inplay Module
    PRECONDITIONS: - 'In-Play' module is created and enabled in CMS > Sports Pages > Sport Categories > specific sport e.g. Football
    PRECONDITIONS: - 'Inplay event count' is set to any digit e.g. 20
    PRECONDITIONS: 2) CMS config2:
    PRECONDITIONS: - 'Highlight carousel' module is created and enabled in CMS > Sports Pages > Sport Categories > specific sport e.g. Football
    PRECONDITIONS: - 'Highlight carousel' module should have 'Display In-play events' ticked
    PRECONDITIONS: - Some events in Highlights Carousel should be configured as in-play events and some as prematch events
    PRECONDITIONS: 3) In-play events should be present for selected sport e.g. Football
    PRECONDITIONS: 1. Load the app and navigate to <Sport> Landing page under test e.g. Football
    PRECONDITIONS: 2. Open 'Matches' tab
    """
    keep_browser_open = True

    def test_001_verify_live_events_displayed_within_in_play_module(self):
        """
        DESCRIPTION: Verify live events displayed within 'In-Play' module
        EXPECTED: Only those live events that are NOT present in 'Highlight carousel' module are displayed within 'In-Play' module
        """
        pass

    def test_002__in_cms_untick_display_in_play_option_for_highlight_carousel_module_see_cms_config2_in_preconditions_in_application_refresh_the_page(self):
        """
        DESCRIPTION: * In CMS untick "Display In-Play" option for 'Highlight carousel' module (see CMS config2 in preconditions)
        DESCRIPTION: * In application refresh the page
        EXPECTED: * NO inplay events are displayed within 'Highlight carousel' module
        EXPECTED: * Inplay events that were previously displayed within 'Highlight carousel' module are now shown within 'In-Play' module
        """
        pass
