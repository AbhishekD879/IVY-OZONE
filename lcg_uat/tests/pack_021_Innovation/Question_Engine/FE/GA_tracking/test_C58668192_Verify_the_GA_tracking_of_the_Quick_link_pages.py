import pytest
import tests
from tests.base_test import vtest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.utils.waiters import wait_for_result


# @pytest.mark.tst2   # question engine is not configured in qa2
# @pytest.mark.stg2
@pytest.mark.qe_crl_prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.other
@pytest.mark.question_engine
@vtest
class Test_C58668192_Verify_the_GA_tracking_of_the_Quick_link_pages(BaseDataLayerTest):
    """
    TR_ID: C58668192
    NAME: Verify the GA tracking of the Quick link pages
    DESCRIPTION: This test case verifies the Google Analytics tracking of the Splash page.
    PRECONDITIONS: For more information please consider https://confluence.egalacoral.com/display/SPI/GA+TRACKING+CORRECT+4
    PRECONDITIONS: 1. The Quiz is configured in the CMS.
    PRECONDITIONS: 2. Open the Correct4 https://phoenix-invictus.coral.co.uk/correct4.
    PRECONDITIONS: 3. The User is logged in.
    PRECONDITIONS: 4. The User has not played a Quiz yet.
    PRECONDITIONS: 5. Open DevTools in browser.
    """
    keep_browser_open = True
    device_name = tests.desktop_default

    def navigate_to_quick_link_page(self, quick_link):

        self.__class__.quick_links = self.site.question_engine.quicklinks_section.items_as_ordered_dict
        self.assertTrue(self.quick_links, msg='No quick links found on splash page')
        current_url = self.device.get_current_url()
        self.assertTrue(quick_link in list(self.quick_links.keys()),
                        msg=f'Expected quick link "{quick_link}" is not present in actual list of links "{list(self.quick_links.keys())}"')
        self.quick_links[quick_link].click()
        self.assertTrue(wait_for_result(lambda: current_url != self.device.get_current_url()),
                        msg=f'User is still on the splash page after clicking on quick link item')
        self.site.wait_splash_to_hide(timeout=10)
        if quick_link == 'Prizes':
            self.assertTrue(self.site.question_engine.quick_links_page.prizes_page_text,
                            msg='Direct navigation to "Prizes" page failed')
        elif quick_link == 'Frequently Asked Questions':
            self.assertTrue(self.site.question_engine.quick_links_page.faqs_page_text,
                            msg='Direct navigation to "FAQs" page failed')
        elif quick_link == 'Terms and Conditions':
            self.assertTrue(self.site.question_engine.quick_links_page.terms_page_text,
                            msg='Direct navigation to "Terms and Conditions" page failed')

    def test_000_pre_conditions(self):
        """"
        PRECONDITIONS: 1. The user is logged in to CMS
        PRECONDITIONS: 2. The user is logged in to Coral/Ladbrokes test environment
        PRECONDITIONS: 3. The user is on the Splash page
        """
        self.__class__.quiz = self.create_question_engine_quiz()
        self.assertTrue(self.quiz, msg='Quiz is not present')
        source_page_url = self.quiz['sourceId']
        user_name = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(user_name=user_name)
        self.navigate_to_page(name=source_page_url)
        self.assertTrue(self.site.question_engine.has_cta_button(), msg=f'cta button is not displayed')

    def test_001_click_on_the_prizes_buttonenter_datalayer_in_the_console(self):
        """
        DESCRIPTION: Click on the 'Prizes' button.
        DESCRIPTION: Enter 'dataLayer' in the console.
        EXPECTED: For Coral:
        EXPECTED: 1. The following code is present in the console:
        EXPECTED: { event: "trackEvent",
        EXPECTED: eventCategory: "Correct4",
        EXPECTED: eventAction: "Prizes",
        EXPECTED: eventLabel: "none" },
        EXPECTED: { event: "content-view"
        EXPECTED: screen_name: "/correct4/info/prizes" }
        EXPECTED: 2. The following code is not present in the console:
        EXPECTED: { event: “trackPageview”​,
        EXPECTED: page: “/correct4/info/prizes”​ }
        EXPECTED: For Ladbrokes:
        EXPECTED: 1. The following code is present in the console:
        EXPECTED: { event: "trackEvent",
        EXPECTED: eventCategory: "{SourceId}",
        EXPECTED: eventAction: "Prizes",
        EXPECTED: eventLabel: "none"},
        EXPECTED: { event: "content-view"
        EXPECTED: screen_name: "/qe/{sourceId}/info/prizes" }
        EXPECTED: 2. The following code is not present in the console:
        EXPECTED: { event: “trackPageview”​,
        EXPECTED: page: “/{sourceId}/info/prizes”​ }
        """
        self.navigate_to_quick_link_page(quick_link="Prizes")
        expected_track_event = {'event': 'trackEvent', 'eventCategory': 'Footballsuperseries', 'eventAction': 'Prizes',
                                'eventLabel': 'none'}
        actual_track_event_response = self.get_data_layer_specific_object(object_key='event', object_value='trackEvent')
        self.compare_json_response(actual_track_event_response, expected_track_event)

        expected_conten_view = {'event': 'content-view', 'screen_name': '/footballsuperseries/info/Prizes'}
        actual_content_view_response = self.get_data_layer_specific_object(object_key='event',
                                                                           object_value='content-view')
        self.compare_json_response(actual_content_view_response, expected_conten_view)

        try:
            actual_trackPageview_response = self.get_data_layer_specific_object(object_key='event',
                                                                                object_value='trackPageview')
            self.assertTrue(actual_trackPageview_response,
                            msg='trackPageview data is present, whereas it should not be present')
        except Exception:
            pass

    def test_002_click_on_the_back_arrow_button(self, quick_link='Prizes'):
        """
        DESCRIPTION: Click on the Back arrow button.
        EXPECTED: The Splash page is opened.
        """
        self.quick_links[quick_link].quick_links_page.has_back_button()
        self.quick_links[quick_link].quick_links_page.back_button.click()
        quick_links_section = self.site.question_engine.quicklinks_section
        self.assertTrue(quick_links_section,
                        msg='User is not returned to the previous page: "Quick Links Section" on clicking back button')

    def test_003_click_on_the_faq_buttonenter_datalayer_in_the_console(self):
        """
        DESCRIPTION: Click on the 'FAQ' button.
        DESCRIPTION: Enter 'dataLayer' in the console.
        EXPECTED: For Coral:
        EXPECTED: 1. The following code is present in the console:
        EXPECTED: { event: "trackEvent",
        EXPECTED: eventCategory: "Correct4",
        EXPECTED: eventAction: "FAQ",
        EXPECTED: eventLabel: "none" },
        EXPECTED: { event: "content-view"
        EXPECTED: screen_name: "/correct4/info/faq" }
        EXPECTED: 2. The following code is not present in the console:
        EXPECTED: { event: “trackPageview”​,
        EXPECTED: page: “/correct4/info/faq”​ }
        EXPECTED: For Ladbrokes:
        EXPECTED: 1. The following code is present in the console:
        EXPECTED: { event: "trackEvent",
        EXPECTED: eventCategory: "{SourceId}",
        EXPECTED: eventAction: "FAQ",
        EXPECTED: eventLabel: "none"},
        EXPECTED: { event: "content-view"
        EXPECTED: screen_name: "/qe/{sourceId}/info/faq" }
        EXPECTED: 2. The following code is not present in the console:
        EXPECTED: { event: “trackPageview”​,
        EXPECTED: page: “/{sourceId}/info/faq”​ }
        """
        self.navigate_to_quick_link_page(quick_link="Frequently Asked Questions")
        expected_track_event = {'event': 'trackEvent', 'eventCategory': 'Footballsuperseries',
                                'eventAction': 'Frequently Asked Questions', 'eventLabel': 'none'}
        actual_track_event_response = self.get_data_layer_specific_object(object_key='event', object_value='trackEvent')
        self.compare_json_response(actual_track_event_response, expected_track_event)

        expected_conten_view = {'event': 'content-view', 'screen_name': '/footballsuperseries/info/FAQs'}
        actual_content_view_response = self.get_data_layer_specific_object(object_key='event',
                                                                           object_value='content-view')
        self.compare_json_response(actual_content_view_response, expected_conten_view)

        try:
            actual_trackPageview_response = self.get_data_layer_specific_object(object_key='event',
                                                                                object_value='trackPageview')
            self.assertTrue(actual_trackPageview_response,
                            msg='trackPageview data is present, whereas it should not be present')
        except Exception:
            pass

    def test_004_click_on_the_back_arrow_button(self):
        """
        DESCRIPTION: Click on the Back arrow button.
        EXPECTED: The Splash page is opened.
        """
        self.test_002_click_on_the_back_arrow_button(quick_link='Frequently Asked Questions')

    def test_005_click_on_the_terms__conditions_buttonenter_datalayer_in_the_console(self):
        """
        DESCRIPTION: Click on the 'Terms & Conditions' button.
        DESCRIPTION: Enter 'dataLayer' in the console.
        EXPECTED: For Coral:
        EXPECTED: 1. The following code is present in the console:
        EXPECTED: { event: "trackEvent",
        EXPECTED: eventCategory: "Correct4",
        EXPECTED: eventAction: "Terms & Conditions",
        EXPECTED: eventLabel: "none" },
        EXPECTED: { event: "content-view"
        EXPECTED: screen_name: "/correct4/info/terms" }
        EXPECTED: 2. The following code is not present in the console:
        EXPECTED: { event: “trackPageview”​,
        EXPECTED: page: “/correct4/info/terms”​ }
        EXPECTED: For Ladbrokes
        EXPECTED: 1. The following code is present in the console:
        EXPECTED: { event: "trackEvent",
        EXPECTED: eventCategory: "{SourceId}",
        EXPECTED: eventAction: "Terms & Conditions",
        EXPECTED: eventLabel: "none"},
        EXPECTED: { event: "content-view"
        EXPECTED: screen_name: "/qe/{sourceId}/info/terms" }
        EXPECTED: 2. The following code is not present in the console:
        EXPECTED: { event: “trackPageview”​,
        EXPECTED: page: “/{sourceId}/info/terms”​ }
        """
        self.navigate_to_quick_link_page(quick_link="Terms and Conditions")
        expected_track_event = {'event': 'trackEvent', 'eventCategory': 'Footballsuperseries',
                                'eventAction': 'Terms and Conditions', 'eventLabel': 'none'}
        actual_track_event_response = self.get_data_layer_specific_object(object_key='event', object_value='trackEvent')
        self.compare_json_response(actual_track_event_response, expected_track_event)

        expected_conten_view = {'event': 'content-view', 'screen_name': '/footballsuperseries/info/TandCs'}
        actual_content_view_response = self.get_data_layer_specific_object(object_key='event',
                                                                           object_value='content-view')
        self.compare_json_response(actual_content_view_response, expected_conten_view)

        try:
            actual_trackPageview_response = self.get_data_layer_specific_object(object_key='event',
                                                                                object_value='trackPageview')
            self.assertTrue(actual_trackPageview_response,
                            msg='trackPageview data is present, whereas it should not be present')
        except Exception:
            pass
