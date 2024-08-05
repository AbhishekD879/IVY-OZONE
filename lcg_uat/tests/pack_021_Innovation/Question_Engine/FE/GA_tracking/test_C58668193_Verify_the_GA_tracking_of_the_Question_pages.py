import pytest
import tests
from tests.base_test import vtest
from time import sleep
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest


# @pytest.mark.tst2 #QuestionEngine is not configured under qa2
# @pytest.mark.stg2
@pytest.mark.qe_crl_prod
# @pytest.mark.hl
@pytest.mark.question_engine
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C58668193_Verify_the_GA_tracking_of_the_Question_pages(BaseDataLayerTest):
    """
    TR_ID: C58668193
    NAME: Verify the GA tracking of the Question pages
    DESCRIPTION: This test case verifies the Google Analytics tracking of the the Question pages.
    PRECONDITIONS: For more information please consider https://confluence.egalacoral.com/display/SPI/GA+TRACKING+CORRECT+4
    PRECONDITIONS: 1. The Quiz is configured in the CMS.
    PRECONDITIONS: 2. Open the Correct4 https://phoenix-invictus.coral.co.uk/correct4.
    PRECONDITIONS: 3. The User is logged in.
    PRECONDITIONS: 4. The User has not played a Quiz yet.
    PRECONDITIONS: 5. Open DevTools in browser.
    """
    keep_browser_open = True
    device_name = tests.desktop_default
    expected_response_playnow_coral = {'event': 'trackPageview',
                                       'virtualUrl': 'footballsuperseries/question'
                                       }

    def verify_event_virtualUrl_dataLayer(self):
        actual_response = self.get_data_layer_specific_object(object_key='event', object_value='trackPageview')
        self.assertEqual(self.expected_response_playnow_coral.get("event"), actual_response.get("event"),
                         msg=f'Expected event value "{self.expected_response_playnow_coral.get("event")}" is not '
                             f'same as actual event value "{actual_response.get("event")}"')
        self.assertIn(self.expected_response_playnow_coral.get("virtualUrl"), actual_response.get("virtualUrl"),
                      msg=f'Expected virtualUrl value "{self.expected_response_playnow_coral.get("virtualUrl")}" is not '
                          f'in actual virtualUrl value "{actual_response.get("virtualUrl")}"')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Login with the created User and Create the QUIZ in CMS
        """
        self.create_question_engine_quiz(pop_up=True)
        user_name = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=user_name)
        self.navigate_to_page('footballsuperseries')

    def test_001_click_on_the_play_now_for_free_buttonenter_datalayer_in_the_console(self):
        """
        DESCRIPTION: Click on the 'Play now for free' button.
        DESCRIPTION: Enter 'dataLayer' in the console.
        EXPECTED: The following code is present in the console for Coral:
        EXPECTED: { event: "trackPageview",
        EXPECTED: virtualUrl: “/correct4/question1”​ }
        EXPECTED: The following code is present in the console for Ladbrokes:
        EXPECTED: { event: "trackPageview",
        EXPECTED: virtualUrl: “/{sourceId}/question1”​ }
        """
        self.assertTrue(self.site.question_engine.has_cta_button(), msg=f'cta button is not displayed')
        self.site.question_engine.cta_button.click()
        self.__class__.questions = list(self.site.quiz_home_page.question_container.items_as_ordered_dict.values())
        self.assertTrue(self.questions, msg=f' questions are not displayed')
        self.verify_event_virtualUrl_dataLayer()

    def test_002_select_any_answerenter_datalayer_in_the_console(self):
        """
        DESCRIPTION: Select any answer.
        DESCRIPTION: Enter 'dataLayer' in the console.
        EXPECTED: The following code is present in the console for Coral:
        EXPECTED: { event: "trackPageview",
        EXPECTED: virtualUrl: “/correct4/question2”​ }
        EXPECTED: The following code is present in the console for Ladbrokes:
        EXPECTED: { event: "trackPageview",
        EXPECTED: virtualUrl: "/{sourceId}/question2" }
        """
        # question1 is present always in virtualUrl
        options = list(self.questions[0].answer_options.items_as_ordered_dict.values())
        options[0].click()
        self.verify_event_virtualUrl_dataLayer()

    def test_003_select_any_answerenter_datalayer_in_the_console(self):
        """
        DESCRIPTION: Select any answer.
        DESCRIPTION: Enter 'dataLayer' in the console.
        EXPECTED: The following code is present in the console for Coral:
        EXPECTED: { event: "trackPageview",
        EXPECTED: virtualUrl: “/correct4/question3”​ }
        EXPECTED: The following code is present in the console for Ladbrokes:
        EXPECTED: { event: "trackPageview",
        EXPECTED: virtualUrl: "/{sourceId}/question3" }
        """
        sleep(2)
        options = list(self.questions[1].answer_options.items_as_ordered_dict.values())
        options[0].click()
        self.verify_event_virtualUrl_dataLayer()

    def test_004_click_on_the_previous_arrow_buttonenter_datalayer_in_the_console(self):
        """
        DESCRIPTION: Click on the Previous arrow button.
        DESCRIPTION: Enter 'dataLayer' in the console.
        EXPECTED: The following code is present in the console for Coral:
        EXPECTED: { event: "trackPageview",
        EXPECTED: virtualUrl: “/correct4/question2”​ }
        EXPECTED: The following code is present in the console for Ladbrokes:
        EXPECTED: { event: "trackPageview",
        EXPECTED: virtualUrl: "/{sourceId}/question2" }
        """
        self.site.quiz_home_page.quiz_left_swipe_overlay.click()
        self.verify_event_virtualUrl_dataLayer()

    def test_005_click_on_the_next_arrow_buttonenter_datalayer_in_the_console(self):
        """
        DESCRIPTION: Click on the Next arrow button.
        DESCRIPTION: Enter 'dataLayer' in the console.
        EXPECTED: The following code is present in the console for Coral:
        EXPECTED: { event: "trackPageview",
        EXPECTED: virtualUrl: “/correct4/question3”​ }
        EXPECTED: The following code is present in the console for Ladbrokes:
        EXPECTED: { event: "trackPageview",
        EXPECTED: virtualUrl: "/{sourceId}/question3" }
        """
        self.site.quiz_home_page.quiz_right_swipe_overlay.click()
        self.verify_event_virtualUrl_dataLayer()
