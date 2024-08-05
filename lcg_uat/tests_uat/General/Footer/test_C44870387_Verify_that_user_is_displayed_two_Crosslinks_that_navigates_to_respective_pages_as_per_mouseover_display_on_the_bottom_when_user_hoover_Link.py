import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.stg2
@pytest.mark.tst2
@pytest.mark.prod
@pytest.mark.uat
@pytest.mark.desktop
@pytest.mark.p2
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870387_Verify_that_user_is_displayed_two_Crosslinks_that_navigates_to_respective_pages_as_per_mouseover_display_on_the_bottom_when_user_hoover_Link_open_another_window__Be_Gamble_Aware__https_wwwbegambleawareorg__Gambling_commission(Common):
    """
    TR_ID: C44870387
    NAME: "Verify that user is displayed two Crosslinks that navigates to respective pages (as per mouseover display on the bottom, when user hoover): Link open another window - Be Gamble Aware:   https://www.begambleaware.org/ - Gambling commission:
    DESCRIPTION: "Verify that user is displayed two Crosslinks that navigates to respective pages (as per mouseover display on the bottom, when user hoover):
    DESCRIPTION: Link open another window
    DESCRIPTION: - Be Gamble Aware:  http://www.whenthefunstops.co.uk/( https://www.begambleaware.org/)
    DESCRIPTION: - Gambling commission:                  https://www.gamstop.co.uk/"
    """
    keep_browser_open = True

    def click_and_verify_footer_logo(self, footer_logo, name, unique_url_word):
        footer_logo.get(name).perform_click()
        wait_for_result(lambda: self.device.switch_to_new_tab(), timeout=10)
        actual_url = self.device.get_current_url()
        self.assertIn(unique_url_word, actual_url, msg=f'Not navigated to "{unique_url_word}" page')
        self.device.driver.switch_to.window(self.device.driver.window_handles[0])

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Application is loaded.
        """
        self.site.wait_content_state('Homepage')

    def test_002_navigate_to_the_bottom_of_the_page_and_select_thegamble_aware__when_the_fun_stops_stop_responsible_gambling_icons(self):
        """
        DESCRIPTION: Navigate to the bottom of the page and select the
        DESCRIPTION: Gamble aware ( when the FUN stops STOP) &
        DESCRIPTION: Responsible Gambling icons
        EXPECTED:
        """
        # Covered in step 3

    def test_003_verify_that_user_is_displayed_two_crosslinks_that_navigates_to_respective_pages_as_per_mouseover_display_on_the_bottom_when_user_hooverlink_open_another_window__be_gamble_aware_when_the_fun_stops_stop__httpswwwbegambleawareorg__gambling_commission_httpwwwgamblingcommissiongovukhomeaspx(self):
        """
        DESCRIPTION: "Verify that user is displayed two Crosslinks that navigates to respective pages (as per mouseover display on the bottom, when user hoover):
        DESCRIPTION: Link open another window
        DESCRIPTION: - Be Gamble Aware (when the FUN stops STOP):  https://www.begambleaware.org/
        DESCRIPTION: - Gambling commission: http://www.gamblingcommission.gov.uk/home.aspx
        EXPECTED: When clicked on links, user is navigated to appropriate links.
        EXPECTED: Link open another window
        EXPECTED: - Be Gamble Aware (when the FUN stops STOP): https://www.begambleaware.org/
        EXPECTED: - Gambling commission:  http://www.gamblingcommission.gov.uk/home.aspx
        """
        footer_logo = self.site.footer.footer_section_bottom.items_as_ordered_dict
        self.site.header.scroll_to_bottom()
        self.click_and_verify_footer_logo(footer_logo=footer_logo, name=vec.gvc.FOOTER_LINKS_ALT_LIST.begambleaware, unique_url_word=vec.gvc.FOOTER_LOGO_URL.begambleaware)
        self.click_and_verify_footer_logo(footer_logo=footer_logo, name=vec.gvc.FOOTER_LINKS_ALT_LIST.gambling_comission, unique_url_word=vec.gvc.FOOTER_LOGO_URL.gambling_comission)
