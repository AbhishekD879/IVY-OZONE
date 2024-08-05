import pytest
from tests.base_test import vtest
from tests.Common import Common


# @pytest.mark.tst2 # question enginee not configured in qa2
# @pytest.mark.stg2
@pytest.mark.qe_crl_prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.question_engine
@vtest
class Test_C57732154_Verify_the_view_and_navigation_of_the_Splash_Page_when_user_havent_played_a_current_game(Common):
    """
    TR_ID: C57732154
    NAME: Verify the view and navigation of the Splash Page when user haven't played a current game
    DESCRIPTION: This test case verifies:
    DESCRIPTION: - the view of the Splash Page when User haven't played a current game.
    DESCRIPTION: - Start page navigation for a 'PLAY NOW FOR FREE' CTA1 button.
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds,
    PRECONDITIONS: 1. The user is logged in https://m.ladbrokes.com
    PRECONDITIONS: 2. The user is logged in to CMS
    PRECONDITIONS: 3. User opens previously created Quiz
    PRECONDITIONS: 4. Content for Splash page configured before
    PRECONDITIONS: 5. User haven't played the current game yet
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. The game is configured in the CMS.
        PRECONDITIONS: 2. The User is logged in.
        PRECONDITIONS: 3. User opens previously created Quiz
        PRECONDITIONS: 4. Content for Splash page configured before
        PRECONDITIONS: 5. User haven't played the current game yet
        """
        splash_pages = self.cms_config.get_qe_splash_page()
        self.__class__.splash_page = next((page for page in splash_pages if page.get('title') == "Autotest_Splash_Page"))
        question = self.create_question_engine_quiz()
        self.__class__.expected_first_question = question['firstQuestion']['text']
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)
        self.navigate_to_page('footballsuperseries')

    def test_001_tap_on_banner_or_link_to_launch_a_quiz(self):
        """
        DESCRIPTION: Tap on banner or link to launch a quiz
        EXPECTED: - Splash page displayed and correctly designed according to:
        EXPECTED: https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a/screen/5d4d962ddc6f4e9be56f646c
        EXPECTED: - Button with the text 'Play now for free' displayed (Retrieved from CMS > CTA1)
        """
        self.assertEqual(self.site.question_engine.strap_line_text, self.splash_page['strapLine'],
                         msg=f'Actual strap line text text : "{self.site.question_engine.strap_line_text}"'
                             f'is not as expected : "{ self.splash_page["strapLine"]}"')
        self.assertEqual(self.site.question_engine.footer_text, self.splash_page['footerText'],
                         msg=f'Actual footer text text : "{self.site.question_engine.footer_text}"'
                             f'is not as expected : "{self.splash_page["footerText"]}"')
        self.assertTrue(self.site.question_engine.has_cta_button(), msg='"Play now for free" button is not displayed')
        actual_playnowforfree_button = self.site.question_engine.cta_button.text
        self.assertEqual(actual_playnowforfree_button, self.splash_page['playForFreeCTAText'],
                         msg=f'Actual "Play now for free" button text : "{actual_playnowforfree_button}"'
                             f'is not as expected : "{self.splash_page["playForFreeCTAText"]}"')

    def test_002_tap_on_the_play_now_for_free_cta1_button(self):
        """
        DESCRIPTION: Tap on the 'Play now for free' CTA1 button.
        EXPECTED: The User is navigated to the first question page.
        """
        self.site.question_engine.cta_button.click()
        questions = list(self.site.quiz_home_page.question_container.items_as_ordered_dict.values())
        self.assertTrue(questions, msg='Questions are not displayed')
        actual_first_question = questions[0].question_header.text
        self.assertEqual(actual_first_question, self.expected_first_question,
                         msg=f'Actual first question: "{actual_first_question}"'
                             f'is not as expected first question: "{self.expected_first_question}"')
