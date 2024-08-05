import pytest
import tests
import voltron.environments.constants as vec
from crlat_cms_client.utils.exceptions import CMSException
from tests.Common import Common
from tests.base_test import vtest
from voltron.utils.waiters import wait_for_result



def get_sport_tab_status(tab):
    check_events = tab.get("checkEvents")
    has_events = tab.get("hasEvents")
    enabled = tab.get("enabled")
    if not enabled:
        return False
    if check_events is None or has_events is None:
        raise CMSException(
            f'check_events:{check_events} and has_events:{has_events},The paremeters are not present in response')
    if check_events and not has_events:
        return False
    return True


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.american_football_specific
@pytest.mark.sports_specific
@pytest.mark.adhoc_suite
@vtest
class Test_C66007950_Verify_the_display_of_data_on_the_American_Football_sports_landing_page_is_as_per_CMS_config(Common):
    """
    TR_ID: C66007950
    NAME: Verify the display of data on the American Football sports landing page is as per CMS config.
    DESCRIPTION: This test case is to validate sports landing page data displaying for the American Football sport is as per CMS configuration.
    PRECONDITIONS: 1.User should have access to oxygen CMS
    PRECONDITIONS: URL: https://cms-api-ui-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/
    PRECONDITIONS: American Football entry points
    PRECONDITIONS: 2.Navigate to sport pages&gt;sport categories&gt;American Football&gt;General sport configuration.
    PRECONDITIONS: 3.Enable all the required check boxes present out there.
    PRECONDITIONS: 4.Enter all the mandatory fields.
    PRECONDITIONS: Note : Add primary markets there.
    PRECONDITIONS: |Match Betting|,
    PRECONDITIONS: |Match Betting 3-Way|,
    PRECONDITIONS: |Frames 1-4 Winner|,
    PRECONDITIONS: |Total Frames|,
    PRECONDITIONS: |Frame X Winner|,
    PRECONDITIONS: |Total Frames Over/Under|
    PRECONDITIONS: 5.Scroll down and make sure to enable all the tabs(Today/Tomorrow,Future Matches,Specials, Outright's).
    PRECONDITIONS: 6.Click on any one of the tab shown below the tab name and add the market switcher labels.
    PRECONDITIONS: 7.Under modules tab enable the required modules.
    PRECONDITIONS: 8.Click on save changes button.
    PRECONDITIONS: Note: In mobile when no events are available American Football sport is not displayed in A-Z sports menu and on clicking American Football from Sports ribbon user is navigated back to the sports homepage.
    """
    keep_browser_open = True
    device_name = 'Pixel 2 XL' if not tests.use_browser_stack else tests.default_pixel
    default_date_tab = vec.sb.SPORT_DAY_TABS.today
    American_Football_CONFIG = {
        "category_id": 1,
        "imageTitle": "American Football",
        "ssCategoryCode": "AMERICAN_FB",
        "general_configuration": {
            "disabled": False,
            "inApp": True,
            "showInPlay": True,
            "showInHome": True,
            "showInAZ": True,
            "showInMenu": True,
            "showScoreboard": True,
            "showFreeRideBanner": True,
            "isTopSport": True
        }
    }
    def test_000_preconditions(self):
        """
         PRECONDITIONS: 1. User should have access to oxygen CMS
         PRECONDITIONS: URL: https://cms-api-ui-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/
         PRECONDITIONS: 2. Navigate to Sport pages -> Sport categories -> BASKETBALL -> General Sport Configuration.
         PRECONDITIONS: 3.Enable all the required check boxes present out there.
         PRECONDITIONS: 5.Scroll down and make sure to enable all the required tabs Matches, Specials, Outright's, Competitions,Coupons
         PRECONDITIONS: 6.Click on any one of the tab shown below the tab name and add the Market Switcher labels.
         PRECONDITIONS: 7.Under modules tab enable the required modules.
         PRECONDITIONS: 8.Click on save changes button.
         PRECONDITIONS: Note: In Mobile when no events are available BASKETBALL sport is not displayed in A-Z sports menu and on clicking BASKETBALL  from Sports Ribbon user is navigated back to the Sports Home page.
        """
        am_football_sport = self.get_sport_title(category_id=self.ob_config.american_football_config.category_id)

        # Check If American Football is Available in AllSport Categories
        if not am_football_sport:
            self.cms_config.create_sport_category(
                categoryId=self.American_Football_CONFIG.get("category_id"),
                title=self.American_Football_CONFIG.get("imageTitle"),
                ssCategoryCode=self.American_Football_CONFIG.get("ssCategoryCode"),
                **self.American_Football_CONFIG.get("general_configuration"))
        else:
            sport_categories = self.cms_config.get_sport_categories()
            sport_category_id = next((category.get('id') for category in sport_categories if category['categoryId'] == self.ob_config.american_football_config.category_id), None)
            self.cms_config.update_sport_category(sport_category_id=sport_category_id,
                                                  **self.American_Football_CONFIG.get("general_configuration"))

    def test_001_launch_the_ladbrokescoral_application(self):
        """
        DESCRIPTION: Launch the Ladbrokes/Coral application.
        EXPECTED: Application should be loaded successfully and by default user is on home page
        """
        self.site.wait_content_state(state_name='Homepage')

    def test_002_desktop_under_a_z_sport_menu_click_on_american_football(self):
        """
        DESCRIPTION: Desktop: Under A-Z Sport menu, click on American Football.
        EXPECTED: User should be navigated to the  American Football  page and by default user should be in Today/Tomorrow tab.
        """
        self.navigate_to_page(name='sport/american-football')
        self.site.wait_content_state('american-football')

    def test_003_mobile_navigate_to_sports_ribbon_or_from_a_z_sports_click_on_american_football(self):
        """
        DESCRIPTION: Mobile: Navigate to sports ribbon or from A-Z Sports, click on American Football.
        EXPECTED: User should be navigated to the American Football page and by default user is in Today/Tomorrow tab.
        """
        all_sub_tabs_for_american_football = self.cms_config.get_sport_tabs(sport_id=self.American_Football_CONFIG.get("category_id"))
        all_active_tabs = []
        for tab in all_sub_tabs_for_american_football:
            tab_available = get_sport_tab_status(tab)
            if tab_available:
                all_active_tabs.append(tab.get('displayName').upper())
        all_sub_tabs_for_american_football_fe = self.site.sports_page.tabs_menu.items_as_ordered_dict
        all_sub_tabs_for_american_football_fe = [tab.upper() for tab in list(all_sub_tabs_for_american_football_fe.keys())
                                            if tab.upper() != "IN-PLAY"]
        if self.device_type == 'mobile':
            self.assertListEqual(all_active_tabs, all_sub_tabs_for_american_football_fe)

        if "MATCHES" in all_active_tabs:
            current_tab_on_american_football_slp = self.site.sports_page.tabs_menu.current
            self.assertEqual(current_tab_on_american_football_slp.upper(), "MATCHES",
                             msg=f"Current Active tab is {current_tab_on_american_football_slp},"
                                 f"Expected tab is MATCHES")

            if self.device_type != "mobile":
                current_date_tab = self.site.sports_page.tab_content.grouping_buttons.current
                self.assertEqual(current_date_tab, self.default_date_tab,
                                 msg=f"Current Active tab is {current_date_tab} expected"
                                     f"{self.default_date_tab}")

        active_events_present = len(self.get_active_events_for_category(category_id=self.ob_config.american_football_config.category_id, in_play_event=True,
                                                                        raise_exceptions=False)) != 0
        if self.device_type == "desktop" and active_events_present:
            inplay_widget = wait_for_result(lambda: self.site.sports_page.in_play_widget, expected_result=True)
            self.assertTrue(inplay_widget, msg="Inplay Widget is not Present in Matches Tab on American football")
            inplay_widget.scroll_to()

    def test_004_navigate_to_other_tabs_future_matches_outrights_specials(self):
        """
        DESCRIPTION: Navigate to other tabs (Future Matches, Outrights, Specials)
        EXPECTED: Events should be loaded successfully, if there are no events "No events found"  message is shown.
        """
        for tab_name, tab in self.site.sports_page.tabs_menu.items_as_ordered_dict.items():
            tab.click()
            if tab_name != "COMPETITIONS":
                no_event_label = self.site.sports_page.tab_content.has_no_events_label()
                if no_event_label:
                    self._logger.info("Events Not Available for %s", tab_name)
                    continue
                else:
                    all_events = self.site.sports_page.tab_content.accordions_list
            else:
                all_events = self.site.sports_page.tab_content.competitions_categories_list
            self.assertTrue(all_events, msg=f"Events not Present in {tab_name} on American football SLP")
        self.navigate_to_page("Homepage")
        self.site.wait_content_state('HomePage', timeout=5)


    def test_005_verify_the_created_modules_for_sport_category_page_from_cms_login_to_the_application_with_a_valid_userrepeat_all_the_above_steps(self):
        """
        DESCRIPTION: Verify the created modules for sport category page from CMS. Login to the application with a valid user.Repeat all the above steps.
        EXPECTED: It should work as expected.
        """
        self.site.login()
        self.test_002_desktop_under_a_z_sport_menu_click_on_american_football()
        self.test_003_mobile_navigate_to_sports_ribbon_or_from_a_z_sports_click_on_american_football()
        self.test_004_navigate_to_other_tabs_future_matches_outrights_specials()
