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
class Test_C57732021_Verify_the_accessibility_of_the_app_connected_to_any_not_corporate_network(Common):
    """
    TR_ID: C57732021
    NAME: Verify the accessibility of the app connected to any (not corporate) network
    DESCRIPTION: This test case verifies the accessibility of the app connected to any (not corporate) network.
    PRECONDITIONS: 1. Connect a device to any (not corporate) network.
    PRECONDITIONS: 2. The user is logged in https://m.ladbrokes.com / app.
    PRECONDITIONS: 3. The Quick link 'Play 1-2-FREE predictor and win £150' is available on the Home page / Football page.
    """
    keep_browser_open = True

    def test_001_tap_on_the_1_2_free_link(self):
        """
        DESCRIPTION: Tap on the '1-2-Free' link.
        EXPECTED: The 'This week' tab is opened.
        EXPECTED: The Splash page is opened (only on mobile).
        """
        pass

    def test_002_tap_on_the_back_buttontap_on_the_cancel_button_only_on_mobile(self):
        """
        DESCRIPTION: Tap on the 'Back' button.
        DESCRIPTION: Tap on the 'Cancel' button (only on mobile).
        EXPECTED: The User is redirected to the Home page / Football page.
        """
        pass

    def test_003_tap_on_the_1_2_free_link(self):
        """
        DESCRIPTION: Tap on the '1-2-Free' link.
        EXPECTED: The 'This week' tab is opened.
        EXPECTED: The Splash page is opened (only on mobile).
        """
        pass

    def test_004_tap_on_the_play_now_button_only_on_mobile(self):
        """
        DESCRIPTION: Tap on the 'Play now' button (only on mobile).
        EXPECTED: The 'This week' tab is opened (only on mobile).
        """
        pass

    def test_005_tap_on_the_x_icon_only_on_mobile(self):
        """
        DESCRIPTION: Tap on the 'X' icon (only on mobile).
        EXPECTED: The User is redirected to the Home page / Football page.
        """
        pass

    def test_006_tap_on_the_1_2_free_link(self):
        """
        DESCRIPTION: Tap on the '1-2-Free' link.
        EXPECTED: The 'This week' tab is opened.
        EXPECTED: The Splash page is opened (only on mobile).
        """
        pass

    def test_007_tap_on_the_play_now_button_only_on_mobile(self):
        """
        DESCRIPTION: Tap on the 'Play now' button (only on mobile).
        EXPECTED: The 'This week' tab is opened.
        """
        pass

    def test_008_tap_on_the_last_weeks_results_tab(self):
        """
        DESCRIPTION: Tap on the 'Last weeks results' tab.
        EXPECTED: The 'Last weeks results' tab is opened.
        """
        pass

    def test_009_tap_on_the_this_week_tab(self):
        """
        DESCRIPTION: Tap on the 'This week' tab.
        EXPECTED: The 'This week' tab is opened.
        """
        pass

    def test_010_tap_on_the_show_more_link_only_on_mobile(self):
        """
        DESCRIPTION: Tap on the 'Show more...' link (only on mobile).
        EXPECTED: The text is expanded and displayed on the logo background (only on mobile).
        """
        pass

    def test_011_tap_on_the_hide_info_link_only_on_mobile(self):
        """
        DESCRIPTION: Tap on the 'Hide info' link (only on mobile).
        EXPECTED: The text is collapsed and displayed on the logo background (only on mobile).
        """
        pass

    def test_012_tap_on_the_submit_button(self):
        """
        DESCRIPTION: Tap on the 'Submit' button.
        EXPECTED: The predictions are successfully submitted.
        EXPECTED: The 'You are in' page is opened.
        """
        pass

    def test_013_tap_on_the_add_to_betslip_button(self):
        """
        DESCRIPTION: Tap on the 'Add to betslip' button.
        EXPECTED: The 'You are in' page is not closed.
        EXPECTED: The Upsell is successfully added to the Betslip.
        """
        pass

    def test_014_tap_on_the_back_to_betting_button(self):
        """
        DESCRIPTION: Tap on the 'Back to betting' button.
        EXPECTED: The User is redirected to the Homepage / Football page.
        """
        pass
