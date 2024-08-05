import pytest
from tests.base_test import vtest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from time import sleep


# @pytest.mark.tst2  # question engine is not configured in qa2
# @pytest.mark.stg2
@pytest.mark.qe_crl_prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.question_engine
@pytest.mark.desktop
@pytest.mark.other
@vtest
class Test_C58668196_Verify_the_GA_tracking_of_the_Previous_tab(BaseDataLayerTest):
    """
    TR_ID: C58668196
    NAME: Verify the GA tracking of the Previous tab
    DESCRIPTION: This test case verifies the Google Analytics tracking of the Previous tab elements.
    PRECONDITIONS: For more information please consider https://confluence.egalacoral.com/display/SPI/GA+TRACKING+CORRECT+4
    PRECONDITIONS: 1. The Quiz is configured in the CMS.
    PRECONDITIONS: 2. Open the Correct4 https://phoenix-invictus.coral.co.uk/correct4.
    PRECONDITIONS: 3. The User is logged in.
    PRECONDITIONS: 4. The User has already played a Quiz.
    PRECONDITIONS: 5. Open DevTools in browser.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. The Quiz is configured in the CMS.
        PRECONDITIONS: 2. Open the website https://phoenix-invictus.coral.co.uk/.
        PRECONDITIONS: 3. The User is logged in.
        PRECONDITIONS: 4. The User has already played a Quiz.
        """
        quiz = self.create_question_engine_quiz()
        self.assertTrue(quiz, msg='Quiz is not configured in the CMS')
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username, async_close_dialogs=False)

        self.navigate_to_page('footballsuperseries')
        self.site.wait_splash_to_hide(timeout=10)
        self.assertTrue(self.site.question_engine.has_cta_button(), msg='"Play now for free" button is not displayed')

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

    def test_001_proceed_to_the_results_page(self):
        """
        DESCRIPTION: Proceed to the Results page.
        EXPECTED: The Results page is opened.
        """
        self.site.wait_splash_to_hide(timeout=10)
        self.assertTrue(self.site.quiz_results_page.latest_tab, msg=f'Quiz not submitted successfully')

    def test_002_select_the_previous_tabenter_datalayer_in_the_console(self):
        """
        DESCRIPTION: Select the 'Previous' tab.
        DESCRIPTION: Enter 'dataLayer' in the console.
        EXPECTED: The 'Previous' tab is opened.
        EXPECTED: The following code is present in the console for Coral:
        EXPECTED: { event: "trackEvent",
        EXPECTED: eventAction: "Previous",
        EXPECTED: eventCategory: "Correct4",
        EXPECTED: eventLabel: "none" },
        EXPECTED: { event: “trackPageview”​
        EXPECTED: virtualUrl: “/correct4/previous-quiz”​ }
        EXPECTED: The following code is present in the console for Ladbrokes:
        EXPECTED: { event: "trackEvent",
        EXPECTED: eventAction: "Previous",
        EXPECTED: eventCategory: "{SourceId}",
        EXPECTED: eventLabel: "none" },
        EXPECTED: { event: “trackPageview”​
        EXPECTED: virtualUrl: “/correct4/previous-quiz”​ }
        """
        self.site.quiz_results_page.previous_tab.click()
        sleep(1)
        actual_response = self.get_data_layer_specific_object(object_key='event',
                                                              object_value='trackEvent')
        expected_response = {'event': "trackEvent",
                             'eventAction': 'Previous',
                             'eventCategory': "Footballsuperseries",
                             'eventLabel': "none"}
        self.compare_json_response(actual_response, expected_response)

        actual_response = self.get_data_layer_specific_object(object_key='event',
                                                              object_value='trackPageview')
        expected_response = {'event': "trackPageview",
                             'virtualUrl': '/footballsuperseries/previous-quiz'}
        self.compare_json_response(actual_response, expected_response)

    def test_003_select_the_latest_tabenter_datalayer_in_the_console(self):
        """
        DESCRIPTION: Select the 'Latest' tab.
        DESCRIPTION: Enter 'dataLayer' in the console.
        EXPECTED: The 'Latest' tab is opened.
        EXPECTED: The following code is present in the console for Coral:
        EXPECTED: { event: "trackEvent",
        EXPECTED: eventAction: "Latest",
        EXPECTED: eventCategory: "Correct4",
        EXPECTED: eventLabel: "none" },
        EXPECTED: { event: “trackPageview”​
        EXPECTED: virtualUrl: “/correct4/latest-quiz”​ }
        EXPECTED: The following code is present in the console for Ladbrokes:
        EXPECTED: { event: "trackEvent",
        EXPECTED: eventAction: "Latest",
        EXPECTED: eventCategory: "{SourceId}",
        EXPECTED: eventLabel: "none" },
        EXPECTED: { event: “trackPageview”​
        EXPECTED: virtualUrl: “/correct4/latest-quiz”​ }
        """
        self.site.quiz_results_page.latest_tab.click()
        sleep(1)
        actual_response = self.get_data_layer_specific_object(object_key='event',
                                                              object_value='trackEvent')
        expected_response = {'event': "trackEvent",
                             'eventAction': 'Latest',
                             'eventCategory': "Footballsuperseries",
                             'eventLabel': "none"}
        self.compare_json_response(actual_response, expected_response)

        actual_response = self.get_data_layer_specific_object(object_key='event',
                                                              object_value='trackPageview')
        expected_response = {'event': "trackPageview",
                             'virtualUrl': '/footballsuperseries/latest-quiz'}
        self.compare_json_response(actual_response, expected_response)

    def test_004_select_the_previous_tab(self):
        """
        DESCRIPTION: Select the 'Previous' tab.
        EXPECTED: The 'Previous' tab is opened.
        """
        self.site.quiz_results_page.previous_tab.click()
        sleep(1)

    def test_005_tap_on_the_view_game_summary_to_expand_the_boxenter_datalayer_in_the_console(self):
        """
        DESCRIPTION: Tap on the ‘View Game Summary’ to expand the box.
        DESCRIPTION: Enter 'dataLayer' in the console.
        EXPECTED: The box is expanded.
        EXPECTED: The following code is present in the console for Coral:
        EXPECTED: { event: "trackEvent",
        EXPECTED: eventCategory: "Correct4",
        EXPECTED: eventAction: "View Game Summary",
        EXPECTED: eventLabel: "Expand" }
        EXPECTED: The following code is present in the console for Ladbrokes:
        EXPECTED: { event: "trackEvent",
        EXPECTED: eventCategory: "/{SourceId}",
        EXPECTED: eventAction: "View Game Summary",
        EXPECTED: eventLabel: "Expand" }
        """
        try:
            if self.site.quiz_results_page.has_results_summary():
                self.site.quiz_results_page.view_game_summary.click()
                actual_response = self.get_data_layer_specific_object(object_key='event',
                                                                      object_value='trackEvent')
                expected_response = {'event': "trackEvent",
                                     'eventAction': 'View Game Summary',
                                     'eventCategory': "Footballsuperseries",
                                     'eventLabel': "Expand"}
                self.compare_json_response(actual_response, expected_response)
        except Exception:
            self._logger.info(f'No previous results found')

    def test_006_tap_on_the_view_game_summary_to_collapse_the_boxenter_datalayer_in_the_console(self):
        """
        DESCRIPTION: Tap on the ‘View Game Summary’ to collapse the box.
        DESCRIPTION: Enter 'dataLayer' in the console.
        EXPECTED: The box is collapsed.
        EXPECTED: The following code is present in the console for Coral:
        EXPECTED: { event: "trackEvent",
        EXPECTED: eventCategory: "Correct4",
        EXPECTED: eventAction: "View Game Summary",
        EXPECTED: eventLabel: "Collapse" }
        EXPECTED: The following code is present in the console for Ladbrokes:
        EXPECTED: { event: "trackEvent",
        EXPECTED: eventCategory: "/{SourceId}",
        EXPECTED: eventAction: "View Game Summary",
        EXPECTED: eventLabel: "Colapse" }
        """
        try:
            if self.site.quiz_results_page.has_results_summary():
                self.site.quiz_results_page.view_game_summary.click()
                actual_response = self.get_data_layer_specific_object(object_key='event',
                                                                      object_value='trackEvent')
                expected_response = {'event': "trackEvent",
                                     'eventAction': 'View Game Summary',
                                     'eventCategory': "Footballsuperseries",
                                     'eventLabel': "Collapse"}
                self.compare_json_response(actual_response, expected_response)
        except Exception:
            self._logger.info(f'No previous results found')

    def test_007_tap_on_the_show_more_buttonenter_datalayer_in_the_console(self):
        """
        DESCRIPTION: Tap on the ‘Show More’ button.
        DESCRIPTION: Enter 'dataLayer' in the console.
        EXPECTED: Additional previous games are displayed.
        EXPECTED: The following code is present in the console for Coral:
        EXPECTED: { event: "trackEvent",
        EXPECTED: eventCategory: "Correct4",
        EXPECTED: eventAction: "View Historic Games",
        EXPECTED: eventLabel: "Show More" }
        EXPECTED: The following code is present in the console for Ladbrokes:
        EXPECTED: { event: "trackEvent",
        EXPECTED: eventCategory: "{SourceId}",
        EXPECTED: eventAction: "View Historic Games",
        EXPECTED: eventLabel: "Show More" }
        """
        # Show More button not displayed
