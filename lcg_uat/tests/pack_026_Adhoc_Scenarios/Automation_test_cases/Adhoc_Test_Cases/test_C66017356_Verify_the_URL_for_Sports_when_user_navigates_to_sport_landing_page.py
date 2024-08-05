from collections import OrderedDict
import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.pages.shared import get_driver
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result, wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.adhoc_suite
@pytest.mark.back_button
@pytest.mark.navigation
@pytest.mark.desktop
@pytest.mark.adhoc24thJan24
@pytest.mark.other
@vtest
class Test_C66017356_Verify_the_URL_for_Sports_when_user_navigates_to_sport_landing_page(Common):
    """
    TR_ID: C66017356
    NAME: Verify the URL for Sports when user navigates to sport landing page
    DESCRIPTION: Verify the URL for Sports(Tire1 & Tier2) when user navigates to sport landing page
    PRECONDITIONS: In CMS-&gt;Sport Category-&gt;Football-&gt;Target Uri-&gt;sport/football
    """
    keep_browser_open = True

    def handle_accordions_and_events(self):
        accordion_name, accordion = self.site.sports_page.tab_content.accordions_list.first_item
        event_name, event = accordion.first_item
        event.click()

    def get_enabled_tabs(self, sport_id):
        all_sport_tabs = self.cms_config.get_sport_tabs(sport_id=sport_id)
        self.__class__.expected_sports_tabs = []
        for tab in all_sport_tabs:
            if tab['enabled'] and not (tab['checkEvents'] and not tab['hasEvents']):
                self.expected_sports_tabs.append(tab['displayName'].upper())
        matches_tab_name = self.get_sport_tab_name(
            self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches, category_id=sport_id)
        if matches_tab_name not in self.expected_sports_tabs:
            raise CmsClientException(f'Matches tab is not enabled for for Sport ID {sport_id} in CMS')


    def test_001_launch_the_front_end_application(self):
        """
        DESCRIPTION: Launch the front end application
        EXPECTED: Homepage is loaded successfully
        """
        pass

    def test_002_navigate_to_football_landing_page(self):
        """
        DESCRIPTION: Navigate to Football landing page
        EXPECTED: Football landing page is successfully launched and user is on 'Matches' tab
        EXPECTED: The Football URL is displayed in the below format: 'https://sports.ladbrokes.com/sport/football'
        """
        self.site.open_sport('Football')
        self.site.wait_content_state(state_name='football')

    def test_003_navigate_to_any_other_sub_tabs_like_inplaycompetitionsout_rightsspecials_and_come_back_to_matches_tab_by_using_browser_back_button(self, sport_type='football', sport_id=16):
        """
        DESCRIPTION: Navigate to any other sub tabs like: Inplay/Competitions/Out rights/Specials and come back to 'Matches' tab by using browser back button
        EXPECTED: User successfully navigated to other tabs
        EXPECTED: The Football URL is displayed in below format: 'https://sports.ladbrokes.com/sport/football' once came back to Matches tab by using browser back button
        """
        actual_sports_tabs = self.site.sports_page.tabs_menu.items_as_ordered_dict
        self.assertTrue(actual_sports_tabs, f'There is no tabs available for {sport_type}')
        for tab_name, tab in list(actual_sports_tabs.items()):
            if tab_name.upper() == 'MATCHES':
                continue
            tab.click()
            if tab_name.upper().strip() == " Trending ":
                wait_for_haul(3)
            get_driver().back()
            actual_url = self.device.get_current_url()
            expected_url = f'https://{tests.HOSTNAME}/sport/{sport_type}'
            self.assertEqual(actual_url, expected_url, msg=f'"{actual_url}" doesnt match with "{expected_url}"')

    def test_004_navigate_to_any_edp_page_and_come_back_by_using_browser_back_button(self, sport_type='football'):
        """
        DESCRIPTION: Navigate to any EDP page and come back by using browser back button
        EXPECTED: User successfully navigated to EDP page
        EXPECTED: The Football URL is displayed in below format: 'https://sports.ladbrokes.com/sport/football' once came back to Matches tab by using browser back button
        """
        self.handle_accordions_and_events()
        self.site.wait_content_state('EventDetails')
        get_driver().back()
        actual_url = self.device.get_current_url()
        expected_url = f'https://{tests.HOSTNAME}/sport/{sport_type}'
        self.assertEqual(actual_url, expected_url, msg=f'"{actual_url}" doesnt match with "{expected_url}"')

    def test_005_navigate_to_any_edp_page_and_come_back_by_using_football_page_back_button(self, sport_type='football'):
        """
        DESCRIPTION: Navigate to any EDP page and come back by using Football page back button
        EXPECTED: User successfully navigated to EDP page
        EXPECTED: The Football URL is displayed in below format: 'https://sports.ladbrokes.com/sport/football' once came back to Matches tab by using browser back button
        """
        self.handle_accordions_and_events()
        self.site.wait_content_state('EventDetails')
        wait_for_result(lambda: self.site.has_back_button, bypass_exceptions=VoltronException)
        self.site.back_button.click()
        actual_url = self.device.get_current_url()
        expected_url = f'https://{tests.HOSTNAME}/sport/{sport_type}'
        self.assertEqual(actual_url, expected_url, msg=f'"{actual_url}" doesnt match with "{expected_url}"')

    def test_006_again_navigate_to_any_edp_page_and_come_back_by_clicking_on_football_breadcrumb(self, sport_type='football', sport_name='Football'):
        """
        DESCRIPTION: Again Navigate to any EDP page and come back by clicking on Football breadcrumb
        EXPECTED: User successfully navigated to EDP page
        EXPECTED: The Football URL is displayed in below format: 'https://sports.ladbrokes.com/sport/football' once came back to Matches tab by clicking on football breadcrumb
        """
        if self.device_type == 'desktop':
            self.handle_accordions_and_events()
            breadcrumbs = OrderedDict((key.strip(), self.site.sport_event_details.breadcrumbs.items_as_ordered_dict[key])
                                      for key in self.site.sport_event_details.breadcrumbs.items_as_ordered_dict)
            breadcrumbs[sport_name].link.click()
            actual_url = self.device.get_current_url()
            expected_url = f'https://{tests.HOSTNAME}/sport/{sport_type}'
            self.assertEqual(actual_url, expected_url, msg=f'"{actual_url}" doesnt match with "{expected_url}"')

    def test_007_now_navigate_to_any_other_sub_tabs_like_inplaycompetitionsout_rightsspecials_and_come_back_to_matches_tab_by_clicking_on_football_breadcrumb(self, sport_type='football',  sport_name='Football'):
        """
        DESCRIPTION: Now Navigate to any other sub tabs like: Inplay/Competitions/Out rights/Specials and come back to 'Matches' tab by clicking on Football breadcrumb
        EXPECTED: User successfully navigated to other tabs
        EXPECTED: The Football URL is displayed in below format once came back to Matches tab by clicking on football breadcrumb:
        EXPECTED: Desktop: 'https://sports.ladbrokes.com/sport/football/matches/today'
        EXPECTED: Mobile: 'https://sports.ladbrokes.com/sport/football/matches'
        """
        if self.device_type == 'desktop':
            actual_sports_tabs = self.site.sports_page.tabs_menu.items_as_ordered_dict
            self.assertTrue(actual_sports_tabs, f'tabs are not available for {sport_type}')
            for tab_name, tab in actual_sports_tabs.items():
                if tab_name.upper() == 'MATCHES':
                    continue
                tab.click()
                raw_breadcrumbs = wait_for_result(lambda : self.site.sports_page.breadcrumbs.items_as_ordered_dict,timeout=2, bypass_exceptions=VoltronException)
                breadcrumbs = OrderedDict((key.strip(), value) for key, value in raw_breadcrumbs.items())
                breadcrumbs[sport_name].link.click()
                actual_url = self.device.get_current_url()
                if self.device_type == 'desktop':
                    expected_url = f'https://{tests.HOSTNAME}/sport/{sport_type}/matches/today'
                else:
                    expected_url = f'https://{tests.HOSTNAME}/sport/{sport_type}/matches'
                self.assertEqual(actual_url, expected_url, msg=f'"{actual_url}" doesnt match with "{expected_url}"')

    def test_008_navigate_to_homepage_and_again_navigate_to_football_page_then_refresh_the_page(self, sport_type='Football'):
        """
        DESCRIPTION: Navigate to homepage and again navigate to football page then refresh the page
        EXPECTED: The Football URL is displayed in below format: 'https://sports.ladbrokes.com/sport/football'
        """
        self.navigate_to_page('/')
        self.site.open_sport(sport_type)
        self.site.wait_content_state(state_name=sport_type.lower())
        self.device.driver.refresh()
        actual_url = self.device.get_current_url()
        expected_url = f'https://{tests.HOSTNAME}/sport/{sport_type.lower()}'
        self.assertEqual(actual_url, expected_url, msg=f'"{actual_url}" doesnt match with "{expected_url}"')

    def test_009_duplicate_the_page_and_check_the_other_duplicated_page(self):
        """
        DESCRIPTION: Duplicate the page and check the other duplicated page
        EXPECTED: The Football URL is displayed in below format: 'https://sports.ladbrokes.com/sport/football'
        """
        #cannot automate

    def test_010_edit_the_football_landing_page_url_to_httpssportsladbrokescomsportfootballtest(self, sport_type='football'):
        """
        DESCRIPTION: Edit the football landing page URL to: 'https://sports.ladbrokes.com/sport/football/test'
        EXPECTED: The Football URL is displayed in below format:
        EXPECTED: Desktop: 'https://sports.ladbrokes.com/sport/football/matches/today'
        EXPECTED: Mobile: 'https://sports.ladbrokes.com/sport/football/matches'
        """
        self.navigate_to_page(f'sport/{sport_type}/test')
        actual_url = self.device.get_current_url()
        if self.device_type == 'desktop':
            expected_url = f'https://{tests.HOSTNAME}/sport/{sport_type}/matches/today'
        else:
            expected_url = f'https://{tests.HOSTNAME}/sport/{sport_type}/matches'
        self.assertEqual(actual_url, expected_url, msg=f'"{actual_url}" doesnt match with "{expected_url}"')

    def test_011_edit_the_football_landing_page_url_to_httpssportsladbrokescomsportfoottest(self):
        """
        DESCRIPTION: Edit the football landing page URL to: 'https://sports.ladbrokes.com/sport/foottest'
        EXPECTED: User is navigated to Homepage
        """
        self.navigate_to_page(f'sport/foottest')
        self.site.wait_content_state('Home')

    def test_012_navigate_to_football_ampgtany_other_sub_tabs_like_inplaycompetitionsout_rightsspecials_and_come_back_to_matches_tab_by_directly_clicking_on_matches_tab(self, sport_type='Football'):
        """
        DESCRIPTION: Navigate to Football-&amp;gt;any other sub tabs like: Inplay/Competitions/Out rights/Specials and come back to 'Matches' tab by directly clicking on 'Matches' tab
        EXPECTED: User navigates to other tab successfully
        EXPECTED: The Football URL is displayed in below format:
        EXPECTED: Desktop: 'https://sports.ladbrokes.com/sport/football/matches/today'
        EXPECTED: Mobile: 'https://sports.ladbrokes.com/sport/football/matches'
        """
        self.site.open_sport(sport_type)
        self.site.wait_content_state(state_name=sport_type.lower())
        actual_sports_tabs = self.site.sports_page.tabs_menu.items_as_ordered_dict
        matches_tab = next((tab for tab_name, tab in actual_sports_tabs.items() if tab_name.upper() == 'MATCHES'), None)
        self.assertTrue(matches_tab, f'Matches Tab is not available')
        for tab_name, tab in actual_sports_tabs.items():
            if tab_name.upper() == 'MATCHES':
                continue
            tab.click()
            matches_tab.click()
            wait_for_haul(2)
            actual_url = self.device.get_current_url()
            if self.device_type == 'desktop':
                expected_url = f'https://{tests.HOSTNAME}/sport/{sport_type.lower()}/matches/today'
            else:
                expected_url = f'https://{tests.HOSTNAME}/sport/{sport_type.lower()}/matches'
            self.assertEqual(actual_url, expected_url,
                             msg=f'"{actual_url}" doesnt match with "{expected_url}"')

    def test_013_repeat_above_all_steps_by_logging_into_the_front_end_application(self):
        """
        DESCRIPTION: Repeat above all steps by logging into the front end application
        EXPECTED: The result should be the same as above.
        """
        self.navigate_to_page('/')
        self.site.login()
        self.test_001_launch_the_front_end_application()
        self.test_002_navigate_to_football_landing_page()
        self.test_003_navigate_to_any_other_sub_tabs_like_inplaycompetitionsout_rightsspecials_and_come_back_to_matches_tab_by_using_browser_back_button()
        self.test_004_navigate_to_any_edp_page_and_come_back_by_using_browser_back_button()
        self.test_005_navigate_to_any_edp_page_and_come_back_by_using_football_page_back_button()
        self.test_006_again_navigate_to_any_edp_page_and_come_back_by_clicking_on_football_breadcrumb()
        self.test_007_now_navigate_to_any_other_sub_tabs_like_inplaycompetitionsout_rightsspecials_and_come_back_to_matches_tab_by_clicking_on_football_breadcrumb()
        self.test_008_navigate_to_homepage_and_again_navigate_to_football_page_then_refresh_the_page()
        self.test_010_edit_the_football_landing_page_url_to_httpssportsladbrokescomsportfootballtest()
        self.test_011_edit_the_football_landing_page_url_to_httpssportsladbrokescomsportfoottest()
        self.test_012_navigate_to_football_ampgtany_other_sub_tabs_like_inplaycompetitionsout_rightsspecials_and_come_back_to_matches_tab_by_directly_clicking_on_matches_tab()

    def test_014_repeat_above_all_steps_for_both_tier_1_amp_tier_2_sports(self):
        """
        DESCRIPTION: Repeat above all steps for both Tier-1 &amp; Tier-2 Sports
        EXPECTED: The result should be the same as above.
        """
        self.navigate_to_page('/')
        self.site.open_sport('Basketball')
        self.site.wait_content_state(state_name='Basketball')
        self.test_003_navigate_to_any_other_sub_tabs_like_inplaycompetitionsout_rightsspecials_and_come_back_to_matches_tab_by_using_browser_back_button(sport_type='basketball', sport_id=6)
        self.test_004_navigate_to_any_edp_page_and_come_back_by_using_browser_back_button(sport_type='basketball')
        self.test_005_navigate_to_any_edp_page_and_come_back_by_using_football_page_back_button(sport_type='basketball')
        self.test_006_again_navigate_to_any_edp_page_and_come_back_by_clicking_on_football_breadcrumb(sport_type='basketball', sport_name='Basketball')
        self.test_007_now_navigate_to_any_other_sub_tabs_like_inplaycompetitionsout_rightsspecials_and_come_back_to_matches_tab_by_clicking_on_football_breadcrumb(sport_type='basketball', sport_name='Basketball')
        self.test_008_navigate_to_homepage_and_again_navigate_to_football_page_then_refresh_the_page(sport_type='basketball')
        self.test_010_edit_the_football_landing_page_url_to_httpssportsladbrokescomsportfootballtest(sport_type='basketball')
        self.test_011_edit_the_football_landing_page_url_to_httpssportsladbrokescomsportfoottest()
        self.test_012_navigate_to_football_ampgtany_other_sub_tabs_like_inplaycompetitionsout_rightsspecials_and_come_back_to_matches_tab_by_directly_clicking_on_matches_tab(sport_type='basketball')
