import pytest
from crlat_cms_client.utils.exceptions import CMSException

from tests.base_test import vtest
from tests.Common import Common
import voltron.environments.constants as vec
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.basketball_specific
@pytest.mark.sports_specific
@pytest.mark.adhoc_suite
@vtest
class Test_C66007949_Verify_Virtual_Basketball_banner_display_as_per_CMS_config_and_navigation_to_Virtual_Basketball_page(
    Common):
    """
    TR_ID: C66007949
    NAME: Verify Virtual Basketball banner display as per CMS config and navigation to Virtual Basketball page.
    DESCRIPTION: This test case validates the display of the Virtual sports banner in the Basketball landing page through which the user is redirected to the Virtual Basketball page.
    PRECONDITIONS: In CMS, Sport pages -&gt; Sport Categories -&gt; Basketball sport -&gt; Matches tab -&gt; Under  'Virtual Sports Entry Points Section: Matches'
    PRECONDITIONS: check 'Banner Enabled' check box and enter data in remaining fields
    """
    keep_browser_open = True

    def test_000_pre_conditions(self):
        """
        PRECONDITIONS: In CMS, Sport pages -> Sport Categories -> Basketball sport -> Matches tab -> Under  'Virtual Sports Entry Points Section: Matches'
        PRECONDITIONS: check 'Banner Enabled' check box and enter data in remaining fields
        """
        sport_id = self.ob_config.basketball_config.category_id
        self.__class__.tab_name = self.get_sport_tab_name(name=vec.SB.TABS_NAME_MATCHES.lower(), category_id=sport_id)
        sports_tab_data = self.cms_config.get_sports_tab_data(sport_id=sport_id, tab_name=self.tab_name.lower())
        if sports_tab_data['interstitialBanners']:
            if not sports_tab_data['interstitialBanners']['desktopBannerId'] and not sports_tab_data['interstitialBanners']['mobileBannerId']:
                raise CMSException('"desktopBannerId" and "mobileBannerId" is not available')
        else:
            raise CMSException('interstitialBanners is not configured in cms')
        if not sports_tab_data['interstitialBanners']['bannerEnabled']:
            self.cms_config.update_sports_event_filters(tab_name=self.tab_name.lower(), enabled=True, sport_id=sport_id,
                                                        banner_Enabled=True)
        self.__class__.has_events = self.cms_config.get_sport_tab_status(tab_name=self.tab_name.lower(), sport_id=sport_id)

    def test_001_launch_the_application(self):
        """
        DESCRIPTION: Launch the application
        EXPECTED: Application should be launched successfully.
        """
        self.site.go_to_home_page()
        self.site.wait_content_state(state_name='HomePage')

    def test_002_navigate_to_basketball_sport(self):
        """
        DESCRIPTION: Navigate to Basketball sport
        EXPECTED: Navigation should be successful.
        EXPECTED: By default application navigates to Matches tab/Today sub tab.
        """
        self.site.open_sport('Basketball')
        self.site.wait_content_state_changed()
        if not self.has_events and not self.site.sports_page.tabs_menu.items_as_ordered_dict.get(self.tab_name):
            raise CmsClientException(f'matches tab is not available in basketball sport')

    def test_003_validate_the_presence_of_virtual_basketball_banner(self):
        """
        DESCRIPTION: Validate the presence of Virtual Basketball banner
        EXPECTED: Virtual Basketball banner should be displayed as per CMS configuration.
        """
        tabs = list(self.site.sports_page.tabs_menu.items_as_ordered_dict.keys())
        self.assertIn(self.tab_name, tabs, msg=f'tab name {self.tab_name}'
                                               f' is not available')
        if self.site.sports_page.tabs_menu.current != self.tab_name:
            self.site.sports_page.tabs_menu.click_item(self.tab_name)
        if self.device_type == 'mobile':
            has_virtual_banner = wait_for_result(lambda : self.site.basketball.tab_content.accordions_list.has_virtual_banner_section(), timeout=30)
            self.assertTrue(has_virtual_banner, msg='virtual banner section is not available')
            play_now_button = self.site.basketball.tab_content.accordions_list.virtual_banner_section.Play_now_button
            self.assertTrue(play_now_button, msg='"play now" button is not available in virtual banner section')
            play_now_button.click()
            self.site.wait_content_state(state_name='VirtualSports')
            current_url = self.device.get_current_url()
            self.assertIn('virtual-sports/sports/basketball', current_url,
                          msg='could not redirected to the Virtual Basketball sport page.')
        else:
            grouping_button = self.site.basketball.tab_content.grouping_buttons.current
            if grouping_button != vec.sb.SPORT_DAY_TABS.today:
                self.site.basketball.tab_content.grouping_buttons.items_as_ordered_dict.get(
                    vec.sb.SPORT_DAY_TABS.today).click()
            has_virtual_banner = self.site.basketball.tab_content.accordions_list.has_virtual_banner_section()
            self.assertTrue(has_virtual_banner, msg='virtual banner section is not available')

    def test_004_navigate_to_tomorrow_sub_tab_and_verify_the_presence_of_virtual_sport_banner(self):
        """
        DESCRIPTION: Navigate to Tomorrow sub tab and verify the presence of Virtual Sport banner
        EXPECTED: Virtual Basketball banner should be displayed as per CMS configuration.
        """
        if self.device_type == 'desktop':
            grouping_button = self.site.basketball.tab_content.grouping_buttons.current
            if grouping_button != vec.sb.SPORT_DAY_TABS.tomorrow:
                self.site.basketball.tab_content.grouping_buttons.items_as_ordered_dict.get(
                    vec.sb.SPORT_DAY_TABS.tomorrow).click()
            has_virtual_banner = self.site.basketball.tab_content.accordions_list.has_virtual_banner_section()
            self.assertTrue(has_virtual_banner, msg='virtual banner section is not available')

    def test_005_navigate_to_future_sub_tab_and_verify_the_presence_of_virtual_sport_banner(self):
        """
        DESCRIPTION: Navigate to Future sub tab and verify the presence of Virtual sport banner
        EXPECTED: Virtual Basketball banner should be displayed as per CMS configuration.
        """
        if self.device_type == 'desktop':
            grouping_button = self.site.basketball.tab_content.grouping_buttons.current
            if grouping_button != vec.sb.SPORT_DAY_TABS.future:
                self.site.basketball.tab_content.grouping_buttons.items_as_ordered_dict.get(
                    vec.sb.SPORT_DAY_TABS.future).click()
            has_virtual_banner = self.site.basketball.tab_content.accordions_list.has_virtual_banner_section()
            self.assertTrue(has_virtual_banner, msg='virtual banner section is not available')

    def test_006_click_on_the_banner(self):
        """
        DESCRIPTION: Click on the banner
        EXPECTED: User should be redirected to the Virtual Basketball sport page.
        """
        if self.device_type == 'desktop':
            play_now_button = self.site.basketball.tab_content.accordions_list.virtual_banner_section.Play_now_button
            self.assertTrue(play_now_button, msg='"play now" button is not available in virtual banner section')
            play_now_button.click()
            self.site.wait_content_state(state_name='VirtualSports')
            current_url = self.device.get_current_url()
            self.assertIn('virtual-sports/sports/basketball', current_url,
                          msg='could not redirected to the Virtual Basketball sport page.')
