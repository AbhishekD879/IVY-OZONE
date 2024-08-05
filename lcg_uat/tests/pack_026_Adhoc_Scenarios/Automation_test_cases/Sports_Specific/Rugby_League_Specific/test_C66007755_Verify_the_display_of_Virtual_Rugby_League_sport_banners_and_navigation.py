import pytest
from crlat_cms_client.utils.exceptions import CMSException
from tests.base_test import vtest
from tests.Common import Common
import voltron.environments.constants as vec
from voltron.utils.waiters import wait_for_result

@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.navigation
@pytest.mark.sports_specific
@pytest.mark.rugby_league_specific
@pytest.mark.adhoc_suite
@pytest.mark.desktop
@vtest
class Test_C66007755_Verify_the_display_of_Virtual_Rugby_League_sport_banners_and_navigation(Common):
    """
    TR_ID: C66007755
    NAME: Verify the display of  Virtual Rugby League sport banners and navigation
    DESCRIPTION: This test case validates the display of the Virtual sports banner in the Rugby League landing page through which the user is redirected to the Virtual Rugby sports.
    PRECONDITIONS: In CMS, Sport pages -&gt; Sport Categories -&gt; Rugby league sport -&gt; Matches tab -&gt; Under  'Virtual Sports Entry Points Section: Matches'
    PRECONDITIONS: check 'Banner Enabled' check box and enter data in remaining fields.
    """
    keep_browser_open = True
    def test_000_pre_conditions(self):
        """
        PRECONDITIONS: In CMS, Sport pages -> Sport Categories -> Basketball sport -> Matches tab -> Under  'Virtual Sports Entry Points Section: Matches'
        PRECONDITIONS: check 'Banner Enabled' check box and enter data in remaining fields
        """
        sport_id = self.ob_config.rugby_league_config.category_id
        tab_name = vec.sb.MATCHES.lower()
        sports_tab_data = self.cms_config.get_sports_tab_data(sport_id=sport_id, tab_name=tab_name)
        if sports_tab_data['interstitialBanners']:
            if not sports_tab_data['interstitialBanners']['desktopBannerId'] and not sports_tab_data['interstitialBanners']['mobileBannerId']:
                raise CMSException('"desktopBannerId" and "mobileBannerId" is not available')
        else:
            raise CMSException('interstitialBanners is not configured in cms')
        if not sports_tab_data['interstitialBanners']['bannerEnabled']:
            self.cms_config.update_sports_event_filters(tab_name=tab_name, enabled=True, sport_id=sport_id,
                                                        banner_Enabled=True)
    def test_001_launch_the_application(self):
        """
        DESCRIPTION: Launch the application
        EXPECTED: Application should be launched successfully.
        """
        self.site.go_to_home_page()
        self.site.wait_content_state(state_name='HomePage')
    def test_002_navigate_to_rugby_league_sport(self):
        """
        DESCRIPTION: Navigate to Rugby league sport
        EXPECTED: Navigation should be successful.
        EXPECTED: By default application navigates to Matches tab/Today subtab.
        """
        self.site.open_sport('Rugby League')
    def test_003_validate_the_presence_of_virtual_rugby_league_banner(self):
        """
        DESCRIPTION: Validate the presence of Virtual Rugby League banner
        EXPECTED: Virtual Rugby League banner should be displayed as per CMS configuration.
        """
        if self.device_type == 'mobile':
            tabs = list(self.site.sports_page.tabs_menu.items_as_ordered_dict.keys())
            self.assertIn(vec.SB.TABS_NAME_MATCHES.upper(),tabs,msg=f'tab name {vec.SB.TABS_NAME_MATCHES.upper()}'
                                                                    f'is not available')
            if self.site.sports_page.tabs_menu.current != vec.SB.TABS_NAME_MATCHES.upper():
                self.site.sports_page.tabs_menu.click_item(vec.SB.TABS_NAME_MATCHES.upper())
            has_virtual_banner = wait_for_result(lambda : self.site.sports_page.tab_content.accordions_list.has_virtual_banner_section(), timeout=30)
            self.assertTrue(has_virtual_banner, msg='virtual banner section is not available')
            play_now_button = self.site.sports_page.tab_content.accordions_list.virtual_banner_section.Play_now_button
            self.assertTrue(play_now_button, msg='"play now" button is not available in virtual banner section')
            play_now_button.click()
            self.site.wait_content_state(state_name='VirtualSports')
            current_url = self.device.get_current_url()
            self.assertIn('virtual-sports/sports/basketball', current_url,
                          msg='could not redirected to the Virtual Basketball sport page.')
        else:
            grouping_button = self.site.sports_page.tab_content.grouping_buttons.current
            if grouping_button != vec.sb.SPORT_DAY_TABS.today:
                self.site.sports_page.tab_content.grouping_buttons.items_as_ordered_dict.get(vec.sb.SPORT_DAY_TABS.today).click()
            has_virtual_banner = self.site.sports_page.tab_content.accordions_list.has_virtual_banner_section()
            self.assertTrue(has_virtual_banner, msg='virtual banner section is not available')
    def test_004_navigate_to_tomorrow_sub_tab_and_verify_the_presence_of_virtual_sport_banner(self):
        """
        DESCRIPTION: Navigate to Tomorrow sub tab and verify the presence of Virtual Sport banner
        EXPECTED: Virtual Rugby League banner should be displayed as per CMS configuration.
        """
        if self.device_type == 'desktop':
            grouping_button = self.site.sports_page.tab_content.grouping_buttons.current
            if grouping_button != vec.sb.SPORT_DAY_TABS.tomorrow:
                self.site.sports_page.tab_content.grouping_buttons.items_as_ordered_dict.get(vec.sb.SPORT_DAY_TABS.tomorrow).click()
            has_virtual_banner = self.site.sports_page.tab_content.accordions_list.has_virtual_banner_section()
            self.assertTrue(has_virtual_banner, msg='virtual banner section is not available')
    def test_005_navigate_to_future_sub_tab_and_verify_the_presence_of_virtual_sport_banner(self):
        """
        DESCRIPTION: Navigate to Future sub tab and verify the presence of Virtual sport banner
        EXPECTED: Virtual Rugby League banner should be displayed as per CMS configuration.
        """
        if self.device_type == 'desktop':
            grouping_button = self.site.sports_page.tab_content.grouping_buttons.current
            if grouping_button != vec.sb.SPORT_DAY_TABS.future:
                self.site.sports_page.tab_content.grouping_buttons.items_as_ordered_dict.get(vec.sb.SPORT_DAY_TABS.future).click()
            has_virtual_banner = self.site.sports_page.tab_content.accordions_list.has_virtual_banner_section()
            self.assertTrue(has_virtual_banner, msg='virtual banner section is not available')
    def test_006_click_on_the_banner(self):
        """
        DESCRIPTION: Click on the banner
        EXPECTED: User should be redirected to the Virtual Rugby League sport page.
        """
        if self.device_type == 'desktop':
            play_now_button = self.site.basketball.tab_content.accordions_list.virtual_banner_section.Play_now_button
            self.assertTrue(play_now_button, msg='"play now" button is not available in virtual banner section')
            play_now_button.click()
            self.site.wait_content_state(state_name='VirtualSports')
            current_url = self.device.get_current_url()
            self.assertIn('virtual-sports/sports/basketball', current_url,
                          msg='could not redirected to the Virtual Basketball sport page.')