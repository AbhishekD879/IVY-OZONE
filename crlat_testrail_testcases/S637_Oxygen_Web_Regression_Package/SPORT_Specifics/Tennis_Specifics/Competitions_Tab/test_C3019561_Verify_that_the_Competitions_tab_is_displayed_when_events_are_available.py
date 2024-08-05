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
class Test_C3019561_Verify_that_the_Competitions_tab_is_displayed_when_events_are_available(Common):
    """
    TR_ID: C3019561
    NAME: Verify that the Competitions tab is displayed when events are available
    DESCRIPTION: Verify that the Competitions tab is displayed on the Tennis page when relevant events are available
    PRECONDITIONS: Competitions tab enabled in CMS
    PRECONDITIONS: Tennis Events in different classes/types are available
    PRECONDITIONS: **(!)** 'CompetitionsTennis' request is sent each time Competitions page(tab) is loaded(opened). Values from JSON response on this request are used to get the Class Accordion data from Openbet TI.
    """
    keep_browser_open = True

    def test_001_navigate_to_oxygen_fe_tennis_page(self):
        """
        DESCRIPTION: Navigate to Oxygen FE> Tennis Page
        EXPECTED: Competitions tab is available
        """
        pass

    def test_002_tap_on_competitions_tab(self):
        """
        DESCRIPTION: Tap on Competitions tab
        EXPECTED: Competitions tab content is displayed
        """
        pass
