import pytest
import tests
from tests.base_test import vtest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest


# @pytest.mark.tst2 # question engine is not configured in qa2
# @pytest.mark.stg2
@pytest.mark.qe_crl_prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.question_engine
@pytest.mark.desktop
@vtest
class Test_C58668191_Verify_the_GA_tracking_of_the_Splash_page(BaseDataLayerTest):
    """
    TR_ID: C58668191
    NAME: Verify the GA tracking of the Splash page
    DESCRIPTION: This test case verifies the Google Analytics tracking of the Splash page.
    PRECONDITIONS: For more information please consider https://confluence.egalacoral.com/display/SPI/GA+TRACKING+CORRECT+4
    PRECONDITIONS: 1. The Quiz is configured in the CMS.
    PRECONDITIONS: 2. Open the website https://phoenix-invictus.coral.co.uk/.
    PRECONDITIONS: 3. The User is logged in.
    PRECONDITIONS: 4. The User has not played a Quiz yet.
    PRECONDITIONS: 5. Open DevTools in browser.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. The Quiz is configured in the CMS.
        PRECONDITIONS: 2. Open the website https://phoenix-invictus.coral.co.uk/.
        PRECONDITIONS: 3. The User is logged in.
        """
        quiz = self.create_question_engine_quiz()
        self.assertTrue(quiz, msg='Quiz is not configured in the CMS')
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username, async_close_dialogs=False)

    def test_001_select_correct4_tabenter_datalayer_in_the_console(self):
        """
        DESCRIPTION: Select 'Correct4' tab.
        DESCRIPTION: Enter 'dataLayer' in the console.
        EXPECTED: For Coral:
        EXPECTED: 1. The following code is present in the console:
        EXPECTED: { event: "content-view",
        EXPECTED: screen_name: "/correct4/splash"​ }
        EXPECTED: 2. Make sure that only 1 'content-view' tag is fired.
        EXPECTED: 3. The following code is not present in the console:
        EXPECTED: { event: "trackPageview",
        EXPECTED: page: "/correct4/splash" }
        EXPECTED: For Ladbrokes:
        EXPECTED: 1. The following code is present in the console:
        EXPECTED: { event: "content-view",
        EXPECTED: screen_name: "/{sourceId}/splash"​ }
        EXPECTED: 2. Make sure that only 1 'content-view' tag is fired.
        EXPECTED: 3. The following code is not present in the console:
        EXPECTED: { event: "trackPageview",
        EXPECTED: page: "/{sourceId}/splash" }
        """
        self.navigate_to_page('footballsuperseries')
        actual_response = self.get_data_layer_specific_object(object_key='event', object_value='content-view')
        url = self.device.get_current_url()
        path = url.replace('https://%s' % tests.HOSTNAME, '')
        expected_response = {'event': 'content-view',
                             'screen_name': path}
        self.compare_json_response(actual_response, expected_response)
        res = self.get_data_layer_objects_count(object_key='event', object_value='trackPageview')
        self.assertEqual(0, res, msg='trackPageview event present in console log')

    def test_002_click_on_the_cta_buttonenter_datalayer_in_the_console(self):
        """
        DESCRIPTION: Click on the CTA button.
        DESCRIPTION: Enter 'dataLayer' in the console.
        EXPECTED: The following code is present in the console for Coral:
        EXPECTED: { event: "trackEvent",
        EXPECTED: eventCategory’: "Correct4"
        EXPECTED: eventAction: "{CTA NAME}" //e.g. "Play Now For Free", "See Your Selections", "See Previous Games", "Login To View"
        EXPECTED: eventLabel: "none" }
        EXPECTED: The following code is present in the console for Ladbrokes:
        EXPECTED: { event: "trackEvent",
        EXPECTED: eventCategory’: "{SourceId}"
        EXPECTED: eventAction: "{CTA NAME}" //e.g. "Play Now For Free", "See Your Selections", "See Previous Games", "Login To View"
        EXPECTED: eventLabel: "none" }
        """
        self.assertTrue(self.site.question_engine.has_cta_button(), msg=f'cta button is not displayed')
        playnowforfree_button = self.site.question_engine.cta_button.text
        self.site.question_engine.cta_button.click()
        actual_response = self.get_data_layer_specific_object(object_key='eventCategory',
                                                              object_value='Footballsuperseries')
        expected_response = {'event': "trackEvent",
                             'eventAction': playnowforfree_button,
                             'eventCategory': "Footballsuperseries",
                             'eventLabel': "none"}
        self.compare_json_response(actual_response, expected_response)

    def test_003_click_on_the_back_arrow_button_on_the_mobile(self):
        """
        DESCRIPTION: Click on the Back arrow button on the mobile.
        EXPECTED: The Exit pop-up is opened.
        """
        if self.device_type == 'mobile':
            self.site.question_engine.quick_links_page.back_button.click()
        else:
            self.site.question_engine.exit_button.click()

    def test_004_click_on_the_exit_game_button(self):
        """
        DESCRIPTION: Click on the 'Exit game' button.
        EXPECTED: The Exit pop-up is closed.
        EXPECTED: The User is redirected to the Splash page.
        """
        self.site.quiz_page_popup.has_quiz_exit_popup()
        self.site.quiz_page_popup.exit_quiz_popup.leave_button.click()
        self.site.wait_content_state("HomePage")

    def test_005_click_on_the_x_icon_on_the_mobileenter_datalayer_in_the_console(self):
        """
        DESCRIPTION: Click on the 'X' icon on the mobile.
        DESCRIPTION: Enter 'dataLayer' in the console.
        EXPECTED: The following code is present in the console for Coral:
        EXPECTED: { event: "trackEvent",
        EXPECTED: eventCategory: "Correct4",
        EXPECTED: eventAction: "Exit",
        EXPECTED: eventLabel: "none" }
        EXPECTED: The following code is present in the console for Ladbrokes:
        EXPECTED: { event: "trackEvent",
        EXPECTED: eventCategory: "{SourceId}",
        EXPECTED: eventAction: "Exit",
        EXPECTED: eventLabel: "none" }
        """
        actual_response = self.get_data_layer_specific_object(object_key='eventAction', object_value='Exit')
        expected_response = {'event': 'trackEvent',
                             'eventCategory': 'Footballsuperseries',
                             'eventAction': 'Exit',
                             'eventLabel': 'none'}
        self.compare_json_response(actual_response, expected_response)
