import pytest
from tests.Common import Common
from tests.base_test import vtest
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.uat
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.p2
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870383_Verify_that_user_is_displayed_Crosslinks_that_navigates_to_respective_pages_as_per_mouseover_display_on_the_bottom_when_user_hoover_and_this_ink_opens_another_window(Common):
    """
    TR_ID: C44870383
    NAME: "Verify that user is displayed Crosslinks that navigates to respective pages (as per mouseover display on the bottom, when user hoover): and this ink opens another window
    DESCRIPTION: This TC is to verify all footer links are navigating accordingly.
    """
    keep_browser_open = True

    def click_and_verify_footer_logo(self, footer_logo, name, unique_url_word):
        footer_logo.get(name).perform_click()
        if name == vec.GVC.FOOTER_LINKS_ALT_LIST.eighteen:
            self.device.driver.switch_to.window(self.device.driver.window_handles[0])
        else:
            wait_for_result(lambda: self.device.switch_to_new_tab(), timeout=10)
        actual_url = self.device.get_current_url()
        self.assertIn(unique_url_word, actual_url, msg=f'Not navigated to "{unique_url_word}" page')
        if name == vec.GVC.FOOTER_LINKS_ALT_LIST.eighteen:
            self.device.go_back()
        else:
            self.device.driver.switch_to.window(self.device.driver.window_handles[0])

    def test_001_open_application(self):
        """
        DESCRIPTION: Open application.
        EXPECTED: Application is opened.
        """
        self.site.wait_content_state("Homepage")

    def test_002_verify_that_user_is_displayed_crosslinks_that_navigates_to_respective_pages_as_per_mouseover_display_on_the_bottom_when_user_hoover_and_this_ink_opens_another_windowgam_stop_httpsgamstopcoukgamcare_httpwwwgamcareorgukgambling_commission_httpgamblingcommissiongovukibas_httpwwwibas_ukcom18plus_httpmedialadbrokescom(self):
        """
        DESCRIPTION: "Verify that user is displayed Crosslinks that navigates to respective pages (as per mouseover display on the bottom, when user hoover): and this ink opens another window
        DESCRIPTION: Gam stop https://gamstop.co.uk/
        DESCRIPTION: GamCare http://www.gamcare.org.uk/
        DESCRIPTION: Gambling Commission http://gamblingcommission.gov.uk/
        DESCRIPTION: IBAS http://www.ibas-uk.com/
        DESCRIPTION: 18+ https://www.coral.co.uk/en/p/18plus"
        EXPECTED: When clicked on, user is navigated to appropriate links.
        EXPECTED: Gam stop https://gamstop.co.uk/
        EXPECTED: GamCare http://www.gamcare.org.uk/
        EXPECTED: Gambling Commission http://gamblingcommission.gov.uk/
        EXPECTED: IBAS http://www.ibas-uk.com/
        EXPECTED: 18+ https://www.coral.co.uk/en/p/18plus"
        """
        footer_logo = self.site.footer.footer_section_bottom.items_as_ordered_dict
        self.site.header.scroll_to_bottom()
        self.click_and_verify_footer_logo(footer_logo, vec.GVC.FOOTER_LINKS_ALT_LIST.ibas,
                                          vec.GVC.FOOTER_LOGO_URL.ibas)
        self.click_and_verify_footer_logo(footer_logo, vec.GVC.FOOTER_LINKS_ALT_LIST.gamecare,
                                          vec.GVC.FOOTER_LOGO_URL.gamecare)
        self.click_and_verify_footer_logo(footer_logo, vec.GVC.FOOTER_LINKS_ALT_LIST.gambling_comission,
                                          vec.GVC.FOOTER_LOGO_URL.gambling_comission)
        self.click_and_verify_footer_logo(footer_logo, vec.GVC.FOOTER_LINKS_ALT_LIST.gamestop,
                                          vec.GVC.FOOTER_LOGO_URL.gamestop)
        self.click_and_verify_footer_logo(footer_logo, vec.GVC.FOOTER_LINKS_ALT_LIST.eighteen,
                                          vec.GVC.FOOTER_LOGO_URL.eighteen)
