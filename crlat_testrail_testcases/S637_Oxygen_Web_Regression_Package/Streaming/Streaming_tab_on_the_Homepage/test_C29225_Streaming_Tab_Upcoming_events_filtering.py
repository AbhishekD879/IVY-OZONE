import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.streaming
@vtest
class Test_C29225_Streaming_Tab_Upcoming_events_filtering(Common):
    """
    TR_ID: C29225
    NAME: Streaming Tab: Upcoming events filtering
    DESCRIPTION: This test case verifies what events are present on Live Stream -> Upcoming page
    DESCRIPTION: **Jira tickets:** BMA-5106
    PRECONDITIONS: To get information about event use the following link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/x.xx/EventToOutcomeForEvent/xxxx?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: *   x.xx latest supported SiteServer version
    PRECONDITIONS: *   xxxx event id
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: 
        """
        pass

    def test_002_select_live_stream_tab_from_module_selector_ribbon(self):
        """
        DESCRIPTION: Select 'Live Stream' tab from Module Selector Ribbon
        EXPECTED: *   'Live Stream' tab is opened
        EXPECTED: *   'Live Now' sorting type is selected by default
        """
        pass

    def test_003_tap_upcoming_sorting_type_button(self):
        """
        DESCRIPTION: Tap 'Upcoming' sorting type button
        EXPECTED: 
        """
        pass

    def test_004_verify_events_that_are_present(self):
        """
        DESCRIPTION: Verify events that are present
        EXPECTED: Events which satisfy the following conditions should be present on the page:
        EXPECTED: **NOT Outrights:**
        EXPECTED: *   **drilldownTagNames **should include the following attributes: {EVFLAG\_BL and EVFLAG\_IVM} OR {EVFLAG\_BL, EVFLAG\_PVM} OR {EVFLAG_BL, EVFLAG_IVM, EVFLAG_PVM}(on the Event level)** **
        EXPECTED: *   AND **isMarketBetInRun="true" **(on the any Market level)
        EXPECTED: *   **event **startTime **is today**
        EXPECTED: **Outrights:**
        EXPECTED: *   **eventSortCode="TNMT"**
        EXPECTED: *   **drilldownTagNames **should include the following attributes: {EVFLAG\_BL and EVFLAG\_IVM} OR {EVFLAG\_BL, EVFLAG\_PVM} OR {EVFLAG_BL, EVFLAG_IVM, EVFLAG_PVM}(on the Event level)** **
        EXPECTED: *   AND **isMarketBetInRun="true" **(on the any Market level)
        EXPECTED: *   **event **startTime **is today**
        EXPECTED: Events should NOT have:
        EXPECTED: *   isStarted=true OR rawIsOffCode=Y
        """
        pass
