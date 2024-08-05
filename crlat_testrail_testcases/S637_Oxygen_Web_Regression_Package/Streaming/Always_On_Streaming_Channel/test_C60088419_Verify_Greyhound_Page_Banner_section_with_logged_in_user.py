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
class Test_C60088419_Verify_Greyhound_Page_Banner_section_with_logged_in_user(Common):
    """
    TR_ID: C60088419
    NAME: Verify Greyhound Page Banner section with logged in user
    DESCRIPTION: This test case verifies Greyhound Page Banner section content for logged in user with enabled Always On Stream Channel
    PRECONDITIONS: **TO BE FINISHED AFTER IMPLEMENTATION OF BMA-56791**
    PRECONDITIONS: List of CMS endpoints: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    PRECONDITIONS: Static block for Always On Stream Channel is created in CMS
    PRECONDITIONS: Designs:
    PRECONDITIONS: Ladbrokes: https://app.zeplin.io/project/5ba3a1f77d3b30391d93e665/dashboard?sid=5f748efe059ce64d59a70620
    PRECONDITIONS: Coral: https://app.zeplin.io/project/5d24ab732fabd699077b9b8c/dashboard?sid=5f748e0c0bf7df38a687f767
    PRECONDITIONS: In CMS: System Configuration > Structure > %future banner config name% -> set to **enabled**
    PRECONDITIONS: 1) Load app
    """
    keep_browser_open = True

    def test_001_log_in_with_user_with_0_balance_and_no_placed_bets_during_last_24_hours_eg_just_registered_user(self):
        """
        DESCRIPTION: Log in with user with 0 balance and NO placed bets during last 24 hours (e.g. just registered user)
        EXPECTED: User is successfully logged in
        """
        pass

    def test_002__navigate_to_greyhounds_page_observe_banner_area(self):
        """
        DESCRIPTION: * Navigate to Greyhounds page
        DESCRIPTION: * Observe banner area
        EXPECTED: * Always On Stream Channel placeholder is displayed
        EXPECTED: * 'Play' button is displayed within image
        EXPECTED: * Text within placeholder is configured and corresponds to Static Block in CMS
        """
        pass

    def test_003_press_play_button(self):
        """
        DESCRIPTION: Press 'Play' button
        EXPECTED: * No action performed (Placeholder is not an active area)
        """
        pass

    def test_004_log_out_from_app(self):
        """
        DESCRIPTION: Log out from app
        EXPECTED: User is successfully logged out
        """
        pass

    def test_005_log_in_with_user_with_balance_0_or_placed_bet_during_last_24_hours(self):
        """
        DESCRIPTION: Log in with user with balance >0 or placed bet during last 24 hours
        EXPECTED: User is successfully logged in
        """
        pass

    def test_006__navigate_to_greyhounds_page_observe_banner_area(self):
        """
        DESCRIPTION: * Navigate to Greyhounds page
        DESCRIPTION: * Observe banner area
        EXPECTED: Stream with 'Play' button is displayed within banner area
        """
        pass

    def test_007_press_play_button(self):
        """
        DESCRIPTION: Press 'Play' button
        EXPECTED: * Stream is successfully launched
        EXPECTED: * Stream is muted by default
        EXPECTED: ![](index.php?/attachments/get/122187728)
        EXPECTED: ![](index.php?/attachments/get/122187729)
        """
        pass

    def test_008_check_opt_in_request_in_devtools_network_tab__opt_filter(self):
        """
        DESCRIPTION: Check opt-in request in devTools (Network tab > 'opt' filter)
        EXPECTED: * Opt-In request is present
        EXPECTED: * iGameMedia provider is mentioned in request
        EXPECTED: ![](index.php?/attachments/get/122187727)
        """
        pass
