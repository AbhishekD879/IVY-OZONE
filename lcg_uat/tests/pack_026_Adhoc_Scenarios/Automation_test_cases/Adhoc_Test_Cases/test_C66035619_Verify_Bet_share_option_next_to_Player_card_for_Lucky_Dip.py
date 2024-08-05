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
class Test_C66035619_Verify_Bet_share_option_next_to_Player_card_for_Lucky_Dip(Common):
    """
    TR_ID: C66035619
    NAME: Verify Bet share option next to Player card for Lucky Dip
    DESCRIPTION: This testcase verifies  Share option next to the Player card after 'Got it' button
    PRECONDITIONS: Bet sharing should be configured in CMS page.
    PRECONDITIONS: Go to CMS->Bet sharing->enable.
    PRECONDITIONS: Note: 1. All bet share card details can be configured and managed via CMS.
    """
    keep_browser_open = True

    def test_000_launch_and_login_to_the_application(self):
        """
        DESCRIPTION: Launch and login to the Application
        EXPECTED: User should be able to launch and login to application successfully
        """
        pass

    def test_000_place_a_lucky_dip_bet_and_complete_lucky_dip_journey(self):
        """
        DESCRIPTION: Place a Lucky dip bet and complete Lucky dip journey
        EXPECTED: User is displayed with Lucky dip Player card
        """
        pass

    def test_000_verify_whether_user_can_view_the_share_option_next_to_player_card_after_got_it_button(self):
        """
        DESCRIPTION: Verify whether user can view the Share option next to Player card after "Got it" button
        EXPECTED: User should be able see share icon for Lucky dip bet
        """
        pass

    def test_000_click_on_share_icon_amp_verify_pop_up_is_displaying_with_a_cms_config_inputs(self):
        """
        DESCRIPTION: Click on share icon &amp; Verify pop-up is displaying with a CMS config inputs.
        EXPECTED: User should be able to see pop-up with a CMS config inputs.eg-odds,stake,date etc.
        """
        pass

    def test_000_verify_share_button_in_pop_up(self):
        """
        DESCRIPTION: Verify share button in pop-up.
        EXPECTED: User should be able to click on share button.
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

    def test_000_verify_preview_page_when_clicking_on_selected_social_app_icon(self):
        """
        DESCRIPTION: Verify preview page when clicking on selected social app icon.
        EXPECTED: User "A"should be able to see whether share card has been sent successfully with a "B" user via selected social app.
        """
        pass

    def test_000_verify_share_card_has_been_sent_to_the_other_user_via_selected_social_app(self):
        """
        DESCRIPTION: Verify share card has been sent to the other user via selected social app.
        EXPECTED: User "B" should be able to see a share card which "A" user has shared.
        """
        pass

    def test_000_verify_that_the_receiving_share_card_should_contain_all_the_details_which_are_selected_by_the_sender(self):
        """
        DESCRIPTION: Verify that the Receiving share card should contain all the details, which are selected by the Sender.
        EXPECTED: The Receiver will be receiving all the share card details that is sent by User
        """
        pass

    def test_000_click_on_share_icon(self):
        """
        DESCRIPTION: Click on share icon
        EXPECTED: Pop up is opened
        """
        pass

    def test_000_verify_cancel_button_in_pop_up(self):
        """
        DESCRIPTION: Verify CANCEL button in pop-up.
        EXPECTED: User should be able to click on CANCEL button.
        """
        pass

    def test_000_verify_user_has_reverted_back_to_the_previous_page(self):
        """
        DESCRIPTION: Verify user has reverted back to the previous page.
        EXPECTED: User should be able to see the previous page successfully.
        """
        pass

    def test_000_verify_share_button_in_pop_up(self):
        """
        DESCRIPTION: Verify share button in pop-up
        EXPECTED: User should be able to click on share button.
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

    def test_000_verify_the_player_card_has_been_sent_to_the_other_user_via_selected_social_app(self):
        """
        DESCRIPTION: Verify the player card has been sent to the other user via selected social app.
        EXPECTED: User "B" should be able to see a share card which "A" user has shared along with selected preferences
        """
        pass

    def test_000_verify_that_the_receiving_share_card_should_contain_all_the_details_which_are_selected_by_the_sender(self):
        """
        DESCRIPTION: Verify that the Receiving share card should contain all the details, which are selected by the Sender.
        EXPECTED: The Receiver will be receiving all the share card details that is sent by User
        """
        pass
