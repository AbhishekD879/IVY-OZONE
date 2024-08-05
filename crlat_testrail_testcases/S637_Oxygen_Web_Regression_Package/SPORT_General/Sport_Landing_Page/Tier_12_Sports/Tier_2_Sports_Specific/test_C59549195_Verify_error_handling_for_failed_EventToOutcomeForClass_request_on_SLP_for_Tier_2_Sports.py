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
class Test_C59549195_Verify_error_handling_for_failed_EventToOutcomeForClass_request_on_SLP_for_Tier_2_Sports(Common):
    """
    TR_ID: C59549195
    NAME: Verify error handling for failed /EventToOutcomeForClass request on SLP for Tier 2 Sports
    DESCRIPTION: This test case verifies error handling for failed /EventToOutcomeForClass request on on 'Matches'(Mobile), 'Today'/'Tomorrow'/'Future'(Desktop) tabs for different Sports
    PRECONDITIONS: 1. https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs - list of Tier 1 and Tier 2 sports.
    PRECONDITIONS: 2. Choose one Football event, one more event from Tier 2 and Tier 2 sport Outright(Golf, Cycling, Hurling, Motorbikes).
    PRECONDITIONS: 3. Go to Dev Tools > Network > enter 'simpleFilter' in search field > EventToOutcomeForClass.
    """
    keep_browser_open = True

    def test_001_navigate_to_to_matchesmobile_todaytomorrowfuturedesktop_tabs_on_any_sport_landing_page_with_tier_2_sport_configuration(self):
        """
        DESCRIPTION: Navigate to to 'Matches'(Mobile), 'Today'/'Tomorrow'/'Future'(Desktop) tabs on any Sport Landing page with Tier 2 Sport configuration
        EXPECTED: 
        """
        pass

    def test_002_block_eventtooutcomeforclass_request_in_chrome_dev_tools__gt_request_blocking_and_refresh_the_page(self):
        """
        DESCRIPTION: Block EventToOutcomeForClass request in Chrome Dev tools -&gt; Request blocking and refresh the page
        EXPECTED: * "Oops! We are having trouble loading this page. Please check your connection" message is shown
        EXPECTED: * "TRY AGAIN" button is displayed under the error message and is clickable
        """
        pass

    def test_003_unblock_eventtooutcomeforclass_request_in_chrome_dev_tools__gt_request_blocking_and_press_on_try_again_button(self):
        """
        DESCRIPTION: Unblock EventToOutcomeForClass request in Chrome Dev tools -&gt; Request blocking and press on 'Try Again' button
        EXPECTED: * EventToOutcomeForClass request is resent
        EXPECTED: * EventToOutcomeForClass request is not failed and EventToOutcomeForClass data is received
        EXPECTED: * Error message and 'Try Again' button are no longer displayed
        """
        pass
