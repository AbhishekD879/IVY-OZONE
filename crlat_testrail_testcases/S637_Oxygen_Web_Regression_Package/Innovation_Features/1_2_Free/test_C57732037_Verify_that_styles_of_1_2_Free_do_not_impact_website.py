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
class Test_C57732037_Verify_that_styles_of_1_2_Free_do_not_impact_website(Common):
    """
    TR_ID: C57732037
    NAME: Verify that styles of 1-2-Free do not impact website
    DESCRIPTION: This test case verifies that styles of 1-2-Free do not impact website
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Zeplin
    PRECONDITIONS: 1. The user is logged in https://m.ladbrokes.com
    """
    keep_browser_open = True

    def test_001_open_the_ladbrokescoral_website(self):
        """
        DESCRIPTION: Open the Ladbrokes/Coral website.
        EXPECTED: The website is opened
        """
        pass

    def test_002_tap_on_the_1_2_free_link(self):
        """
        DESCRIPTION: Tap on the '1-2-Free' link
        EXPECTED: '1-2-Free' is succssefuly opened and displayed
        """
        pass

    def test_003_close_1_2_free(self):
        """
        DESCRIPTION: Close '1-2-Free'
        EXPECTED: '1-2-Free' is succssefuly closed
        """
        pass

    def test_004_open_the_homepage_and_check_if_any_styles_and_functionality_do_not_impact_website(self):
        """
        DESCRIPTION: Open the homepage and check if any styles and functionality do not impact website
        EXPECTED: - Spinner has NOT disappeared before featured data was loaded
        EXPECTED: - NO empty black screen instead of displaying spinner or featured data
        EXPECTED: - All functionality on the website works correctly as before opening '1-2-Free'
        """
        pass
