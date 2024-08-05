import pytest
import tests
from tests.base_test import vtest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from time import sleep


# @pytest.mark.tst2 #QuestionEngine is not configured under qa2
# @pytest.mark.stg2
@pytest.mark.qe_crl_prod
@pytest.mark.question_engine
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.other
@vtest
class Test_C58668195_Verify_the_GA_tracking_of_the_Submit_pop_up(BaseDataLayerTest):
    """
    TR_ID: C58668195
    NAME: Verify the GA tracking of the Submit pop-up
    DESCRIPTION: This test case verifies the Google Analytics tracking of the Submit pop-up.
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
                                       'virtualUrl': '/footballsuperseries/question1'
                                       }

    def verify_confirm_your_selections_dataLayer(self):
        expected_response_playnow_coral = {'event': 'trackEvent',
                                           'eventAction': 'Confirm Your Selections',
                                           'eventCategory': 'Footballsuperseries',
                                           'eventLabel': 'Go Back & Edit'
                                           }
        actual_response = self.get_data_layer_specific_object(object_key='event', object_value='trackEvent')
        self.assertEqual(expected_response_playnow_coral.get("event"), actual_response.get("event"),
                         msg=f'Expected event value "{expected_response_playnow_coral.get("event")}" is not '
                             f'same as actual event value "{actual_response.get("event")}"')
        self.assertEqual(expected_response_playnow_coral.get("eventAction"), actual_response.get("eventAction"),
                         msg=f'Expected eventAction value "{expected_response_playnow_coral.get("eventAction")}" is not '
                             f'same as actual eventAction value "{actual_response.get("eventAction")}"')
        self.assertEqual(expected_response_playnow_coral.get("eventCategory"), actual_response.get("eventCategory"),
                         msg=f'Expected eventCategory value "{expected_response_playnow_coral.get("eventCategory")}" is not '
                             f'same as actual eventCategory value "{actual_response.get("eventCategory")}"')
        self.assertEqual(expected_response_playnow_coral.get("eventLabel"), actual_response.get("eventLabel"),
                         msg=f'Expected eventLabel value "{expected_response_playnow_coral.get("eventLabel")}" is not '
                             f'same as actual eventLabel value "{actual_response.get("eventLabel")}"')

    def verify_event_virtualUrl_dataLayer(self):
        actual_response = self.get_data_layer_specific_object(object_key='event', object_value='trackPageview')
        self.assertEqual(self.expected_response_playnow_coral.get("event"), actual_response.get("event"),
                         msg=f'Expected event value "{self.expected_response_playnow_coral.get("event")}" is not '
                             f'same as actual event value "{actual_response.get("event")}"')
        self.assertEqual(self.expected_response_playnow_coral.get("virtualUrl"), actual_response.get("virtualUrl"),
                         msg=f'Expected virtualUrl value "{self.expected_response_playnow_coral.get("virtualUrl")}" is not '
                             f'same as actual virtualUrl value "{actual_response.get("virtualUrl")}"')

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
        EXPECTED: virtualUrl: “/{sourceId}/question2”​ }
        """
        options = list(self.questions[0].answer_options.items_as_ordered_dict.values())
        options[0].click()
        self.verify_event_virtualUrl_dataLayer()

    def test_003_repeat_step_2_to_reach_the_last_questionenter_datalayer_in_the_console(self):
        """
        DESCRIPTION: Repeat step 2 to reach the last question.
        DESCRIPTION: Enter 'dataLayer' in the console.
        EXPECTED: The following code is present in the console for Coral:
        EXPECTED: { event: "trackPageview",
        EXPECTED: virtualUrl: “/correct4/question{number}”​ }
        EXPECTED: The following code is present in the console for Ladbrokes:
        EXPECTED: { event: "trackPageview",
        EXPECTED: virtualUrl: “/{sourceId}/question{number}”​ }
        """
        sleep(2)
        options = list(self.questions[1].answer_options.items_as_ordered_dict.values())
        options[0].click()
        self.verify_event_virtualUrl_dataLayer()

    def test_004_select_any_answerenter_datalayer_in_the_console(self):
        """
        DESCRIPTION: Select any answer.
        DESCRIPTION: Enter 'dataLayer' in the console.
        EXPECTED: The 'Submit' pop-up is opened.
        EXPECTED: No additional code is present in the console.
        """
        sleep(2)
        options = list(self.questions[2].answer_options.items_as_ordered_dict.values())
        options[0].click()
        self.verify_event_virtualUrl_dataLayer()
        sleep(2)
        options = list(self.questions[3].answer_options.items_as_ordered_dict.values())
        options[0].click()
        self.verify_event_virtualUrl_dataLayer()

    def test_005_click_on_the_go_back__edit_buttonenter_datalayer_in_the_console(self):
        """
        DESCRIPTION: Click on the 'Go Back & Edit' button.
        DESCRIPTION: Enter 'dataLayer' in the console.
        EXPECTED: The following code is present in the console for Coral:
        EXPECTED: { event: "trackEvent",
        EXPECTED: eventAction: "Confirm Your Selections",
        EXPECTED: eventCategory: "Correct4",
        EXPECTED: eventLabel: "Go Back & Edit" }
        EXPECTED: The following code is present in the console for Ladbrokes:
        EXPECTED: { event: "trackEvent",
        EXPECTED: eventAction: "Confirm Your Selections",
        EXPECTED: eventCategory: "{SourceId}",
        EXPECTED: eventLabel: "Go Back & Edit" }
        """
        self.site.quiz_page_popup.go_back_edit_button.click()
        self.verify_confirm_your_selections_dataLayer()

    def test_006_repeat_step_3_and_4(self):
        """
        DESCRIPTION: Repeat step 3 and 4.
        EXPECTED: The following code is present in the console for Coral:
        EXPECTED: { event: "trackPageview",
        EXPECTED: virtualUrl: “/correct4/question{number}”​ }
        EXPECTED: The following code is present in the console for Ladbrokes:
        EXPECTED: { event: "trackPageview",
        EXPECTED: virtualUrl: “/{sourceId}/question{number}”​ }
        EXPECTED: The 'Submit' pop-up is opened.
        """
        self.test_002_select_any_answerenter_datalayer_in_the_console()
        self.test_003_repeat_step_2_to_reach_the_last_questionenter_datalayer_in_the_console()
        self.test_004_select_any_answerenter_datalayer_in_the_console()

    def test_007_click_on_the_submit_buttonenter_datalayer_in_the_console(self):
        """
        DESCRIPTION: Click on the 'Submit' button.
        DESCRIPTION: Enter 'dataLayer' in the console.
        EXPECTED: The following code is present in the console for Coral:
        EXPECTED: { event: "trackEvent",
        EXPECTED: eventAction: "Confirm Your Selections",
        EXPECTED: eventCategory: "Correct4",
        EXPECTED: eventLabel: "Submit" }
        EXPECTED: The following code is present in the console for Ladbrokes:
        EXPECTED: { event: "trackEvent",
        EXPECTED: eventAction: "Confirm Your Selections",
        EXPECTED: eventCategory: "{SourceId}",
        EXPECTED: eventLabel: "Submit" }
        """
        self.site.quiz_page_popup.submit_button.click()
        self.verify_confirm_your_selections_dataLayer()
