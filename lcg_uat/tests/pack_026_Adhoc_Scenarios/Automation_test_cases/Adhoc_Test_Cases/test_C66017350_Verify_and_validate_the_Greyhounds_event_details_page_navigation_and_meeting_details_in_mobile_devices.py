import random
import pytest
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
import voltron.environments.constants as vec
from voltron.utils.waiters import wait_for_result, wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.mobile_only
@pytest.mark.adhoc_suite
@pytest.mark.greyhounds
@pytest.mark.betslip
@pytest.mark.bet_placement
@pytest.mark.adhoc24thJan24
@pytest.mark.reg_172_fix
@vtest
class Test_C66017350_Verify_and_validate_the_Greyhounds_event_details_page_navigation_and_meeting_details_in_mobile_devices(BaseBetSlipTest):
    """
    TR_ID: C66017350
    NAME: Verify and validate the Greyhounds event details page navigation and meeting details in mobile devices.
    DESCRIPTION: Verify and validate the Greyhounds EDP navigation and meeting details in mobile devices.
    PRECONDITIONS: 1) User should have oxygen CMS access
    PRECONDITIONS: CMS Link--https://cms-api-ui-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/
    PRECONDITIONS: user : ozoneqa@coral.co.uk   Password:Admin
    PRECONDITIONS: 2)Configuration for Greyhounds racing in the CMS below-
    PRECONDITIONS: i) CMS ->Sports->Sports Category-> Greyhounds-Active
    PRECONDITIONS: ii) CMS ->Menus->Header SubMenus-> Greyhounds-Active
    PRECONDITIONS: iii) CMS ->Sports->Sports Category-> Greyhounds-Module-races like (UK and Irish races, International Races)-Enabled
    PRECONDITIONS: 3) Configuration for Greyhounds racing edp markets and data below
    PRECONDITIONS: i) CMS->System configuration->Structure->Search in "Search for system config" box as "RacingDataHub"->Enabled Checkbox for isEnabledForGreyhound-> Save Changes
    PRECONDITIONS: ii) CMS->Racing EDP markets->Markets should be enabled
    """
    keep_browser_open = True

    def add_selections_for_bet_placement(self, bet_type):
        quick_bet_handled = 0
        event_off_times_list = self.site.greyhound_event_details.tab_content.event_off_times_list.items_as_ordered_dict
        event_off_times = list(event_off_times_list.keys())
        current_event_off_time = self.site.greyhound_event_details.tab_content.event_off_times_list.selected_item
        index_current_event_off_time = event_off_times.index(current_event_off_time)
        i = index_current_event_off_time+1 if bet_type == 'single' else index_current_event_off_time+3
        for event_off_time_name,event_off_time in list(event_off_times_list.items())[index_current_event_off_time:i]:
            if current_event_off_time != event_off_time_name:
                self.site.greyhound_event_details.tab_content.event_off_times_list.select_off_time(event_off_time_name)
            current_tab = self.site.greyhound_event_details.tab_content.event_markets_list.market_tabs_list.current
            if current_tab != vec.racing.RACING_EDP_DEFAULT_MARKET_TAB:
                event_market_list = self.site.greyhound_event_details.tab_content.event_markets_list
                event_market_list.market_tabs_list.open_tab(vec.racing.RACING_EDP_DEFAULT_MARKET_TAB)
            sections = self.site.greyhound_event_details.tab_content.event_markets_list.items_as_ordered_dict
            self.assertTrue(sections, msg=f'No sections found for racing event tab')
            section_name, section = list(sections.items())[0]
            outcomes = list(section.items_as_ordered_dict.items())
            self.assertTrue(outcomes, msg=f'No outcome was found in section: "{section_name}"')
            outcome_name,outcome = outcomes[0]
            outcome.bet_button.click()
            if quick_bet_handled == 0 :
                self.site.quick_bet_panel.header.close_button.click()
                quick_bet_handled+=1
        self.site.open_betslip()
        self.assertTrue(self.site.has_betslip_opened(), msg='Failed to open Betslip')

    def test_000_pre_conditions(self):
        """
        PRECONDITIONS: i) CMS ->Sports->Sports Category-> Greyhounds-Active
        PRECONDITIONS: ii) CMS ->Menus->Header SubMenus-> Greyhounds-Active
        PRECONDITIONS: iii) CMS ->Sports->Sports Category-> Greyhounds-Module-races like (UK and Irish races, International Races)-Enabled
        PRECONDITIONS: 3) Configuration for Greyhounds racing edp markets and data below
        PRECONDITIONS: i) CMS->System configuration->Structure->Search in "Search for system config" box as "RacingDataHub"->Enabled Checkbox for isEnabledForGreyhound-> Save Changes
        PRECONDITIONS: ii) CMS->Racing EDP markets->Markets should be enabled
        """
        category_id = self.ob_config.greyhound_racing_config.category_id
        sport_categories = self.cms_config.get_sport_categories()
        GH_id, self.__class__.GH_title = next(((category.get('id'),category.get('imageTitle')) for category in sport_categories if category.get('categoryId') == category_id), None)
        GH_config = self.cms_config.get_sport_category(sport_category_id = GH_id)
        if GH_config.get('disabled') :
            self.cms_config.update_sport_category(sport_category_id = GH_id, disabled = False)
        sport_modules = self.cms_config.get_sport_module(sport_id = category_id, module_type = "RACING_MODULE")
        uk_and_irish_races_disabled, uk_and_irish_races = next(((sport_module.get('disabled'), sport_module) for sport_module in sport_modules if sport_module.get('racingConfig')['type'] == 'UK_AND_IRISH_RACES'), None)
        self.__class__.uk_and_irish_race_module_name = uk_and_irish_races.get('title')
        international_races_disabled, international_races = next(((sport_module.get('disabled'), sport_module) for sport_module in sport_modules if sport_module.get('title') == "International Races"), None)
        if uk_and_irish_races_disabled:
            self.cms_config.change_sport_module_state(sport_module=uk_and_irish_races)
        if international_races_disabled:
            self.cms_config.change_sport_module_state(sport_module = international_races)
        sub_menus = self.cms_config.get_header_submenus()
        GH_submenu = next((sub_menu for sub_menu in sub_menus if sub_menu.get('linkTitle') == "Greyhounds"), None)
        GH_submenu_disabled = GH_submenu.get('disabled')
        if GH_submenu_disabled:
            self.cms_config.update_header_submenu(header_submenu_id = GH_submenu.get('id'), disabled = False)
        system_configuration = self.cms_config.get_system_configuration_structure()
        if system_configuration.get('RacingDataHub') and not system_configuration.get('RacingDataHub').get('isEnabledForGreyhound'):
            self.cms_config.update_system_configuration_structure(config_item = 'RacingDataHub', field_name = 'isEnabledForGreyhound', field_value = True)
        racing_edp_markets = self.cms_config.get_markets_with_description()
        self.__class__.expected_edp_tabs = [racing_edp_market.get('name').upper().replace(' - EXTRA PLACE', '') for racing_edp_market in racing_edp_markets if racing_edp_market.get('isGH') == True]
        if not self.expected_edp_tabs:
            raise CmsClientException('No markets are available for greyhounds sport')
        self.__class__.today_tab = self.get_sport_tab_name(name = 'today', category_id = category_id)

    def test_001_launch_the_application_and_navigate_to_the_greyhounds_page_from_all_sports_or_sport_ribbon_tab(self):
        """
        DESCRIPTION: Launch the application and navigate to the Greyhounds page from All Sports or Sport ribbon tab
        EXPECTED: Application should be launched successfully And Greyhounds page should be loaded
        """
        self.site.login()
        self.site.wait_content_state(state_name='HomePage')

    def test_002_verify_display_greyhounds_racing_page(self):
        """
        DESCRIPTION: Verify display Greyhounds racing page
        EXPECTED: First tab should be selected by default and highlighted with Red (Ladbrokes) and Blue (Coral) underline.
        EXPECTED: Next races should be displayed.
        """
        self.site.open_sport(name=self.GH_title)
        self.site.wait_content_state(state_name='Greyhounds')
        tab_name = vec.racing.RACING_NEXT_RACES_NAME if self.brand == 'ladbrokes' else vec.racing.DAYS[0]
        current_tab_name = self.site.greyhound.tabs_menu.current
        self.assertEqual(tab_name, current_tab_name, msg=f'current tab {current_tab_name} is not equal with {tab_name}')
        if current_tab_name != self.today_tab:
            self.site.greyhound.tabs_menu.click_item(item_name = self.today_tab)
            self.site.wait_content_state_changed()

    def test_003_verify_race_time_is_clickable_and_navigate_to_respective_page(self):
        """
        DESCRIPTION: Verify Race time is clickable and navigate to respective page
        EXPECTED: Meeting race time should be clickable and navigated to Respective meeting EDP page
        EXPECTED: Race time should be highlighted
        """
        accordions = wait_for_result(lambda : self.site.greyhound.tab_content.accordions_list.items_as_ordered_dict, timeout = 15)
        self.assertTrue(accordions, msg='Accordion list is empty on Horse Racing page')
        wait_for_haul(10)
        self.__class__.UK_AND_IRE = self.uk_and_irish_race_module_name.upper()
        uk_and_ire_module = accordions.get(self.UK_AND_IRE)
        self.assertTrue(uk_and_ire_module, msg=f'"{self.UK_AND_IRE}" is not found in {accordions.keys()}')
        meetings = uk_and_ire_module.items_as_ordered_dict
        self.assertTrue(meetings, f'{meetings.keys()} is not available in {self.UK_AND_IRE}')
        meeting_race_time = list(meetings.values())[0].items_as_ordered_dict
        for expected_race_time, race_obj in list(meeting_race_time.items()):
            if not race_obj.is_resulted:
                race_obj.click()
                break
        self.site.wait_content_state_changed()
        actual_race_time = self.site.greyhound_event_details.tab_content.event_off_times_list.selected_item
        self.assertEqual(actual_race_time,expected_race_time, msg= f'actual race time {actual_race_time} not equal with expected race  {expected_race_time}')

    def test_004_verify_racing_event_details_page_markets_display_under_meeting_and_switch_to_different_market(self):
        """
        DESCRIPTION: Verify Racing event details page markets display under meeting and switch to different market
        EXPECTED: All configured markets should be displayed as per CMS. By default, first market should be selected and highlighted
        EXPECTED: User is able to navigate to a different market data should be displayed according to market
        """
        current_tab = self.site.greyhound_event_details.tab_content.event_markets_list.market_tabs_list.current
        edp_tabs = self.site.greyhound_event_details.tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict
        for tab_name,tab in edp_tabs.items():
            if tab_name != current_tab:
                tab.click()
                cur_tab = self.site.greyhound_event_details.tab_content.event_markets_list.market_tabs_list.current
                self.assertEqual(cur_tab, tab_name, msg=f'could not navigate to tab {cur_tab} after clicking on {tab_name}')
        actual_edp_tabs = list(edp_tabs.keys())
        for tab in actual_edp_tabs:
            if tab == 'Win or Each Way':
                tab = vec.racing.RACING_EDP_DEFAULT_MARKET_TAB
            self.assertIn(tab.upper(), self.expected_edp_tabs, msg=f'actual tab {tab.upper()} not present in expected tab list {self.expected_edp_tabs}')

    def test_005_verify_switch_to_different_meeting_and_displaying_data(self):
        """
        DESCRIPTION: Verify switch to different Meeting and displaying data
        EXPECTED: User is able to navigate to a different meeting and displaying data.
        EXPECTED: Selected meeting should be underlined with Blue (Coral) and Red (Ladbrokes)
        """
        meeting_selector = self.site.greyhound_event_details.sub_header.meeting_selector
        self.assertTrue(meeting_selector, msg='meeting selector is not available')
        meeting_selector.click()
        sections = self.site.greyhound_event_details.meetings_list.items_as_ordered_dict
        self.assertTrue(sections, msg = 'sections is not available in meetings page')
        uk_ire_section = sections.get(self.UK_AND_IRE)
        self.assertTrue(uk_ire_section, msg=f'{self.UK_AND_IRE} section is not available')
        meetings = list(uk_ire_section.items_as_ordered_dict.values())
        self.assertTrue(meetings, msg=f'meetings are not available in {self.UK_AND_IRE}')
        meeting = random.choice(meetings)
        meeting_race_time = meeting.items_as_ordered_dict
        for expected_race_time, race_obj in list(meeting_race_time.items()):
            if not race_obj.is_resulted():
                race_obj.click()
                break
        self.site.wait_content_state_changed()
        actual_race_time = self.site.greyhound_event_details.tab_content.event_off_times_list.selected_item
        self.assertEqual(actual_race_time, expected_race_time, msg=f'actual race time {actual_race_time} not equal with expected race  {expected_race_time}')

    def test_006_verify_bet_placement_for_single_betmultiple_bet_complex_bet(self):
        """
        DESCRIPTION: Verify bet placement for single bet,Multiple bet, Complex bet
        EXPECTED: Bet placement should be happened successfully.
        EXPECTED: Bet receipt appears in Betslip.
        EXPECTED: 'Reuse selections' and 'Done' buttons are present in footer
        """
        self.add_selections_for_bet_placement(bet_type='single')
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        self.assertTrue(self.site.bet_receipt.footer.has_reuse_selections_button(),
                        msg='Reuse Selection button is not displayed')
        self.assertTrue(self.site.bet_receipt.footer.has_done_button(),
                        msg='Go Betting button is not displayed, Bet was not placed')
        self.site.close_betreceipt()
        self.add_selections_for_bet_placement(bet_type='multiple')
        self.place_multiple_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed()
        self.assertTrue(self.site.bet_receipt.footer.has_reuse_selections_button(),
                        msg='Reuse Selection button is not displayed')
        self.assertTrue(self.site.bet_receipt.footer.has_done_button(),
                        msg='Go Betting button is not displayed, Bet was not placed')
        self.site.close_betreceipt()
        self.add_selections_for_bet_placement(bet_type='complex')
        self.place_multiple_bet(number_of_stakes=4)
        self.check_bet_receipt_is_displayed()
        self.assertTrue(self.site.bet_receipt.footer.has_reuse_selections_button(),
                        msg='Reuse Selection button is not displayed')
        self.assertTrue(self.site.bet_receipt.footer.has_done_button(),
                        msg='Go Betting button is not displayed, Bet was not placed')
        self.site.close_betreceipt()
