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
class Test_C59192712_Verify_error_handling_for_failed_EventToOutcomeForClass_request_on_SLP_for_Tier_1_Sports(Common):
    """
    TR_ID: C59192712
    NAME: Verify error handling for failed /EventToOutcomeForClass request on SLP for Tier 1 Sports
    DESCRIPTION: This test case verifies error handling for failed /EventToOutcomeForClass request on on 'Matches'(Mobile), 'Today'/'Tomorrow'/'Future'(Desktop) tabs for different Sports
    PRECONDITIONS: 1. https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs - list of Tier 1 and Tier 2 sports.
    PRECONDITIONS: 2. Choose one Football event, one more event from Tier 1 (Tennis, Basketball)
    PRECONDITIONS: 3. Go to Dev Tools > Network > enter 'simpleFilter' in search field > EventToOutcomeForClass.
    """
    keep_browser_open = True

    def test_001_navigate_to_to_matchesmobile_todaytomorrowfuturedesktop_tabs_on_football_sport_landing_page(self):
        """
        DESCRIPTION: Navigate to to 'Matches'(Mobile), 'Today'/'Tomorrow'/'Future'(Desktop) tabs on Football Sport Landing page
        EXPECTED: 
        """
        pass

    def test_002_block_eventtooutcomeforclass_request_in_chrome_dev_tools___request_blocking_and_refresh_the_page(self):
        """
        DESCRIPTION: Block EventToOutcomeForClass request in Chrome Dev tools -> Request blocking and refresh the page
        EXPECTED: * "Oops! We are having trouble loading this page. Please check your connection" message is shown
        EXPECTED: * "TRY AGAIN" button is displayed under the error message and is clickable
        """
        pass

    def test_003_unblock_eventtooutcomeforclass_request_in_chrome_dev_tools___request_blocking_and_press_on_try_again_button(self):
        """
        DESCRIPTION: Unblock EventToOutcomeForClass request in Chrome Dev tools -> Request blocking and press on 'Try Again' button
        EXPECTED: * EventToOutcomeForClass request is resent
        EXPECTED: * EventToOutcomeForClass request is not failed and EventToOutcomeForClass data is received
        EXPECTED: * Error message and 'Try Again' button are no longer displayed
        """
        pass

    def test_004_navigate_to_to_matchesmobile_todaytomorrowfuturedesktop_tabs_on_any_other_sport_landing_page_with_tier_1_sport_configuration(self):
        """
        DESCRIPTION: Navigate to to 'Matches'(Mobile), 'Today'/'Tomorrow'/'Future'(Desktop) tabs on any other Sport Landing page with Tier 1 Sport configuration
        EXPECTED: 
        """
        pass

    def test_005_block_eventtooutcomeforclass_request_in_chrome_dev_tools___request_blocking_and_refresh_the_page(self):
        """
        DESCRIPTION: Block EventToOutcomeForClass request in Chrome Dev tools -> Request blocking and refresh the page
        EXPECTED: * "Oops! We are having trouble loading this page. Please check your connection" message is shown
        EXPECTED: * "TRY AGAIN" button is displayed under the error message and is clickable
        """
        pass

    def test_006_unblock_eventtooutcomeforclass_request_in_chrome_dev_tools___request_blocking_and_press_on_try_again_button(self):
        """
        DESCRIPTION: Unblock EventToOutcomeForClass request in Chrome Dev tools -> Request blocking and press on 'Try Again' button
        EXPECTED: * EventToOutcomeForClass request is resent
        EXPECTED: * EventToOutcomeForClass request is not failed and EventToOutcomeForClass data is received
        EXPECTED: * Error message and 'Try Again' button are no longer displayed
        """
        pass
