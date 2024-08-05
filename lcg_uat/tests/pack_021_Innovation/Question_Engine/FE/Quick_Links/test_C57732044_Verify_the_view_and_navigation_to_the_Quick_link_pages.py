import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result


# @pytest.mark.tst2   # question engine is not configured in qa2
# @pytest.mark.stg2
@pytest.mark.qe_crl_prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.question_engine
@vtest
class Test_C57732044_Verify_the_view_and_navigation_to_the_Quick_link_pages(Common):
    """
    TR_ID: C57732044
    NAME: Verify the view and navigation to the Quick link pages
    DESCRIPTION: This test case verifies the view and navigation to the Quick link pages:
    DESCRIPTION: - 'Prizes'
    DESCRIPTION: - 'Frequently Asked Questions'
    DESCRIPTION: - 'Terms & Conditions'
    PRECONDITIONS: 1. The Quick link pages are successfully created and linked to the Splash page in the CMS.
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
        self.create_question_engine_quiz()
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)
        self.navigate_to_page('footballsuperseries')

    def test_001_tap_on_the_prizes_quick_link_in_the_footer(self, quick_link='Prizes', partial_url='Prizes'):
        """
        DESCRIPTION: Tap on the 'Prizes' quick link in the footer.
        EXPECTED: The User is navigated to the 'Prizes' content page.
        EXPECTED: https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a/screen/5d4d962a6765b59ba27451b0
        """
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
            self.assertTrue(self.site.question_engine.quick_links_page.prizes_page_text, msg='Direct navigation to "Prizes" page failed')
        elif quick_link == 'Frequently Asked Questions':
            self.assertTrue(self.site.question_engine.quick_links_page.faqs_page_text,
                            msg='Direct navigation to "FAQs" page failed')
        elif quick_link == 'Terms and Conditions':
            self.assertTrue(self.site.question_engine.quick_links_page.terms_page_text,
                            msg='Direct navigation to "Terms and Conditions" page failed')

    def test_002_tap_on_the_back_arrow_icon(self, quick_link='Prizes'):
        """
        DESCRIPTION: Tap on the 'Back' arrow icon.
        EXPECTED: The User is returned to the previous page.
        """
        self.quick_links[quick_link].quick_links_page.has_back_button()
        self.quick_links[quick_link].quick_links_page.back_button.click()
        quick_links_section = self.site.question_engine.quicklinks_section
        self.assertTrue(quick_links_section, msg='User is not returned to the previous page: "Quick Links Section" on clicking back button')

    def test_003_tap_on_the_frequently_asked_questions_quick_link_in_the_footer(self):
        """
        DESCRIPTION: Tap on the 'Frequently Asked Questions' quick link in the footer.
        EXPECTED: The User is navigated to the 'Frequently Asked Questions' content page.
        EXPECTED: https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a/screen/5d4d962a96fd105217526bf6
        """
        self.test_001_tap_on_the_prizes_quick_link_in_the_footer(quick_link='Frequently Asked Questions', partial_url='FAQs')

    def test_004_tap_on_the_back_arrow_icon(self):
        """
        DESCRIPTION: Tap on the 'Back' arrow icon.
        EXPECTED: The User is returned to the previous page.
        """
        self.test_002_tap_on_the_back_arrow_icon()

    def test_005_tap_on_the_terms__conditions_quick_link_in_the_footer(self):
        """
        DESCRIPTION: Tap on the 'Terms & Conditions' quick link in the footer.
        EXPECTED: The User is navigated to the 'Terms & Conditions' content page.
        EXPECTED: https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a/screen/5d4d962a96fd105217526bf6
        """
        self.test_001_tap_on_the_prizes_quick_link_in_the_footer(quick_link='Terms and Conditions', partial_url='TandCs')

    def test_006_tap_on_the_back_arrow_icon(self):
        """
        DESCRIPTION: Tap on the 'Back' arrow icon.NN
        EXPECTED: The User is returned to the previous page.
        """
        self.test_002_tap_on_the_back_arrow_icon()
