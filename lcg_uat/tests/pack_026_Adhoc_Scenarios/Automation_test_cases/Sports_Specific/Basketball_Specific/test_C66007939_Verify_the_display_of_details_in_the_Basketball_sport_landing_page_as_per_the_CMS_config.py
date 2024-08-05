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
@pytest.mark.basketball_specific
@pytest.mark.sports_specific
@pytest.mark.adhoc_suite
@vtest
class Test_C66007939_Verify_the_display_of_details_in_the_Basketball_sport_landing_page_as_per_the_CMS_config(Common):
    """
    TR_ID: C66007939
    NAME: Verify the display of details in the Basketball sport landing page as per the CMS config.
    DESCRIPTION: This test case validates the details on the Basketball landing page is as per the CMS configuration.
    PRECONDITIONS: 1.User should have access to oxygen CMS
    PRECONDITIONS: URL: https://cms-api-ui-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/
    PRECONDITIONS: 2.Navigate to Sport pages -&gt; Sport categories -&gt; Basketball -&gt; General Sport Configuration.
    PRECONDITIONS: 3.Enable all the required check boxes present out there.
    PRECONDITIONS: 5.Scroll down and make sure to enable all the required tabs Matches, Specials, Outright's, Competitions,Coupons
    PRECONDITIONS: 6.Click on any one of the tab shown below the tab name and add the Market Switcher labels.
    PRECONDITIONS: 7.Under modules tab enable the required modules.
    PRECONDITIONS: 8.Click on save changes button.
    PRECONDITIONS: Note:In Mobile when no events are available Basketball sport is not displayed in A-Z sports menu and on clicking Basketball  from Sports Ribbon user is navigated back to the Sports Home page.
    """
    keep_browser_open = True
    device_name = 'Pixel 2 XL' if not tests.use_browser_stack else tests.default_pixel
    default_date_tab = vec.sb.SPORT_DAY_TABS.today
    BASKETBALL_CONFIG = {
        "category_id": 6,
        "imageTitle": "Basketball",
        "ssCategoryCode": "BASKETBALL",
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
        sport_categories = self.cms_config.get_sport_categories()

        # Get BASKETBALL From All Sport Categories
        self.__class__.basketball = next(
            (sport_category for sport_category in sport_categories if
             sport_category['imageTitle'].strip().upper() == "BASKETBALL"), None)

        # Check If BasketBall is Available in AllSport Categories
        if not self.basketball:
            self.__class__.basketball = self.cms_config.create_sport_category(
                categoryId=self.BASKETBALL_CONFIG.get("category_id"),
                title=self.BASKETBALL_CONFIG.get("imageTitle"),
                ssCategoryCode=self.BASKETBALL_CONFIG.get("ssCategoryCode"),
                **self.BASKETBALL_CONFIG.get("general_configuration"))
        else:
            self.cms_config.update_sport_category(sport_category_id=self.basketball.get("id"),
                                                  **self.BASKETBALL_CONFIG.get("general_configuration"))

    def test_001_launch_the_ladbrokes_and_coral_application(self):
        """
        DESCRIPTION: Launch the Ladbrokes and Coral application
        EXPECTED: Home page should be loaded successfully
        """
        self.site.login()

    def test_002_click_on_the_basketball_sport(self):
        """
        DESCRIPTION: Click on the Basketball sport.
        EXPECTED: User should be able to navigate Basketball landing page.
        """
        self.site.open_sport(name="basketball")

    def test_003_verify_the_basketball_landing_page(self):
        """
        DESCRIPTION: Verify the Basketball landing page.
        EXPECTED: Various tabs should be displayed by default Matches tab should be selected with today events.
        EXPECTED: In play widget will display if any events are live when it was enabled in the System Config in CMS.
        EXPECTED: Mobile
        EXPECTED: Matches module is loaded as default with in-play events in it.
        """
        all_sub_tabs_for_basketball = self.cms_config.get_sport_tabs(sport_id=self.BASKETBALL_CONFIG.get("category_id"))
        all_active_tabs = []
        for tab in all_sub_tabs_for_basketball:
            tab_available = get_sport_tab_status(tab)
            if tab_available:
                all_active_tabs.append(tab.get('displayName').upper())
        all_sub_tabs_for_basketball_fe = self.site.sports_page.tabs_menu.items_as_ordered_dict
        all_sub_tabs_for_basketball_fe = [tab.upper() for tab in list(all_sub_tabs_for_basketball_fe.keys())]
        self.assertListEqual(all_active_tabs, all_sub_tabs_for_basketball_fe)

        current_tab_on_basketball_slp = self.site.sports_page.tabs_menu.current
        self.assertEqual(current_tab_on_basketball_slp.upper(), "MATCHES",
                         msg=f"Current Active tab is {current_tab_on_basketball_slp},"
                             f"Expected tab is MATCHES")

        if self.device_type != "mobile":
            current_date_tab = self.site.sports_page.tab_content.grouping_buttons.current
            self.assertEqual(current_date_tab, self.default_date_tab,
                             msg=f"Current Active tab is {current_date_tab} expected"
                                 f"{self.default_date_tab}")
        has_no_events_label = self.site.sports_page.tab_content.has_no_events_label(expected_result=False)
        self.assertFalse(has_no_events_label, msg="Current Active tab is "
                                                  "contains has no events label")

        active_events_present = len(self.get_active_events_for_category(category_id=6, in_play_event=True,
                                                                        raise_exceptions=False)) != 0
        if active_events_present:
            if self.device_type != "mobile":
                inplay_widget = wait_for_result(lambda: self.site.sports_page.in_play_widget, expected_result=True)
                inplay_widget.scroll_to()
                self.assertTrue(inplay_widget, msg="Inplay Widget is not Present in Matches Tab on BASKETBALL")
            # else:
            #     inplay_module = self.site.sports_page.tab_content.in_play_module
            #     inplay_module.scroll_to()
            #     self.assertTrue(inplay_module, msg="Inplay Module is not Present in Matches Tab on BASKETBALL")

    def test_004_navigate_to_other_tabs_future_matches_outrights_specials(self):
        """
        DESCRIPTION: Navigate to other tabs (Future Matches, Outrights, Specials)
        EXPECTED: Events should be loaded successfully.
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
                if self.device_type == "mobile":
                    all_events = self.site.sports_page.tab_content.competitions_categories
                else:
                    all_events = self.site.sports_page.tab_content.competitions_categories_list
            self.assertTrue(all_events, msg=f"Events not Present in {tab_name} on BasketBall SLP")

    def test_005_verify_the_created_modules_for_sport_category_page_from_the_cms(self):
        """
        DESCRIPTION: Verify the created modules for Sport Category page from the CMS.
        EXPECTED: Modules should be loaded as per the CMS configuration.
        """
        # This test Step cannot be automated because we cannot confirm the presence of modules like highlights
        # carousel,surface bet, and quick link with valid parameters in CMS. If these elements are not configured with
        # valid parameters, then they would not be visible on the front-end. Without verifying their visibility on the
        # front end,we cannot verify their order. For example, even if highlights carousel is created in CMS with valid
        # 'from date and 'to date' and visible is true but if the event id inside it is suspended then highlights
        # carousel would not be visible in front end.

    def test_006_verify_by_clicking_on_the_backward_chevron_beside_sport_header(self):
        """
        DESCRIPTION: Verify by clicking on the backward chevron beside sport header
        EXPECTED: Desktop
        EXPECTED: User should be redirected to Home page.
        EXPECTED: User should be redirected to sport navigation page
        """
        if self.device_type == "mobile" and tests.settings.brand == "ladbrokes":
            back_button = self.site.header.back_button
            back_button.click()
        else:
            self.site.sports_page.back_button_click()
        self.site.wait_content_state(state_name="Home")
        self.test_002_click_on_the_basketball_sport()

    def test_007_verify_bet_placements_for_single_multiple_and_complex(self):
        """
        DESCRIPTION: Verify bet placements for Single, Multiple and Complex
        EXPECTED: Bet placements should be successful.
        """
        # covered in C60089508 testcase
