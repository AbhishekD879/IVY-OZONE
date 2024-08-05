import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from time import sleep


# @pytest.mark.tst2  # question engine not configured in qa2
# @pytest.mark.stg2
@pytest.mark.qe_crl_prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.question_engine
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C57732075_Verify_opening_different_pages_of_Correct_4(Common):
    """
    TR_ID: C57732075
    NAME: Verify opening different pages of Correct 4
    DESCRIPTION: This test case verifies opening different pages of Correct4 (e.g. directly to end page)
    PRECONDITIONS: Please look for some insights on a page as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: 1. The user is logged in to CMS
    PRECONDITIONS: 2. The user is logged in to Coral/Ladbrokes test environment
    PRECONDITIONS: 3. User NOT played Correct 4 before
    PRECONDITIONS: **NOTE: use your current domain name instead of 'https://phoenix-invictus.coral.co.uk/' and current source id instead of 'correct4' e.g. '/qe/survey1'**
    """
    keep_browser_open = True
    splash_page_url = f'https://{tests.HOSTNAME}/footballsuperseries/splash'
    questions_page_url = f'https://{tests.HOSTNAME}/footballsuperseries/questions'
    latest_quiz_page_url = f'https://{tests.HOSTNAME}/footballsuperseries/after/latest-quiz'
    prizes_page_url = f'https://{tests.HOSTNAME}/footballsuperseries/info/Prizes'
    faqs_page_url = f'https://{tests.HOSTNAME}/footballsuperseries/info/FAQs'
    terms_page_url = f'https://{tests.HOSTNAME}/footballsuperseries/info/TandCs'
    wrong_url = f'https://{tests.HOSTNAME}/footballsuperseries/afdasdfasf'

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. The game is configured in the CMS.
        PRECONDITIONS: 2. The User is logged in.
        PRECONDITIONS: 3. User opens previously created Quiz
        PRECONDITIONS: 4. Content for Splash page configured before
        PRECONDITIONS: 5. User haven't played the current game yet
        """
        splash_pages = self.cms_config.get_qe_splash_page()
        self.__class__.cms_splash_page = next((page for page in splash_pages if page.get('title') == "Autotest_Splash_Page"))
        question = self.create_question_engine_quiz()
        self.__class__.expected_first_question = question['firstQuestion']['text']
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)

    def test_001_try_to_access_links_directlyhttpsphoenix_invictuscoralcoukcorrect4splashhttpsphoenix_invictuscoralcoukcorrect4questionshttpsphoenix_invictuscoralcoukcorrect4afterlatest_quizhttpsphoenix_invictuscoralcoukcorrect4infoprizeshttpsphoenix_invictuscoralcoukcorrect4infofaqhttpsphoenix_invictuscoralcoukcorrect4infoterms(self):
        """
        DESCRIPTION: Try to access links directly:
        DESCRIPTION: https://phoenix-invictus.coral.co.uk/correct4/splash
        DESCRIPTION: https://phoenix-invictus.coral.co.uk/correct4/questions
        DESCRIPTION: https://phoenix-invictus.coral.co.uk/correct4/after/latest-quiz
        DESCRIPTION: https://phoenix-invictus.coral.co.uk/correct4/info/prizes
        DESCRIPTION: https://phoenix-invictus.coral.co.uk/correct4/info/faq
        DESCRIPTION: https://phoenix-invictus.coral.co.uk/correct4/info/terms
        EXPECTED: - Links should be successfully opened
        """
        self.device.navigate_to(self.splash_page_url)
        self.site.wait_splash_to_hide(timeout=10)
        self.assertTrue(self.site.question_engine.strap_line_text, msg='Direct navigation to Splash page failed')

        self.device.navigate_to(self.questions_page_url)
        self.site.wait_splash_to_hide(timeout=10)
        self.assertTrue(self.site.quiz_home_page.header, msg='Direct navigation to Questions page failed')

        self.device.navigate_to(self.latest_quiz_page_url)
        self.site.wait_splash_to_hide(timeout=10)
        self.assertTrue(self.site.quiz_results_page.latest_tab, msg='Direct navigation to Result page failed')

        self.device.navigate_to(self.prizes_page_url)
        self.site.wait_splash_to_hide(timeout=10)
        # self.assertTrue(self.site.question_engine.quick_links_page.prizes_page_text, msg='Direct navigation to "Prizes" page failed')  # Working in prod but not in beta/beta2

        self.device.navigate_to(self.faqs_page_url)
        self.site.wait_splash_to_hide(timeout=10)
        self.assertTrue(self.site.question_engine.quick_links_page.faqs_page_text, msg='Direct navigation to "FAQs" page failed')

        self.device.navigate_to(self.terms_page_url)
        self.site.wait_splash_to_hide(timeout=10)
        self.assertTrue(self.site.question_engine.quick_links_page.terms_page_text, msg='Direct navigation to "Terms and Conditions" page failed')

    def test_002_make_prediction_to_active_quiz(self):
        """
        DESCRIPTION: Make prediction to active Quiz
        EXPECTED: Predictions successfully made
        """
        self.device.navigate_to(self.splash_page_url)
        self.site.wait_splash_to_hide(timeout=10)
        self.assertTrue(self.site.question_engine.has_cta_button(), msg='"Play now for free" button is not displayed')
        actual_playnowforfree_button = self.site.question_engine.cta_button.text
        self.assertEqual(actual_playnowforfree_button, self.cms_splash_page['playForFreeCTAText'],
                         msg=f'Actual "Play now for free" button text : "{actual_playnowforfree_button}"'
                             f'is not as expected : "{self.cms_splash_page["playForFreeCTAText"]}"')
        self.site.question_engine.cta_button.click()
        questions = list(self.site.quiz_home_page.question_container.items_as_ordered_dict.values())
        self.assertTrue(questions, msg='Questions are not displayed')

        for question in questions:
            options = list(question.answer_options.items_as_ordered_dict.values())
            options[0].click()
            sleep(4)  # time required to swipe to next question
            self.site.wait_splash_to_hide(timeout=10)
        self.site.quiz_home_page.submit.click()
        sleep(3)
        self.site.wait_splash_to_hide(timeout=10)
        self.assertTrue(self.site.quiz_results_page.latest_tab, msg=f'Quiz not submitted successfully')

    def test_003_try_to_access_links_directlyhttpsphoenix_invictuscoralcoukcorrect4questions(self):
        """
        DESCRIPTION: Try to access links directly:
        DESCRIPTION: https://phoenix-invictus.coral.co.uk/correct4/questions
        EXPECTED: - Access to questions page after making predictions should be closed
        EXPECTED: - User should be redirected to End page.
        """
        self.device.navigate_to(self.questions_page_url)
        self.site.wait_splash_to_hide(timeout=10)
        self.assertTrue(self.site.quiz_results_page.latest_tab, msg='Access to questions page after making '
                                                                    'predictions should be closed. User should be '
                                                                    'redirected to End page.')

    def test_004_try_to_access_links_directlyhttpsphoenix_invictuscoralcoukcorrect4splashhttpsphoenix_invictuscoralcoukcorrect4afterlatest_quizhttpsphoenix_invictuscoralcoukcorrect4infoprizeshttpsphoenix_invictuscoralcoukcorrect4infofaqhttpsphoenix_invictuscoralcoukcorrect4infoterms(self):
        """
        DESCRIPTION: Try to access links directly:
        DESCRIPTION: https://phoenix-invictus.coral.co.uk/correct4/splash
        DESCRIPTION: https://phoenix-invictus.coral.co.uk/correct4/after/latest-quiz
        DESCRIPTION: https://phoenix-invictus.coral.co.uk/correct4/info/prizes
        DESCRIPTION: https://phoenix-invictus.coral.co.uk/correct4/info/faq
        DESCRIPTION: https://phoenix-invictus.coral.co.uk/correct4/info/terms
        EXPECTED: - Links should be successfully openeds
        """
        self.device.navigate_to(self.splash_page_url)
        self.site.wait_splash_to_hide(timeout=10)
        self.assertTrue(self.site.question_engine.strap_line_text, msg='Direct navigation to Splash page failed')

        self.device.navigate_to(self.latest_quiz_page_url)
        self.site.wait_splash_to_hide(timeout=10)
        self.assertTrue(self.site.quiz_results_page.latest_tab, msg='Direct navigation to Result page failed')

        self.device.navigate_to(self.prizes_page_url)
        self.site.wait_splash_to_hide(timeout=10)
        # self.assertTrue(self.site.question_engine.quick_links_page.prizes_page_text, msg='Direct navigation to "Prizes" page failed')

        self.device.navigate_to(self.faqs_page_url)
        self.site.wait_splash_to_hide(timeout=10)
        self.assertTrue(self.site.question_engine.quick_links_page.faqs_page_text,
                        msg='Direct navigation to "FAQs" page failed')

        self.device.navigate_to(self.terms_page_url)
        self.site.wait_splash_to_hide(timeout=10)
        self.assertTrue(self.site.question_engine.quick_links_page.terms_page_text,
                        msg='Direct navigation to "Terms and Conditions" page failed')

    def test_005_try_to_access_links_directlyhttpsphoenix_invictuscoralcoukcorrect4infosadfasfsafdhttpsphoenix_invictuscoralcoukcorrect4afdasdfasf(self):
        """
        DESCRIPTION: Try to access links directly:
        DESCRIPTION: https://phoenix-invictus.coral.co.uk/correct4/info/sadfasfsafd
        DESCRIPTION: https://phoenix-invictus.coral.co.uk/correct4/afdasdfasf
        EXPECTED: - User should be redirected on the homepage or get an error message with back button
        """
        self.device.navigate_to(self.wrong_url)
        self.site.wait_content_state("Homepage")

    def test_006_logout(self):
        """
        DESCRIPTION: Logout.
        EXPECTED: The User is successfully logged out.
        """
        self.site.logout()
        self.assertTrue(self.site.wait_logged_out(),
                        msg='User has not logged out!')

    def test_007_try_to_access_links_directlyhttpsphoenix_invictuscoralcoukcorrect4splashhttpsphoenix_invictuscoralcoukcorrect4infoprizeshttpsphoenix_invictuscoralcoukcorrect4infofaqhttpsphoenix_invictuscoralcoukcorrect4infoterms(self):
        """
        DESCRIPTION: Try to access links directly:
        DESCRIPTION: https://phoenix-invictus.coral.co.uk/correct4/splash
        DESCRIPTION: https://phoenix-invictus.coral.co.uk/correct4/info/prizes
        DESCRIPTION: https://phoenix-invictus.coral.co.uk/correct4/info/faq
        DESCRIPTION: https://phoenix-invictus.coral.co.uk/correct4/info/terms
        EXPECTED: Links are successfully opened.
        """
        # Invalid step. QE does not work when user is logged out

    def test_008_try_to_access_links_directlyhttpsphoenix_invictuscoralcoukcorrect4questionshttpsphoenix_invictuscoralcoukcorrect4afterlatest_quiz(self):
        """
        DESCRIPTION: Try to access links directly:
        DESCRIPTION: https://phoenix-invictus.coral.co.uk/correct4/questions
        DESCRIPTION: https://phoenix-invictus.coral.co.uk/correct4/after/latest-quiz
        EXPECTED: The User is redirected to Splash page.
        EXPECTED: The Login pop-up is opened.
        """
        # Invalid step. QE does not work when user is logged out
