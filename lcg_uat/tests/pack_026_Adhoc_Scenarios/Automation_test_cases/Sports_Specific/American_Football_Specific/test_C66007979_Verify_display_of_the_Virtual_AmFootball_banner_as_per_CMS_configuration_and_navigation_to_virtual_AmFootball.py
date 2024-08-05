import pytest
from tests.base_test import vtest
from tests.Common import Common
import voltron.environments.constants as vec
from crlat_cms_client.utils.exceptions import CMSException
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.sports_specific
@pytest.mark.american_football
@pytest.mark.adhoc_suite
@vtest
class Test_C66007979_Verify_display_of_the_Virtual_AmFootball_banner_as_per_CMS_configuration_and_navigation_to_virtual_AmFootball(Common):
    """
    TR_ID: C66007979
    NAME: Verify display of the Virtual Am.Football banner as per CMS configuration and navigation to virtual Am.Football
    DESCRIPTION: This testcase verifies Virtual American Football banner display as per CMS configuration and navigation to virtual Am.Football page.
    PRECONDITIONS: 1. CMS -&gt; Sports pages -&gt; Sport category -&gt; American Football
    PRECONDITIONS: 2. Navigate to any tab ex: matches
    PRECONDITIONS: 3. Navigate to Sitecore and upload a banner
    PRECONDITIONS: Note: Banners entry point will be configured and displayed only for Matches, Events and Competitions tab
    """
    keep_browser_open = True

    def test_000_pre_conditions(self):
        """
        PRECONDITIONS: In CMS, Sport pages -> Sport Categories -> Basketball sport -> Matches tab -> Under  'Virtual Sports Entry Points Section: Matches'
        PRECONDITIONS: check 'Banner Enabled' check box and enter data in remaining fields
        """
        sport_id = self.ob_config.american_football_config.category_id
        tab_name = vec.sb.MATCHES.lower()
        sports_tab_data = self.cms_config.get_sports_tab_data(sport_id=sport_id, tab_name=tab_name)
        if sports_tab_data['interstitialBanners']:
            if not sports_tab_data['interstitialBanners']['desktopBannerId'] and not \
            sports_tab_data['interstitialBanners']['mobileBannerId']:
                raise CMSException('"desktopBannerId" and "mobileBannerId" is not available')
        else:
            raise CMSException('interstitialBanners is not configured in cms')
        if not sports_tab_data['interstitialBanners']['bannerEnabled']:
            self.cms_config.update_sports_event_filters(tab_name=tab_name, enabled=True, sport_id=sport_id,
                                                        banner_Enabled=True)
        self.__class__.has_events = self.cms_config.get_sport_tab_status(tab_name=tab_name, sport_id=sport_id)

    def test_001_launch__the_login_to_the_cmsapplication(self):
        """
        DESCRIPTION: Launch  the login to the CMS
        DESCRIPTION: application
        EXPECTED: User should be able to launch and login to the application successfully
        """
        # covered in above step

    def test_002_navigate_to_the_sports_category__ampgt_american_football(self):
        """
        DESCRIPTION: Navigate to the Sports Category -&amp;gt; American Football
        EXPECTED: User should be able to see "Virtual sports entry points section: Matches"
        """
        # covered in above step

    def test_003_verify_virtual_sports_entry_pointssection_matches(self):
        """
        DESCRIPTION: Verify "Virtual sports entry points
        DESCRIPTION: section: Matches"
        EXPECTED: User should be able to see below fields
        EXPECTED: a. Banner enable check box
        EXPECTED: b. Desktop banner id
        EXPECTED: c. Mobile banner id
        EXPECTED: d. CTA button label
        EXPECTED: e. redirection url
        EXPECTED: f. Banner position
        """
        # covered in above step

    def test_004_fill_the_fields(self):
        """
        DESCRIPTION: Fill the fields
        EXPECTED: User should be able to fill below fields
        EXPECTED: a. Banner enable check box: enable
        EXPECTED: b. Desktop banner id: should be copied from sitecore
        EXPECTED: c. Mobile banner id: should be copied from sitecore
        EXPECTED: d. CTA button label: Type as "Play now"
        EXPECTED: e. redirection url: Type the url, for which sport user need to be navigate
        EXPECTED: f. Banner position: provide any number, in below which accordian banner should be display ex:3
        EXPECTED: Note: Banners will be displayed as per accordian number which is configured in CMS
        """
        # covered in above step

    def test_005_verify_banner_in_front_end_application(self):
        """
        DESCRIPTION: Verify banner in front end application
        EXPECTED: User should be able to navigate to Am.Football-&amp;gt; Matches tab
        EXPECTED: Virtual American Football sport banner should be displayed in the FE.
        """
        self.site.go_to_home_page()
        self.navigate_to_page('sport/american-football')
        self.site.wait_content_state_changed()
        if not self.has_events and not self.site.sports_page.tabs_menu.items_as_ordered_dict.get(vec.SB.TABS_NAME_MATCHES.upper()):
            raise CmsClientException(f'matches tab is not available in american football')
        if self.device_type == 'mobile':
            tabs = list(self.site.sports_page.tabs_menu.items_as_ordered_dict.keys())
            self.assertIn(vec.SB.TABS_NAME_MATCHES.upper(), tabs, msg=f'tab name {vec.SB.TABS_NAME_MATCHES.upper()}'
                                                                      f' is not available')
            if self.site.sports_page.tabs_menu.current != vec.SB.TABS_NAME_MATCHES.upper():
                self.site.sports_page.tabs_menu.click_item(vec.SB.TABS_NAME_MATCHES.upper())
            has_virtual_banner = wait_for_result(
                lambda: self.site.sports_page.tab_content.accordions_list.has_virtual_banner_section(), timeout=30)
            self.assertTrue(has_virtual_banner, msg='virtual banner section is not available')
            play_now_button = self.site.sports_page.tab_content.accordions_list.virtual_banner_section.Play_now_button
            self.assertTrue(play_now_button, msg='"play now" button is not available in virtual banner section')
            play_now_button.click()
            self.site.wait_content_state(state_name='VirtualSports')
            current_url = self.device.get_current_url()
            self.assertIn('virtual-sports/sports/american-football', current_url,
                          msg='could not redirected to the Virtual Basketball sport page.')
        else:
            current_tab = self.site.sports_page.tab_content.grouping_buttons.current
            if current_tab != vec.sb.SPORT_DAY_TABS.today:
                self.site.sports_page.tab_content.grouping_buttons.items_as_ordered_dict.get(vec.sb.SPORT_DAY_TABS.today).click()
            has_virtual_banner = self.site.sports_page.tab_content.accordions_list.has_virtual_banner_section()
            self.assertTrue(has_virtual_banner, msg='virtual banner section is not available')
            current_tab = self.site.sports_page.tab_content.grouping_buttons.current
            if current_tab != vec.sb.SPORT_DAY_TABS.tomorrow:
                self.site.sports_page.tab_content.grouping_buttons.items_as_ordered_dict.get(vec.sb.SPORT_DAY_TABS.tomorrow).click()
            has_virtual_banner = self.site.sports_page.tab_content.accordions_list.has_virtual_banner_section()
            self.assertTrue(has_virtual_banner, msg='virtual banner section is not available')
            current_tab = self.site.sports_page.tab_content.grouping_buttons.current
            if current_tab != vec.sb.SPORT_DAY_TABS.future:
                self.site.sports_page.tab_content.grouping_buttons.items_as_ordered_dict.get(vec.sb.SPORT_DAY_TABS.future).click()
            has_virtual_banner = self.site.sports_page.tab_content.accordions_list.has_virtual_banner_section()
            self.assertTrue(has_virtual_banner, msg='virtual banner section is not available')

    def test_006_click_on_the_virtual_american_football_banner(self):
        """
        DESCRIPTION: Click on the Virtual American Football banner.
        EXPECTED: User should be redirected to the Virtual American Football page.
        EXPECTED: User should be able to select selections and place bets successfully.
        """
        if self.device_type == 'desktop':
            play_now_button = self.site.sports_page.tab_content.accordions_list.virtual_banner_section.Play_now_button
            self.assertTrue(play_now_button, msg='"play now" button is not available in virtual banner section')
            play_now_button.click()
            self.site.wait_content_state(state_name='VirtualSports')
            current_url = self.device.get_current_url()
            self.assertIn('virtual-sports/sports/american-football', current_url,
                          msg='could not redirected to the Virtual Basketball sport page.')
