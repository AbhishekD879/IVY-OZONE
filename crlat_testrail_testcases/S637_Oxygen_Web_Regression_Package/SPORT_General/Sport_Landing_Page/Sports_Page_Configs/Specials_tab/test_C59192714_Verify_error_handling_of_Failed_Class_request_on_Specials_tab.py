import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C59192714_Verify_error_handling_of_Failed_Class_request_on_Specials_tab(Common):
    """
    TR_ID: C59192714
    NAME: Verify error handling of Failed Class request on 'Specials' tab
    DESCRIPTION: This test case verifies error handling of Failed Class request on 'Specials' tab for both Tier 1 and Tier 2 Sports
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to any Sport Landing page with Tier 1 Sport configuration -> 'Specials' tab
    PRECONDITIONS: 3. Block Class request in Chrome Dev tools -> Request blocking
    PRECONDITIONS: Example of Class request:
    PRECONDITIONS: "https://tst2-backoffice-lcm.ladbrokes.com/openbet-ssviewer/Drilldown/2.31/Class?translationLang=en&responseFormat=json&simpleFilter=class.categoryId:equals:16&simpleFilter=class.isActive&simpleFilter=class.siteChannels:contains:M&simpleFilter=class.hasOpenEvent"
    PRECONDITIONS: - Sport page configurations can be found here: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Sport+Page+Configs
    """
    keep_browser_open = True

    def test_001_refresh_the_page_and_verify_error_handling_of_blocked_class_request(self):
        """
        DESCRIPTION: Refresh the page and verify error handling of blocked Class request
        EXPECTED: * "Oops! We are having trouble loading this page. Please check your connection" message is shown.
        EXPECTED: * 'Try Again' button is displayed under the error message and is clickable
        """
        pass

    def test_002_unblock_class_request_in_chrome_dev_tools___request_blocking_and_press_on_try_again_button(self):
        """
        DESCRIPTION: Unblock Class request in Chrome Dev tools -> Request blocking and press on 'Try Again' button
        EXPECTED: * Class request is resent
        EXPECTED: * Class request is not failed and Class data is received
        EXPECTED: * Error message and 'Try Again' button are no longer displayed
        """
        pass

    def test_003_navigate_to_any_sport_landing_page_with_tier_2_sport_configuration___specials_tab_and_block_class_request_in_chrome_dev_tools___request_blocking(self):
        """
        DESCRIPTION: Navigate to any Sport Landing page with Tier 2 Sport configuration -> 'Specials' tab and block Class request in Chrome Dev tools -> Request blocking
        EXPECTED: 
        """
        pass

    def test_004_refresh_the_page_and_verify_error_handling_of_blocked_class_request(self):
        """
        DESCRIPTION: Refresh the page and verify error handling of blocked Class request
        EXPECTED: * "Oops! We are having trouble loading this page. Please check your connection" message is shown.
        EXPECTED: * 'Try Again' button is displayed under the error message and is clickable
        """
        pass

    def test_005_unblock_class_request_in_chrome_dev_tools___request_blocking_and_press_on_try_again_button(self):
        """
        DESCRIPTION: Unblock Class request in Chrome Dev tools -> Request blocking and press on 'Try Again' button
        EXPECTED: * Class request is resent
        EXPECTED: * Class request is not failed and Class data is received
        EXPECTED: * Error message and 'Try Again' button are no longer displayed
        """
        pass
