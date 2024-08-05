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
class Test_C60088420_Verify_Greyhound_Page_Banner_section_with_logged_out_user(Common):
    """
    TR_ID: C60088420
    NAME: Verify Greyhound Page Banner section with logged out user
    DESCRIPTION: This test case verifies Greyhound Page Banner section content for logged out user with enabled Always On Stream Channel
    PRECONDITIONS: **TO BE FINISHED AFTER IMPLEMENTATION OF BMA-56791**
    PRECONDITIONS: List of CMS endpoints: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    PRECONDITIONS: Static block for Always On Stream Channel is created in CMS
    PRECONDITIONS: Designs:
    PRECONDITIONS: Ladbrokes: https://app.zeplin.io/project/5ba3a1f77d3b30391d93e665/dashboard?sid=5f748efe059ce64d59a70620
    PRECONDITIONS: Coral: https://app.zeplin.io/project/5d24ab732fabd699077b9b8c/dashboard?sid=5f748e0c0bf7df38a687f767
    PRECONDITIONS: In CMS: System Configuration > Structure > %future banner config name% -> set to enabled
    PRECONDITIONS: 1) Load app
    PRECONDITIONS: 2) User is NOT logged in
    """
    keep_browser_open = True

    def test_001__navigate_to_greyhounds_page_observe_banner_area(self):
        """
        DESCRIPTION: * Navigate to Greyhounds page
        DESCRIPTION: * Observe banner area
        EXPECTED: * Always On Stream Channel placeholder is displayed
        EXPECTED: * 'Play' button is displayed within image
        EXPECTED: * Text within placeholder is configured and corresponds to Static Block in CMS
        EXPECTED: ![](index.php?/attachments/get/122187722)
        EXPECTED: ![](index.php?/attachments/get/122187723)
        """
        pass

    def test_002_tappress_on_placeholder_image(self):
        """
        DESCRIPTION: Tap/press on placeholder image
        EXPECTED: Image area is not active for logged out user
        """
        pass

    def test_003_log_in_with_user_with_balance_0_or_placed_bet_during_last_24_hours(self):
        """
        DESCRIPTION: Log in with user with balance >0 or placed bet during last 24 hours
        EXPECTED: Stream with 'Play' button is displayed within banner area
        """
        pass
