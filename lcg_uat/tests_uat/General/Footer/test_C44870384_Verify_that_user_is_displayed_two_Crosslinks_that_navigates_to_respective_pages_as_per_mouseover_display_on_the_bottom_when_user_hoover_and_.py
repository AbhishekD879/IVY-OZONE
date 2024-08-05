import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.uat
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.p1
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870384_Verify_that_user_is_displayed_Crosslinks_that_navigates_to_respective_pages_as_per_mouseover_display_on_the_bottom_when_user_hoover_and_link_opens_another_window__Be_Gamble_Aware__https_wwwbegambleawareorg__GamStop_https_wwwgamstop(Common):
    """
    TR_ID: C44870384
    NAME: "Verify that user is displayed  Crosslinks that navigates to respective pages (as per mouseover display on the bottom, when user hoover) and link opens another window - Be Gamble Aware:   https://www.begambleaware.org/ - GamStop: https://www.gamstop.
    DESCRIPTION: This TC is verify navigation from Footer to respective links available.
    """
    keep_browser_open = True

    def click_and_verify_footer_logo(self, footer_logo, name, unique_url_word):
        footer_logo.get(name).perform_click()
        wait_for_result(lambda: self.device.switch_to_new_tab(), timeout=10)
        actual_url = self.device.get_current_url()
        self.assertIn(unique_url_word, actual_url, msg=f'Not navigated to "{unique_url_word}" page')
        self.device.driver.switch_to.window(self.device.driver.window_handles[0])

    def test_001_open_application(self):
        """
        DESCRIPTION: Open application
        EXPECTED: Application is opened and scroll to the bottom on the Homepage
        """
        self.site.wait_content_state('Homepage')

    def test_002_verify_that_user_is_displayed_crosslinks_that_navigates_to_respective_pages_as_per_mouseover_display_on_the_bottom_when_user_hoover_and_link_opens_another_window__when_the_fun_stops_be_gamble_aware__httpswwwbegambleawareorg__gambling_commission_________________httpwwwgamblingcommissiongovukhomeaspx__gamstop_httpswwwgamstopcouk(self):
        """
        DESCRIPTION: "Verify that user is displayed Crosslinks that navigates to respective pages (as per mouseover display on the bottom, when user hoover) and link opens another window
        DESCRIPTION: - When the fun stops (Be Gamble Aware)  (https://www.begambleaware.org/)
        DESCRIPTION: - Gambling Commission:                 http://www.gamblingcommission.gov.uk/home.aspx
        DESCRIPTION: - Gamstop: https://www.gamstop.co.uk/
        EXPECTED: When clicked on user is able to navigate to following links.
        EXPECTED: - When the fun stops (Be Gamble Aware)  (https://www.begambleaware.org/)
        EXPECTED: - Gambling Commission:                 http://www.gamblingcommission.gov.uk/home.aspx
        EXPECTED: - Gamstop:  https://www.gamstop.co.uk/
        """
        footer_logo = self.site.footer.footer_section_bottom.items_as_ordered_dict
        self.site.header.scroll_to_bottom()
        self.click_and_verify_footer_logo(footer_logo, vec.GVC.FOOTER_LINKS_ALT_LIST.begambleaware, vec.GVC.FOOTER_LOGO_URL.begambleaware)
        self.click_and_verify_footer_logo(footer_logo, vec.GVC.FOOTER_LINKS_ALT_LIST.gambling_comission, vec.GVC.FOOTER_LOGO_URL.gambling_comission)
        self.click_and_verify_footer_logo(footer_logo, vec.GVC.FOOTER_LINKS_ALT_LIST.gamestop, vec.GVC.FOOTER_LOGO_URL.gamestop)
