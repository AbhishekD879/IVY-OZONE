import pytest
import tests
import voltron.environments.constants as vec
from crlat_cms_client.utils.exceptions import CMSException
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.utils.waiters import wait_for_result, wait_for_haul


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


def click_on_selection(self):
    odd_btn = ButtonBase(selector='xpath=//*[@data-crlat="betButton"]')
    odd_btn.click()
    return odd_btn


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.table_tennis_specific
@pytest.mark.sports_specific
@pytest.mark.adhoc_suite
@vtest
class Test_C65968732_Verify_the_display_of_details_in_the_Table_Tennis_sport_landing_page_as_per_the_CMS_config(
    BaseBetSlipTest):
    """
    TR_ID: C65968732
    NAME: Verify the display of details  in the Table Tennis sport landing page  as per the CMS config.
    DESCRIPTION: This test case needs to verify the Table Tennis sport landing page display is as per the CMS config
    """
    keep_browser_open = True
    device_name = 'Pixel 2 XL' if not tests.use_browser_stack else tests.default_pixel
    default_date_tab = vec.sb.SPORT_DAY_TABS.today
    TENNIS_CONFIG = {
        "category_id": 59,
        "imageTitle": "Table Tennis",
        "ssCategoryCode": "TABLE_TENNIS",
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

    def all_selection_on_page(self):
        all_buttons_elements: list = self.device.driver.find_elements(
            by='xpath',
            value='//sport-matches-tab//price-odds-button/*[@data-crlat="betButton"]')
        all_selections_on_page = []
        for button in all_buttons_elements:
            all_selections_on_page.append(ButtonBase(web_element=button))
        return all_selections_on_page

    def test_000_preconditions(self):
        """
         PRECONDITIONS: 1. User should have access to oxygen CMS
         PRECONDITIONS: URL: https://cms-api-ui-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/
         PRECONDITIONS: 2. Navigate to Sport pages -> Sport categories -> Table Tennis -> General Sport Configuration.
         PRECONDITIONS: 3.Enable all the required check boxes present out there.
         PRECONDITIONS: 5.Scroll down and make sure to enable all the required tabs Matches, Specials, Outright's, Competitions,Coupons
         PRECONDITIONS: 6.Click on any one of the tab shown below the tab name and add the Market Switcher labels.
         PRECONDITIONS: 7.Under modules tab enable the required modules.
         PRECONDITIONS: 8.Click on save changes button.
         PRECONDITIONS: Note: In Mobile when no events are available Table Tennis sport is not displayed in A-Z sports menu and on clicking Table Tennis  from Sports Ribbon user is navigated back to the Sports Home page.
        """
        sport_categories = self.cms_config.get_sport_categories()

        # Get Table Tennis From All Sport Categories
        self.__class__.tennis = next(
            (sport_category for sport_category in sport_categories if
             sport_category['imageTitle'].strip().upper() == "TABLE TENNIS"), None)

        # Check If Table Tennis is Available in AllSport Categories
        if not self.tennis:
            self.__class__.tennis = self.cms_config.create_sport_category(
                categoryId=self.TENNIS_CONFIG.get("category_id"),
                title=self.TENNIS_CONFIG.get("imageTitle"),
                ssCategoryCode=self.TENNIS_CONFIG.get("ssCategoryCode"),
                **self.TENNIS_CONFIG.get("general_configuration"))
        else:
            self.cms_config.update_sport_category(sport_category_id=self.tennis.get("id"),
                                                  **self.TENNIS_CONFIG.get("general_configuration"))

    def test_001_launch_the_ladbrokes_and_coral_application(self):
        """
        DESCRIPTION: Launch the ladbrokes and Coral application
        EXPECTED: Home page should be loaded successfully
        """
        self.site.login()

    def test_002_click_on_the_table_tennis_sport(self):
        """
        DESCRIPTION: Click on the Table Tennis sport.
        EXPECTED: User should be able to navigate Table Tennis landing page.
        """
        self.site.open_sport(name="Table Tennis")

    def test_003_verify_the_table_tennis_landing_page(self):
        """
        DESCRIPTION: Verify the Table Tennis landing page.
        EXPECTED: Various tabs should be displayed by default Matches tab should be selected with today events.
        EXPECTED: In play widget will display if any events are live when it was enabled in the System Config in CMS.
        EXPECTED: Mobile
        EXPECTED: Matches module is loaded as default with in-play events in it.
        """
        all_sub_tabs_for_table_tennis = self.cms_config.get_sport_tabs(sport_id=self.TENNIS_CONFIG.get("category_id"))
        all_active_tabs = []
        for tab in all_sub_tabs_for_table_tennis:
            tab_available = get_sport_tab_status(tab)
            if tab_available:
                all_active_tabs.append(tab.get('displayName').upper())
        all_sub_tabs_for_table_tennis_fe = self.site.sports_page.tabs_menu.items_as_ordered_dict
        all_sub_tabs_for_table_tennis_fe = [tab.upper() for tab in list(all_sub_tabs_for_table_tennis_fe.keys())
                                            if tab.upper() != "IN-PLAY"]
        self.assertListEqual(all_active_tabs, all_sub_tabs_for_table_tennis_fe)

        current_tab_on_table_tennis_slp = self.site.sports_page.tabs_menu.current
        self.assertEqual(current_tab_on_table_tennis_slp.upper(), "MATCHES",
                         msg=f"Current Active tab is {current_tab_on_table_tennis_slp},"
                             f"Expected tab is MATCHES")

        if self.device_type != "mobile":
            current_date_tab = self.site.sports_page.tab_content.grouping_buttons.current
            self.assertEqual(current_date_tab, self.default_date_tab,
                             msg=f"Current Active tab is {current_date_tab} expected"
                                 f"{self.default_date_tab}")
        has_no_events_label = self.site.sports_page.tab_content.has_no_events_label(expected_result=False)
        self.assertFalse(has_no_events_label, msg="Current Active tab is "
                                                  "contains has no events label")

        active_events_present = len(self.get_active_events_for_category(category_id=59, in_play_event=True,
                                                                        raise_exceptions=False)) != 0
        if active_events_present:
            if self.device_type != "mobile":
                inplay_widget = wait_for_result(lambda: self.site.sports_page.in_play_widget, expected_result=True)
                inplay_widget.scroll_to()
                self.assertTrue(inplay_widget, msg="Inplay Widget is not Present in Matches Tab on Table Tennis")
            else:
                inplay_module = self.site.sports_page.tab_content.in_play_module
                inplay_module.scroll_to()
                self.assertTrue(inplay_module, msg="Inplay Module is not Present in Matches Tab on Table Tennis")

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
                all_events = self.site.sports_page.tab_content.competitions_categories_list
            self.assertTrue(all_events, msg=f"Events not Present in {tab_name} on Table Tennis SLP")

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
        self.test_002_click_on_the_table_tennis_sport()

    def test_007_verify_bet_placements_for_single_multiple_and_complex(self):
        """
        DESCRIPTION: Verify bet placements for Single, Multiple and Complex
        EXPECTED: Bet placements should be successful.
        """
        wait_for_haul(3)
        all_selection_buttons = self.all_selection_on_page()

        # Single Bet
        single_selection_btn = all_selection_buttons.pop()
        single_selection_btn.click()
        wait_for_haul(3)
        if self.device_type == "mobile":
            self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet is not shown')
            quick_bet = self.site.quick_bet_panel
            quick_bet.selection.content.amount_form.input.value = self.bet_amount
            quick_bet.place_bet.click()
            is_bet_receipt_displayed = quick_bet.bet_receipt.is_displayed()
            self.assertTrue(is_bet_receipt_displayed, msg='bet receipt is not diplayed')
            quick_bet.header.close_button.click()
        else:
            wait_for_haul(3)
            self.place_single_bet(number_of_stakes=1)

        # Multiple bets
        all_selection_buttons.pop().click()
        if self.device_type == "mobile":
            self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet is not shown')
            quick_bet = self.site.quick_bet_panel
            quick_bet.header.close_button.click()
        wait_for_haul(2)
        all_selection_buttons.pop()
        all_selection_buttons.pop()
        all_selection_buttons.pop()
        all_selection_buttons.pop().click()
        wait_for_haul(2)
        self.site.header.bet_slip_counter.click()
        self.place_multiple_bet(number_of_stakes=1)
        self.site.bet_receipt.close_button.click()
        wait_for_haul(2)
        # Complex
        all_selection_buttons.pop().click()
        if self.device_type == "mobile":
            self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet is not shown')
            quick_bet = self.site.quick_bet_panel
            quick_bet.header.close_button.click()
            wait_for_haul(3)
        for i in range(2, 10, 2):
            all_selection_buttons.pop(i).click()
        self.site.header.bet_slip_counter.click()
        wait_for_haul(3)
        self.place_multiple_bet(number_of_stakes=4)
        self.site.bet_receipt.close_button.click()
