import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.user_account
@vtest
class Test_C15358884_Verify_Vanilla_Unplug_gamecare_certified_functionality(Common):
    """
    TR_ID: C15358884
    NAME: Verify [Vanilla] Unplug gamecare-certified functionality
    DESCRIPTION: 1)remove 'gamecare-certified' route from vanilla app-routing.module
    DESCRIPTION: 2) */gamecare-certified page should not be available in vanilla app
    DESCRIPTION: 3) GameCareCertifiedComponent should be unplugged from bma module
    PRECONDITIONS: User should be logged in
    PRECONDITIONS: Example of credentials :
    PRECONDITIONS: login:ukmigct-tstEUR02
    PRECONDITIONS: password: 123123
    """
    keep_browser_open = True

    def test_001_login_to_test_environment(self):
        """
        DESCRIPTION: Login to test environment
        EXPECTED: Successful login
        """
        self.site.login()

    def test_002_navigate_via_link_url_plus_gamecare_certified(self):
        """
        DESCRIPTION: Navigate via link "url" + */gamecare-certified
        EXPECTED: Verify user is redirected to a home page
        """
        url = tests.HOSTNAME + "/gamecare-certified"
        self.device.navigate_to(url=url)
        self.site.wait_content_state("HomePage")

    def test_003_click_gamcare_logo_at_the_footerindexphpattachmentsget31291_orindexphpattachmentsget31292(self):
        """
        DESCRIPTION: Click GamCare logo at the footer
        DESCRIPTION: ![](index.php?/attachments/get/31291) or
        DESCRIPTION: ![](index.php?/attachments/get/31292)
        EXPECTED: Verify user is redirected to :
        EXPECTED: https://www.gamcare.org.uk/
        """
        footer_logo = self.site.footer.footer_section_bottom.items_as_ordered_dict
        self.site.header.scroll_to_bottom()
        footer_logo.get(vec.GVC.FOOTER_LINKS_ALT_LIST.gamecare).perform_click()
        self.site.wait_content_state_changed(timeout=15)
        if self.brand == 'bma':
            wait_for_result(lambda: self.device.switch_to_new_tab(), timeout=10)
        actual_url = self.device.get_current_url()
        self.assertIn(vec.GVC.FOOTER_LOGO_URL.gamecare, actual_url,
                      msg=f'Not navigated to "{vec.GVC.FOOTER_LOGO_URL.gamecare}" page')
        self.device.driver.switch_to.window(self.device.driver.window_handles[0])
