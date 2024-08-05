import pytest
from tests.base_test import vtest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest


# @pytest.mark.tst2 # Question engine is not configured in qa2
# @pytest.mark.stg2
@pytest.mark.qe_crl_prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.question_engine
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C58668194_Verify_the_GA_tracking_of_the_Exit_pop_up(BaseDataLayerTest):
    """
    TR_ID: C58668194
    NAME: Verify the GA tracking of the Exit pop-up
    DESCRIPTION: This test case verifies the Google Analytics tracking of the Exit pop-up.
    PRECONDITIONS: For more information please consider https://confluence.egalacoral.com/display/SPI/GA+TRACKING+CORRECT+4
    PRECONDITIONS: 1. The Quiz is configured in the CMS.
    PRECONDITIONS: 2. Open the Correct4 https://phoenix-invictus.coral.co.uk/correct4.
    PRECONDITIONS: 3. The User is logged in.
    PRECONDITIONS: 4. The User has not played a Quiz yet.
    PRECONDITIONS: 5. Open DevTools in browser.
    """
    keep_browser_open = True
    expected_response_playnow_coral = {'event': 'trackPageview',
                                       'virtualUrl': '/footballsuperseries/question1'
                                       }

    def test_000_preconditions(self):
        """
        DESCRIPTION: Login with the created User and Create the QUIZ in CMS
        """
        self.create_question_engine_quiz()
        user_name = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=user_name, async_close_dialogs=False)
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
        actual_response = self.get_data_layer_specific_object(object_key='event', object_value='trackPageview')
        self.assertEqual(self.expected_response_playnow_coral.get("event"), actual_response.get("event"),
                         msg=f'Expected event value "{self.expected_response_playnow_coral.get("event")}" is not '
                             f'same as actual event value "{actual_response.get("event")}"')
        self.assertEqual(self.expected_response_playnow_coral.get("virtualUrl"), actual_response.get("virtualUrl"),
                         msg=f'Expected virtualUrl value "{self.expected_response_playnow_coral.get("virtualUrl")}" is not '
                             f'same as actual virtualUrl value "{actual_response.get("virtualUrl")}"')

    def test_002_click_on_the_exit_button_on_the_desktop__x_icon_on_the_mobileenter_datalayer_in_the_console(self):
        """
        DESCRIPTION: Click on the 'Exit' button on the Desktop / 'X' icon on the mobile.
        DESCRIPTION: Enter 'dataLayer' in the console.
        EXPECTED: No additional code is present in the console.
        """
        if self.device_type == 'mobile':
            self.site.question_engine.quick_links_page.back_button.click()
            self.assertTrue(self.site.quiz_page_popup.has_quiz_exit_popup(expected_result=True),
                            msg='Exit pop-up is not displayed')
        else:
            self.site.question_engine.exit_button.click()

    def test_003_click_on_the_keep_playing_buttonenter_datalayer_in_the_console(self):
        """
        DESCRIPTION: Click on the 'Keep playing' button.
        DESCRIPTION: Enter 'dataLayer' in the console.
        EXPECTED: The following code is present in the console for Coral:
        EXPECTED: { event: "trackEvent",
        EXPECTED: eventAction: "Exit - Are You Sure?",
        EXPECTED: eventCategory: "Correct4",
        EXPECTED: eventLabel: "Keep Playing" }
        EXPECTED: The following code is present in the console for Ladbrokes:
        EXPECTED: { event: "trackEvent",
        EXPECTED: eventAction: "Exit - Are You Sure?",
        EXPECTED: eventCategory: "{SourceId}",
        EXPECTED: eventLabel: "Keep Playing" }
        """
        self.site.quiz_page_popup.exit_quiz_popup.keep_playing_button.click()
        actual_response = self.get_data_layer_specific_object(object_key='eventCategory',
                                                              object_value='Footballsuperseries')
        expected_response = {'event': "trackEvent",
                             'eventAction': "Exit - Are You Sure?",
                             'eventCategory': "Footballsuperseries",
                             'eventLabel': "Keep Playing"}
        self.compare_json_response(actual_response, expected_response)

    def test_004_click_on_the_exit_button_on_the_desktop__x_icon_on_the_mobileenter_datalayer_in_the_console(self):
        """
        DESCRIPTION: Click on the 'Exit' button on the Desktop / 'X' icon on the mobile.
        DESCRIPTION: Enter 'dataLayer' in the console.
        EXPECTED: No additional code is present in the console.
        """
        if self.device_type == 'mobile':
            self.site.question_engine.quick_links_page.back_button.click()
            self.assertTrue(self.site.quiz_page_popup.has_quiz_exit_popup(expected_result=True),
                            msg='Exit pop-up is not displayed')
        else:
            self.site.question_engine.exit_button.click()

    def test_005_click_on_the_exit_game_buttonenter_datalayer_in_the_console(self):
        """
        DESCRIPTION: Click on the 'Exit game' button.
        DESCRIPTION: Enter 'dataLayer' in the console.
        EXPECTED: The following code is present in the console for Coral:
        EXPECTED: { event: "trackEvent",
        EXPECTED: eventAction: "Exit - Are You Sure?",
        EXPECTED: eventCategory: "Correct4",
        EXPECTED: eventLabel: "Exit Game" }
        EXPECTED: The following code is present in the console for Ladbrokes:
        EXPECTED: { event: "trackEvent",
        EXPECTED: eventAction: "Exit - Are You Sure?",
        EXPECTED: eventCategory: "{SourceId}",
        EXPECTED: eventLabel: "Exit Game" }
        """
        self.site.quiz_page_popup.has_quiz_exit_popup()
        self.site.quiz_page_popup.exit_quiz_popup.leave_button.click()
        self.site.wait_content_state("HomePage")
        actual_response = self.get_data_layer_specific_object(object_key='eventAction', object_value='Exit')
        expected_response = {'event': 'trackEvent',
                             'eventCategory': 'Footballsuperseries',
                             'eventAction': 'Exit',
                             'eventLabel': 'none'}
        self.compare_json_response(actual_response, expected_response)
