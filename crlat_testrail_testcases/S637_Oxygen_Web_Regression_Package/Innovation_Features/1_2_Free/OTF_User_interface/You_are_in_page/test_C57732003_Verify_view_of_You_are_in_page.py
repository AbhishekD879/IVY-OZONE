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
class Test_C57732003_Verify_view_of_You_are_in_page(Common):
    """
    TR_ID: C57732003
    NAME: Verify view of 'You are in' page
    DESCRIPTION: This test case verifies 'You are in' page view
    PRECONDITIONS: Please look for some insights on a page as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Zeplin
    PRECONDITIONS: 1. The user is logged in https://m.ladbrokes.com
    PRECONDITIONS: 2. User on 'Current Tab'
    """
    keep_browser_open = True

    def test_001_tap_on_submit_button_on_current_tab(self):
        """
        DESCRIPTION: Tap on 'Submit' button on 'Current Tab'
        EXPECTED: 'You are in' page is successfully opened and designed according to:
        EXPECTED: https://app.zeplin.io/project/5b5f6d56008921750a2b9a82/screen/5c17957ed99c34afa7c10263
        EXPECTED: - Innovation logo
        EXPECTED: - Main text (pull from CMS->static text-> You are in page -> pageText1)
        EXPECTED: First carousel block 'Match Results' with:
        EXPECTED: - Title
        EXPECTED: - Matches with Match Results information
        EXPECTED: - Odds information
        EXPECTED: - 'Add To Slip' button
        """
        pass
