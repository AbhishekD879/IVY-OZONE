import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from time import sleep
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.desktop
@pytest.mark.uat
@pytest.mark.prod
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C44870405_Verify_Coral_site_logo_display_and_navigation(Common):
    """
    TR_ID: C44870405
    NAME: Verify Coral site logo display and navigation
    DESCRIPTION: Coral logo should be visible in it's respective header on all pages of the website and user should be able to click on the logo and navigate to the homepage via this logo.
    PRECONDITIONS: Coral logo is available in logged in and logged out state.
    """
    keep_browser_open = True
    device_name = tests.desktop_default

    def test_001_open_httpsbeta_sportscoralcouk_on_chrome_browser(self):
        """
        DESCRIPTION: Open https://beta-sports.coral.co.uk/ on Chrome browser.
        EXPECTED: https://beta-sports.coral.co.uk/ displayed on Chrome browser.
        """
        self.site.login()

    def test_002_click_on_in_play_via_header_links(self):
        """
        DESCRIPTION: Click on In-Play via header links
        EXPECTED: In-play page displayed and Coral logo is displayed in header at the top.
        """
        self.site.header.sport_menu.items_as_ordered_dict.get('IN-PLAY').click()
        actual_tab_title = self.site.home.header_line.page_title.sport_title
        if self.brand == 'ladbrokes':
            self.assertEqual(actual_tab_title, vec.inplay.BY_IN_PLAY,
                             msg=f'actual tab: "{actual_tab_title}" is not same as expected tab "{vec.inplay.BY_IN_PLAY}"')
        else:
            self.assertEqual(actual_tab_title, vec.siteserve.IN_PLAY_TAB,
                             msg=f'actual tab: "{actual_tab_title}" is not same as expected tab "{vec.siteserve.IN_PLAY_TAB}"')
        self.assertTrue(self.site.header.brand_logo.is_displayed(),
                        msg='"Brand logo" is not found on header')

    def test_003_click_on_coral_logo(self):
        """
        DESCRIPTION: Click on Coral logo.
        EXPECTED: User directed back to the homepage.
        """
        wait_for_result(lambda: self.site.header.brand_logo.is_displayed(), name='brand logo to be displayed',
                        timeout=10)
        self.site.header.brand_logo.click()
        sleep(2)
        self.site.wait_content_state("HomePage")

    def test_004_click_on_a_sport_in_the_a_z_sports_menu_list(self):
        """
        DESCRIPTION: Click on a sport in the A-Z Sports menu list.
        EXPECTED: Respective sport displayed and Coral logo is displayed in header at the top.
        """
        # covered in step6
        pass

    def test_005_click_on_coral_logo(self):
        """
        DESCRIPTION: Click on Coral logo.
        EXPECTED: User directed back to the homepage.
        """
        self.test_003_click_on_coral_logo()

    def test_006_repeat_above_steps_for_a_range_of_areas_on_the_site(self):
        """
        DESCRIPTION: Repeat above steps for a range of areas on the site
        EXPECTED: Respective pages displayed and Coral logo is displayed in header at the top. User should always be able to direct back to the homepage by clicking on the Coral site logo.
        """
        az_sports = self.site.sport_menu.sport_menu_items_group('Main').items_as_ordered_dict
        self.assertTrue(az_sports, msg=f'"{az_sports}" are not found')
        for sport in az_sports.keys():
            az_sports = self.site.sport_menu.sport_menu_items_group('Main').items_as_ordered_dict
            if self.brand == 'ladbrokes':
                if sport not in ['The Grid', 'Instant Spins', 'News & Blogs']:
                    sleep(2)
                    az_sports[sport].click()
            else:
                if sport not in ['Correct 4', 'Live Casino', 'News & Blogs', 'Racing Super Series', 'Roulette', 'Shooting', 'Slots', 'Softball', 'Sports Roulette', 'Surfing', 'Swimming', 'Water Polo']:
                    az_sports[sport].click()
                status = wait_for_result(lambda: self.site.header.brand_logo.is_displayed(),
                                         name="Logo to be displayed", timeout=10)
                self.assertTrue(status,
                                msg='"Brand logo" is not found on header')
            self.test_003_click_on_coral_logo()

    def test_007_repeat_above_steps_after_logout(self):
        """
        DESCRIPTION: Repeat above steps after logout
        """
        self.site.logout()
        self.test_002_click_on_in_play_via_header_links()
        self.test_003_click_on_coral_logo()
        self.test_005_click_on_coral_logo()
        self.test_006_repeat_above_steps_for_a_range_of_areas_on_the_site()
