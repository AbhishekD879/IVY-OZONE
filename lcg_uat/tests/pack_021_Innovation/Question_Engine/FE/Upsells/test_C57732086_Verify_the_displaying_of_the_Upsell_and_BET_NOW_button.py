import pytest
from time import sleep
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.qe_crl_prod
# @pytest.mark.hl
# @pytest.mark.tst2  # QuestionEngine is not configured under qa2
# @pytest.mark.stg2
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.question_engine
@pytest.mark.other
@vtest
class Test_C57732086_Verify_the_displaying_of_the_Upsell_and_BET_NOW_button(BaseBetSlipTest):
    """
    TR_ID: C57732086
    NAME: Verify the displaying of the Upsell and 'BET NOW' button
    DESCRIPTION: This test case verifies the displaying of the Upsell and 'BET NOW' button.
    PRECONDITIONS: 1. The Upsell is configured in the CMS.
    PRECONDITIONS: 2. The current Event has not started yet.
    PRECONDITIONS: 3. The Quiz is configured in the CMS.
    PRECONDITIONS: 4. The User is logged in.
    PRECONDITIONS: 5. The User has not played a Quiz yet.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. The Upsell is configured in the CMS.
        PRECONDITIONS: 2. The current Event has not started yet.
        PRECONDITIONS: 3. The Quiz is configured in the CMS.
        PRECONDITIONS: 4. The User is logged in.
        PRECONDITIONS: 5. The User has not played a Quiz yet.
        """
        event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
        outcomes = next((market['market']['children'] for market in event['event']['children']
                         if market['market'].get('children')), None)
        if outcomes is None:
            raise SiteServeException('There are no available outcomes')
        selection_ids = [i['outcome']['id'] for i in outcomes]
        quiz = self.create_question_engine_quiz()
        quiz_id = quiz['id']
        quiz_title = quiz['title']
        selection = quiz['upsell']['options']['11;21'] = selection_ids[0]
        self.cms_config.update_question_engine_quiz(quiz_id, quiz_title, selection_1=selection, payload=quiz)
        user_name = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=user_name)
        self.site.wait_content_state('homepage')
        self.navigate_to_page('footballsuperseries')

    def test_001_tap_on_the_play_now_for_free_button(self):
        """
        DESCRIPTION: Tap on the 'Play Now For Free' button.
        EXPECTED: The User is redirected to the 1st Question page.
        """
        self.assertTrue(self.site.question_engine.has_cta_button(), msg=f'CTA button is not displayed')
        self.site.question_engine.cta_button.click()
        self.__class__.questions = list(self.site.quiz_home_page.question_container.items_as_ordered_dict.values())
        self.assertTrue(self.questions, msg=f'Questions are not displayed')

    def test_002_select_any_answer(self):
        """
        DESCRIPTION: Select any answer.
        EXPECTED: The answer is highlighted with yellow colour.
        EXPECTED: The User is redirected to the next Question page.
        """
        for question in self.questions:
            options = list(question.answer_options.items_as_ordered_dict.values())
            options[0].click()
            sleep(4)  # time required to swipe to next question
            self.site.wait_splash_to_hide(timeout=10)

    def test_003_repeat_the_2nd_step_until_the_last_question_page_is_reached(self):
        """
        DESCRIPTION: Repeat the 2nd step until the last Question page is reached.
        EXPECTED: The answer is highlighted with yellow colour.
        EXPECTED: The User is redirected to the last Question page.
        """
        # Covered in Step# 2

    def test_004_select_any_answer(self):
        """
        DESCRIPTION: Select any answer.
        EXPECTED: The 'Confirm your selections!' pop-up is opened.
        """
        # Covered in Step# 2

    def test_005_tap_on_the_submit_button(self):
        """
        DESCRIPTION: Tap on the 'Submit' button.
        EXPECTED: 1. The 'Confirm your selections!' pop-up is closed.
        EXPECTED: 2. The User is navigated to the Latest tab of the Results page.
        EXPECTED: 3. The Upsell 'card' is displayed with:
        EXPECTED: - the 'BET NOW' CTA
        EXPECTED: - signposting as per the attached design
        EXPECTED: Example:
        EXPECTED: - Header: "Premier League Arsenal V Watford".
        EXPECTED: - Upsell description : "Arsenal to Win and Both teams to score".
        EXPECTED: - Ods & Return calculation : "A£10 bet returns £60".
        EXPECTED: - Signposting: n/a.
        EXPECTED: - CTA: "BET NOW".
        EXPECTED: https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a/screen/5d4d962a1db0449b1282fd08
        """
        self.site.quiz_page_popup.submit_button.click()
        sleep(1)
        self.assertTrue(self.site.quiz_results_page.tab_content.upsell.upsell_title,
                        msg=f'Upsell title is not displayed')
        self.assertTrue(self.site.quiz_results_page.tab_content.upsell.upsell_caption,
                        msg=f'Upsell caption is not displayed')
        self.assertTrue(self.site.quiz_results_page.tab_content.upsell.bet_button, msg=f'BET button is not displayed')

    def test_006_tap_on_the_bet_now_button(self):
        """
        DESCRIPTION: Tap on the 'BET NOW' button.
        EXPECTED: The User is redirected to the Betslip page with a possibility to place a bet.
        """
        self.site.quiz_results_page.tab_content.upsell.bet_button.click()
        self.site.betslip._load_complete()
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section, msg='Betslip Singles section is not displayed.')
