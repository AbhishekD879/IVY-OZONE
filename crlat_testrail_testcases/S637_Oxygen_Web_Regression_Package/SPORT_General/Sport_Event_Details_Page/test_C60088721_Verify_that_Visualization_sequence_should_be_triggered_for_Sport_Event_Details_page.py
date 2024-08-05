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
class Test_C60088721_Verify_that_Visualization_sequence_should_be_triggered_for_Sport_Event_Details_page(Common):
    """
    TR_ID: C60088721
    NAME: Verify that  Visualization sequence should be triggered for <Sport>  Event Details page
    DESCRIPTION: Test cases verifies presence of calls for 'bymapping' and 'scoreboard' when user is on <Sport> Event Details page
    PRECONDITIONS: 1) load app
    PRECONDITIONS: 2) navigate to <Sport> landing page
    PRECONDITIONS: 3) <Sport> events are present
    """
    keep_browser_open = True

    def test_001__navigate_to_tier_1__ltsportgt_event_details_pageeg_open_football_event(self):
        """
        DESCRIPTION: * Navigate to 'Tier 1'  &lt;Sport&gt; Event Details Page
        DESCRIPTION: (E.g.: open Football event)
        EXPECTED: * &lt;Sport&gt; Event Details Page is opened
        EXPECTED: * Scoreboard displays
        """
        pass

    def test_002__verify_that_there_are_successful__calls_for_bymapping_and_scoreboardegindexphpattachmentsget122251547indexphpattachmentsget122187839(self):
        """
        DESCRIPTION: * Verify that there are successful  calls for 'bymapping' and 'scoreboard'
        DESCRIPTION: E.g.:
        DESCRIPTION: ![](index.php?/attachments/get/122251547)
        DESCRIPTION: ![](index.php?/attachments/get/122187839)
        EXPECTED: * Calls for 'bymapping' and 'scoreboard' are present
        """
        pass

    def test_003__navigate_to_tier_2_ltsportgt_event_details_pageeg_cricket_make_sure_that__calls_for_bymapping_and_scoreboard_present(self):
        """
        DESCRIPTION: * Navigate to 'Tier 2' &lt;Sport&gt; Event Details page
        DESCRIPTION: (E.g.: Cricket)
        DESCRIPTION: * Make sure that  calls for 'bymapping' and 'scoreboard' present
        EXPECTED: * Calls for 'bymapping' and 'scoreboard'  are present
        """
        pass
