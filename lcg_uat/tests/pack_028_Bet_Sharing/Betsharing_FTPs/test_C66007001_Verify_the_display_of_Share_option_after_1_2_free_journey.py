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
class Test_C66007001_Verify_the_display_of_Share_option_after_1_2_free_journey(Common):
    """
    TR_ID: C66007001
    NAME: Verify the display of Share option after 1-2 free journey
    DESCRIPTION: This testcase verifies the display of Share option after 1-2 free journey
    PRECONDITIONS: 1. Bet sharing should be configured in CMS page.
    PRECONDITIONS: 2. Go to CMS-&gt;Bet sharing-&gt;enable.Note: 1. All bet share card details can be configured  and managed via CMS.
    """
    keep_browser_open = True

    def test_000_launch_and_login_to_the_application(self):
        """
        DESCRIPTION: Launch and login to the Application
        EXPECTED: User should be able to launch and login to application successfully
        """
        pass

    def test_000_complete_1_2_free_predictions_journey_and_navigate_to_final_screen(self):
        """
        DESCRIPTION: Complete 1-2 free predictions journey and navigate to final screen
        EXPECTED: User will be displayed with Share option
        """
        pass

    def test_000_verify_share_icon(self):
        """
        DESCRIPTION: Verify Share icon
        EXPECTED: User should be able to see share option
        """
        pass

    def test_000_click_on_share_option(self):
        """
        DESCRIPTION: Click on Share option
        EXPECTED: Then all the available sharing platforms will be displayed. Note: There will be no share card preference pop up in FTP share journey
        """
        pass

    def test_000_verify_share_card_is_displaying_with_a_static_message_and_image_which_are_configured_in_cms(self):
        """
        DESCRIPTION: Verify share card is displaying with a static message and image which are configured in CMS.
        EXPECTED: User should be able to see share card with static message and image
        """
        pass

    def test_000_verify_other_social_app_icons_are_displaying_below_the_image_in_share_card_window(self):
        """
        DESCRIPTION: Verify other social app icon's are displaying below the image in share card window.
        EXPECTED: User should be able to see other social app icon's below the image
        """
        pass

    def test_000_verify_share_card_has_been_sent_to_the_other_user_via_selected_social_app(self):
        """
        DESCRIPTION: Verify share card has been sent to the other user via selected social app.
        EXPECTED: User "B" should be able to see a share card which "A" user has shared.
        """
        pass
