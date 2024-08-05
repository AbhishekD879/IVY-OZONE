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
class Test_C60088423_Verify_that_Visualization_sequence_should_not_be_triggered_for_Special_Event_Details_page(Common):
    """
    TR_ID: C60088423
    NAME: Verify that  Visualization sequence should not be triggered for Special Event Details page
    DESCRIPTION: Test cases verifies absence of calls for 'bymapping' and 'scoreboard' when user is on Special Event Details page
    PRECONDITIONS: 1) load app
    PRECONDITIONS: 2) navigate to <Sport> landing page > Specials tab
    PRECONDITIONS: 3) 'Special' events are present (EVFLAG_SP is present for event in SS response)
    """
    keep_browser_open = True

    def test_001__open_sport_special_event_details_page(self):
        """
        DESCRIPTION: * Open <Sport> Special Event Details Page
        EXPECTED: * Special Event Details Page is opened
        """
        pass

    def test_002__verify_that_there_are_no_calls_for_bymappingegindexphpattachmentsget122251546(self):
        """
        DESCRIPTION: * Verify that there are no calls for 'bymapping'
        DESCRIPTION: E.g.:
        DESCRIPTION: ![](index.php?/attachments/get/122251546)
        EXPECTED: * No calls for 'bymapping' when Special Event Details Page
        """
        pass

    def test_003__verify_that_there_are_no_calls_for_scoreboardegindexphpattachmentsget122187554(self):
        """
        DESCRIPTION: * Verify that there are no calls for 'scoreboard'
        DESCRIPTION: E.g.:
        DESCRIPTION: ![](index.php?/attachments/get/122187554)
        EXPECTED: * No calls for 'scoreboard' when Special Event Details Page
        """
        pass

    def test_004__navigate_to_different_sport_special_event_details_pages_and_make_sure_that_there_are_no_calls_for_bymapping_and_scoreboard(self):
        """
        DESCRIPTION: * Navigate to different <Sport> Special Event Details Pages and make sure that there are no calls for 'bymapping' and 'scoreboard'
        EXPECTED: * There are no calls for
        EXPECTED: 'bymapping' and
        EXPECTED: 'scoreboard'
        EXPECTED: when surfing  between different Sport> Special Event Details Pages
        """
        pass
