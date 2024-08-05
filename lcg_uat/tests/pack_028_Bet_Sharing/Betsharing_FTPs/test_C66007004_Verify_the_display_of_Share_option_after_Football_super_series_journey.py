import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.qe_crl_prod
@pytest.mark.question_engine
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.adhoc_suite
@pytest.mark.mobile_only
@vtest
class Test_C66007004_Verify_the_display_of_Share_option_after_Football_super_series_journey(Common):
    """
    TR_ID: C66007004
    NAME: Verify the display of Share option after Football super series journey
    DESCRIPTION: This testcase verifies the display of Share option after Football super series journey
    PRECONDITIONS: 1. Bet sharing should be configured in CMS page.
    PRECONDITIONS: 2. Go to CMS-&gt;Bet sharing-&gt;enable.Note: 1. All bet share card details can be configured  and managed via CMS.
    """
    keep_browser_open = True
    device_name = 'iPhone 6 Plus'

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. Bet sharing should be configured in CMS page.
        PRECONDITIONS: 2. Go to CMS-&gt;Bet sharing-&gt;enable.Note: 1. All bet share card details can be configured  and managed via CMS.
        """
        # self.cms_config.delete_quiz('65fd78d379976b25eae84085')
        event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
        event_id = event['event']['id']
        event_name = event['event']['name']
        event_start_time = event['event']['startTime']
        quiz = self.cms_config.check_update_and_create_question_engine_quiz(event_id=event_id, event_name=event_name, start_time=event_start_time, homeTeamName='Arsenal', awayTeamName='Man City')
        self.assertTrue(quiz, msg='Question Engine Quiz not created')
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)

    def test_001_launch_and_login_to_the_application(self):
        """
        DESCRIPTION: Launch and login to the Application
        EXPECTED: User should be able to launch and login to application successfully
        """
        self.navigate_to_page('footballsuperseries')
        self.assertTrue(self.site.question_engine.has_cta_button(), msg=f'cta button is not displayed')
        self.site.question_engine.cta_button.click()
        self.__class__.questions = list(self.site.quiz_home_page.question_container.items_as_ordered_dict.values())
        self.assertTrue(self.questions, msg=f' questions are not displayed')

    def test_002_complete_football_super_series_journey_and_navigate_to_final_screen(self):
        """
        DESCRIPTION: Complete Football super series journey and navigate to final screen
        EXPECTED: User will be displayed with Share option
        """
        pass

    def test_003_verify_share_icon(self):
        """
        DESCRIPTION: Verify Share icon
        EXPECTED: User should be able to see share option
        """
        pass

    def test_004_click_on_share_option(self):
        """
        DESCRIPTION: Click on Share option
        EXPECTED: Then all the available sharing platforms will be displayed. Note: There will be no share card preference pop up in FTP share journey
        """
        pass

    def test_005_verify_share_card_is_displaying_with_a_static_message_and_image_which_are_configured_in_cms(self):
        """
        DESCRIPTION: Verify share card is displaying with a static message and image which are configured in CMS.
        EXPECTED: User should be able to see share card with static message and image
        """
        pass

    def test_006_verify_other_social_app_icons_are_displaying_below_the_image_in_share_card_window(self):
        """
        DESCRIPTION: Verify other social app icon's are displaying below the image in share card window.
        EXPECTED: User should be able to see other social app icon's below the image
        """
        pass

    def test_007_verify_share_card_has_been_sent_to_the_other_user_via_selected_social_app(self):
        """
        DESCRIPTION: Verify share card has been sent to the other user via selected social app.
        EXPECTED: User "B" should be able to see a share card which "A" user has shared.
        """
        pass
