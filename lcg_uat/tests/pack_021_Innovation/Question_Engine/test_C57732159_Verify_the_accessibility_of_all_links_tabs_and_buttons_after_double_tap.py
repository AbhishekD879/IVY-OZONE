import pytest
from time import sleep
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result


# @pytest.mark.crl_tst2   # question engine is not configured in qa2
# @pytest.mark.crl_stg2
# @pytest.mark.crl_hl
@pytest.mark.qe_crl_prod
@pytest.mark.desktop
@pytest.mark.question_engine
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C57732159_Verify_the_accessibility_of_all_links_tabs_and_buttons_after_double_tap(Common):
    """
    TR_ID: C57732159
    NAME: Verify the accessibility of all links, tabs and buttons after double tap
    DESCRIPTION: This test case verifies the accessibility of all links, tabs and buttons after double tap
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Zeplin
    PRECONDITIONS: 1. The user is logged in to Coral/Ladbrokes test environment
    PRECONDITIONS: 2. The link to Correct 4 is available on the website
    """
    keep_browser_open = True

    def navigate_to_quicklinks_page(self, quicklink='Prizes'):
        quick_links = self.site.question_engine.quicklinks_section.items_as_ordered_dict
        self.assertTrue(quick_links, msg='No quick links found on splash page')
        current_url = self.device.get_current_url()
        self.assertTrue(quicklink in list(quick_links.keys()),
                        msg=f'Expected quick link "{quicklink}" is not present in actual list of links "{list(quick_links.keys())}"')
        quick_links[quicklink].click()
        self.assertTrue(wait_for_result(lambda: current_url != self.device.get_current_url()),
                        msg=f'User is still on the splash page after clicking on quick link item')
        self.site.wait_splash_to_hide(timeout=10)
        if quicklink == 'Prizes':
            self.assertTrue(self.site.question_engine.quick_links_page.prizes_page_text,
                            msg='Direct navigation to "Prizes" page failed')
        elif quicklink == 'Frequently Asked Questions':
            self.assertTrue(self.site.question_engine.quick_links_page.faqs_page_text,
                            msg='Direct navigation to "FAQs" page failed')
        elif quicklink == 'Terms and Conditions':
            self.assertTrue(self.site.question_engine.quick_links_page.terms_page_text,
                            msg='Direct navigation to "Terms and Conditions" page failed')

        quick_links[quicklink].quick_links_page.has_back_button()
        quick_links[quicklink].quick_links_page.back_button.click()
        quick_links_section = self.site.question_engine.quicklinks_section
        self.assertTrue(quick_links_section,
                        msg='User is not returned to the previous page: "Quick Links Section" on clicking back button')

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. The game is configured in the CMS.
        PRECONDITIONS: 2. The User is logged in.
        """
        self.create_question_engine_quiz(pop_up=True)
        user_name = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=user_name)

    def test_001_double_tap_on_the_correct_4_link(self):
        """
        DESCRIPTION: Double-tap on the Correct 4 link
        EXPECTED: Correct 4 is opened
        """
        if self.device_type == 'mobile':
            self.site.home.menu_carousel.click_item('FOOTBALL SUPER SERIES')
        else:
            self.site.header.sport_menu.click_item('FOOTBALL SUPER SERIES')
        self.site.wait_content_state_changed(timeout=5)
        status = wait_for_result(lambda: self.site.question_engine.has_cta_button(), timeout=10,
                                 name='"Football Super Series" page to be opened')
        self.assertTrue(status, msg='"Football Super Series" page is not opened')

    def test_002_double_tap_on_each_link_tabs_and_buttons_on_splash_page(self):
        """
        DESCRIPTION: Double-tap on each quick link and verify navigation
        EXPECTED: The User is redirected to the respective page.
        """
        self.navigate_to_quicklinks_page()
        self.navigate_to_quicklinks_page(quicklink='Frequently Asked Questions')
        self.navigate_to_quicklinks_page(quicklink='Terms and Conditions')

    def test_003_double_tap_on_each_link_tabs_and_buttons_on__page(self):
        """
        DESCRIPTION: Double-tap on play button on splash Page
        EXPECTED: The 'latest' and 'previous' tabs are opened after completing quiz.
        """
        self.navigate_to_page('footballsuperseries')
        wait_for_result(lambda: 'footballsuperseries' in self.device.get_current_url(), timeout=8)
        self.assertTrue(self.site.question_engine.has_cta_button(), msg=f'cta button is not displayed')
        self.site.question_engine.cta_button.click()
        questions = list(self.site.quiz_home_page.question_container.items_as_ordered_dict.values())
        self.assertTrue(questions, msg=f' questions are not displayed')

        options = list(questions[0].answer_options.items_as_ordered_dict.values())
        options[0].click()
        sleep(3)
        options = list(questions[1].answer_options.items_as_ordered_dict.values())
        options[0].click()
        sleep(3)
        options = list(questions[2].answer_options.items_as_ordered_dict.values())
        options[0].click()
        sleep(3)
        options = list(questions[3].answer_options.items_as_ordered_dict.values())
        options[0].click()
        sleep(3)
        self.site.quiz_page_popup.submit_button.click()
        status = wait_for_result(lambda: self.site.quiz_results_page.latest_tab.is_displayed(), timeout=10,
                                 name='Latest tab to be displayed')
        self.assertTrue(status, msg='Latest tab is not displayed')
        self.assertTrue(self.site.quiz_results_page.previous_tab.is_displayed(), msg='Previous tab is not displayed')

    def test_004_double_tap_on_each_link_tabs_and_buttons_on_splash_page(self):
        """
        DESCRIPTION: Double-tap on Leaderboard/Previous page button on Splash Page
        EXPECTED: The User is navigated to the respective page.
        """
        self.navigate_to_page('footballsuperseries')
        wait_for_result(lambda: 'footballsuperseries' in self.device.get_current_url(), timeout=5)
        leaderboard_button = self.site.question_engine.has_previous_results_link()
        if leaderboard_button:
            self.site.question_engine.previous_results_link.click()
            self.site.wait_content_state_changed(timeout=5)
            self.navigate_to_page('footballsuperseries')
            wait_for_result(lambda: 'footballsuperseries' in self.device.get_current_url(), timeout=5)

    def test_005_double_tap_on_each_link_tabs_and_buttons_on_splash_page(self):
        """
        DESCRIPTION: Double-tap on cross button on Splash Page(mobile)
        EXPECTED: The User is redirected to the Home page.
        """
        if self.device_type == 'mobile':
            close_button = self.site.question_engine.has_close_button()
            if close_button:
                self.site.question_engine.close_button.click()
                self.site.wait_content_state("Homepage")
