import pytest
import tests
from voltron.utils.waiters import wait_for_result
from tests.base_test import vtest
from tests.Common import Common


# @pytest.mark.tst2 # QuestionEngine is not configured under qa2
# @pytest.mark.stg2
@pytest.mark.qe_crl_prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.question_engine
@vtest
class Test_C57732084_Verify_the_view_of_the_Quick_link_page_Desktop(Common):
    """
    TR_ID: C57732084
    NAME: Verify the view of the Quick link page [Desktop]
    DESCRIPTION: This test case verifies the view of the Quick link page on the Desktop.
    PRECONDITIONS: 1. The game is configured in the CMS.
    PRECONDITIONS: 2. The User is logged in.
    PRECONDITIONS: 3. The User has not played the game yet.
    PRECONDITIONS: 4. Click on the 'Correct4' link.
    PRECONDITIONS: 5. Login with valid credentials.
    """
    keep_browser_open = True
    device_name = tests.desktop_default

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. The game is configured in the CMS.
        PRECONDITIONS: 2. The User is logged in.
        PRECONDITIONS: 3. The User has not played the game yet.
        PRECONDITIONS: 4. Click on the 'Correct4' link.
        PRECONDITIONS: 5. Login with valid credentials.
        """
        self.create_question_engine_quiz()
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)
        self.navigate_to_page('footballsuperseries')

    def test_001_click_on_any_quick_link(self):
        """
        DESCRIPTION: Click on any Quick link.
        EXPECTED: The Quick links content page is displayed with the CMS content.
        EXPECTED: The Back arrow navigation is displayed in the top left corner.
        EXPECTED: The Page header is displayed underneath the back arrow (as on Mobile).
        EXPECTED: The sub-header with breadcrumbs is not displayed.
        """
        self.__class__.quick_links = list(self.site.question_engine.quicklinks_section.items_as_ordered_dict.values())
        self.assertTrue(self.quick_links, msg='No quick links found on splash page')
        self.quick_links[0].click()
        result = wait_for_result(lambda: self.quick_links[0].quick_links_page.has_back_button(), timeout=20)
        self.assertTrue(result, msg='The Back arrow navigation is not displayed in the top left corner.')

    def test_002_click_on_the_back_arrow_icon(self):
        """
        DESCRIPTION: Click on the Back arrow icon.
        EXPECTED: The Splash page is opened.
        EXPECTED: The sub-header with breadcrumbs is not displayed.
        """
        self.quick_links[0].quick_links_page.back_button.click()
        splash_page = self.site.question_engine.has_cta_button()
        self.assertTrue(splash_page,
                        msg='The Splash page is not opened')
