import pytest
import tests
from voltron.utils.waiters import wait_for_result
from collections import OrderedDict
from datetime import datetime
from faker import Faker
from crlat_cms_client.utils.date_time import get_date_time_as_string
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_014_Module_Selector_Ribbon.Featured_tab.Highlights_Carousel.base_highlights_carousel_test import \
    generate_highlights_carousel_name
from time import sleep


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.uat
# @pytest.mark.prod - test case only applicable for QA2 as we need configure event hub sports module in CMS
@pytest.mark.hl
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C44870176_Verify_different_features_configured_under_Event_hub_on_Home_Page_and_Navigation_around_the_page(BaseBetSlipTest):
    """
    TR_ID: C44870176
    NAME: Verify different features configured under Event hub on Home Page and Navigation around the page.
    DESCRIPTION: Verify Event hub features . Verify user is able to place bets from different components.
    DESCRIPTION: -Verify when Event Hub Tab is not there, all the Events and Markets data should also be deleted"
    PRECONDITIONS: User should be logged in
    PRECONDITIONS: User should have configured Event hub in CMS with the following features :
    PRECONDITIONS: 1. Surface bets
    PRECONDITIONS: 2. Quick links
    PRECONDITIONS: 3. Highlights carousel
    PRECONDITIONS: 4. Featured module
    PRECONDITIONS: 5. Events/Races are displayed as configured in CMS
    PRECONDITIONS: 6. Display specific markets (Including racing) with the number of selections provided as per CMS (There Should be a setting to display all the selections)
    PRECONDITIONS: 7. Display specific events (Including racing) with the number of selections provided as per CMS (There Should be a setting to display all the selections)
    """
    keep_browser_open = True
    tabs_bma = OrderedDict()
    fake = Faker()
    content = fake.paragraph()
    price_num = fake.random_int(min=1, max=10)
    price_den = fake.random_int(min=20, max=50)
    highlights_carousels_titles = [generate_highlights_carousel_name()]
    quick_link_name = 'autotest ' + Faker().city()
    destination_url = f'https://{tests.HOSTNAME}/sport/football/matches'
    quick_link_object = None

    def create_surface_bet(self):
        event = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.selection_ids, self.__class__.team1 = event.selection_ids, event.team1
        self.__class__.eventID = event.event_id
        self.__class__.price_button_text = self.ob_config.event.prices['odds_home']
        self.__class__.surface_bet = self.cms_config.add_surface_bet(selection_id=self.selection_ids[self.team1],
                                                                     content=self.content,
                                                                     priceNum=self.price_num,
                                                                     priceDen=self.price_den,
                                                                     eventIDs=self.eventID,
                                                                     edpOn=True,
                                                                     categoryIDs=[0, 16],
                                                                     event_hub_id=self.event_hub_index[0])

    def test_001_load_app(self):
        """
        DESCRIPTION: Load App
        EXPECTED: App is loaded
        """
        self.site.wait_content_state('Home')
        self.site.login()
        self.site.wait_quick_bet_overlay_to_hide()

    def test_002_tap_on_the_event_hub_that_has_been_configured_in_cms(self):
        """
        DESCRIPTION: Tap on the Event hub that has been configured in CMS
        EXPECTED: Event Hub Page is loaded
        """
        module_ribbon_tabs = self.cms_config.module_ribbon_tabs.all_tabs_data
        self.__class__.tabs_cms = [tab['title'].upper() for tab in module_ribbon_tabs if
                                   tab['visible'] is True and
                                   tab['directiveName'] == 'EventHub' and
                                   (tab['displayTo'] is None or tab['displayTo'] > get_date_time_as_string(
                                       time_format="%Y-%m-%dT%H:%M:%S", hours=-1))]
        selected_tab = self.tabs_cms[0]
        self.__class__.event_hub_index = [tab['hubIndex'] for tab in module_ribbon_tabs if
                                          tab['title'].upper() == selected_tab]
        self.__class__.tabs_bma = self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict
        surface_bet_modules_cms = None
        for tab_name, tab in self.tabs_bma.items():
            if tab_name == selected_tab:
                tab.click()
                break
        self.__class__.sports_module_event_hub = self.cms_config.get_sport_modules_for_event_hub(self.event_hub_index[0])
        for module in self.sports_module_event_hub:
            if module['moduleType'] == 'SURFACE_BET':
                surface_bet_modules_cms = module
                break
        if surface_bet_modules_cms is None:
            self.cms_config.add_sport_module_to_event_hub(module_type='SURFACE_BET')
        else:
            surface_bet_module_status = [module['disabled'] for module in self.sports_module_event_hub
                                         if module['moduleType'] == 'SURFACE_BET']
            if surface_bet_module_status is True:
                self.cms_config.change_sport_module_state(sport_module=surface_bet_modules_cms)
        for i in range(0, 3):
            self.create_surface_bet()
        self.device.refresh_page()

    def test_003_verify_surface_bets(self):
        """
        DESCRIPTION: Verify Surface bets
        EXPECTED: User should be able to scroll across the surface bets displaying on the Event hub page
        """
        result = wait_for_result(lambda: f'/{self.event_hub_index[0]}' in self.device.get_current_url(),
                                 name=f'Waiting for Event hub with index "{self.event_hub_index[0]}"',
                                 timeout=5)
        self.assertTrue(result, msg=f'Did not navigate to Event hub with index "{self.event_hub_index[0]}"')
        surface_bets = self.site.home.tab_content.surface_bets.items_as_ordered_dict
        self.assertTrue(surface_bets, msg='No Surface Bets found')
        event_name, self.__class__.sb_event = list(surface_bets.items())[-1]
        self.assertTrue(self.sb_event.is_displayed(), msg=f'surface bet "{event_name}" is not displayed')

    def test_004_tap_on_any_selection_from_surface_bets(self):
        """
        DESCRIPTION: tap on any selection from surface bets
        EXPECTED: Mobile : quick bet should be invoked (if enabled) or selection added to bet slip
        EXPECTED: Tablet : Selection added to the bet slip
        """
        self.sb_event.bet_button.click()
        quick_bet = self.site.quick_bet_panel.selection
        self.assertTrue(quick_bet, msg=f'"Quick Bet" not invoked for "{self.sb_event}"')
        self.site.add_first_selection_from_quick_bet_to_betslip()
        self.__class__.expected_betslip_counter_value += 1
        sleep(1)
        betslip_counter_value = self.site.header.bet_slip_counter.counter_value
        self.assertEqual(int(betslip_counter_value), self.expected_betslip_counter_value,
                         msg=f'Betslip counter value: "{betslip_counter_value}" is not the same as expected: '
                             f'"{self.expected_betslip_counter_value}"')

    def test_005_tap_on_the_event(self):
        """
        DESCRIPTION: tap on the event
        EXPECTED: User should land on the corresponding event landing page.
        """
        # This step is covered in step 7

    def test_006_click_on_back(self):
        """
        DESCRIPTION: click on back
        EXPECTED: User should navigate to the Event hub page
        """
        # This step is covered in step 7

    def test_007_repeat_steps_4_6_for_featured_module_highlight_carousal_if_available(self, **featured):
        """
        DESCRIPTION: repeat steps 4-6 for featured module, Highlight carousal if available
        EXPECTED:
        """
        event_hub_url = self.device.get_current_url()
        # Featured Module
        featured['events_time_from_hours_delta'] = -24
        featured['module_time_from_hours_delta'] = -24
        featured_module_cms = None
        for module in self.sports_module_event_hub:
            if module['moduleType'] == 'FEATURED':
                featured_module_cms = module
                break
        if featured_module_cms is None:
            self.cms_config.add_sport_module_to_event_hub(module_type='FEATURED')
        else:
            featured_module_status = [module['disabled'] for module in self.sports_module_event_hub
                                      if module['moduleType'] == 'FEATURED']
            if featured_module_status is True:
                self.cms_config.change_sport_module_state(sport_module=featured_module_cms)
        params = self.ob_config.add_autotest_premier_league_football_event(perform_stream=True)
        self.__class__.selection_id_1 = list(params.selection_ids.values())[0]
        featured_eventID = params.event_id
        self.cms_config.add_featured_tab_module(select_event_by='Event', id=featured_eventID, page_type='eventhub',
                                                page_id=str(self.event_hub_index[0]), show_expanded=True, **featured)
        featured_modules = self.site.home.tab_content.accordions_list.items_as_ordered_dict
        for item_name, item in featured_modules.items():
            item.first_player_bet_button.click()
            break
        self.expected_betslip_counter_value += 1
        sleep(1)
        betslip_counter_value = self.site.header.bet_slip_counter.counter_value
        self.assertEqual(int(betslip_counter_value), self.expected_betslip_counter_value,
                         msg=f'Betslip counter value: "{betslip_counter_value}" is not the same as expected: "{self.expected_betslip_counter_value}"')
        featured_event_name, featured_event = list(featured_modules.items())[0]
        featured_event.click()
        self.site.wait_content_state_changed()
        result = wait_for_result(lambda: featured_eventID in self.device.get_current_url(),
                                 name=f'Waiting for "{featured_eventID}" event',
                                 timeout=5)
        self.assertTrue(result, msg=f'Event :"{featured_eventID}" is not present in the URL :"{self.device.get_current_url()}"')
        self.site.back_button_click()
        self.site.wait_content_state_changed()
        result = wait_for_result(lambda: event_hub_url == self.device.get_current_url(),
                                 name=f'Waiting for "{featured_eventID}" event',
                                 timeout=5)
        self.assertTrue(result, msg=f'User did not navigate back to Event hub:"{event_hub_url}"')

        # Highlights Corousel
        self.__class__.now = datetime.now()
        self.__class__.time_format = '%Y-%m-%dT%H:%M:%S.%f'
        featured['date_from'] = get_date_time_as_string(date_time_obj=self.now, time_format=self.time_format,
                                                        url_encode=False, hours=-5, days=-1)[:-3] + 'Z'
        hc_module_cms = None
        for module in self.sports_module_event_hub:
            if module['moduleType'] == 'HIGHLIGHTS_CAROUSEL':
                hc_module_cms = module
                break
        if hc_module_cms is None:
            self.cms_config.add_sport_module_to_event_hub(module_type='HIGHLIGHTS_CAROUSEL')
        else:
            highlights_module_status = [module['disabled'] for module in self.sports_module_event_hub
                                        if module['moduleType'] == 'HIGHLIGHTS_CAROUSEL']
            if highlights_module_status is True:
                self.cms_config.change_sport_module_state(sport_module=hc_module_cms)
        event = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.selection_id_2 = list(event.selection_ids.values())[0]
        event_2 = self.ob_config.add_autotest_premier_league_football_event()
        event_id_1 = event.event_id
        event_id_2 = event_2.event_id
        self.cms_config.create_highlights_carousel(title=self.highlights_carousels_titles[0],
                                                   events=[event_id_1, event_id_2],
                                                   page_type='eventhub',
                                                   sport_id=self.event_hub_index[0],
                                                   **featured)
        highlight_carousels = self.site.home.tab_content.highlight_carousels
        if self.brand == 'bma':
            highlight_carousel_cards = highlight_carousels[self.highlights_carousels_titles[0]].items_as_ordered_dict
        else:
            highlight_carousel_cards = highlight_carousels[self.highlights_carousels_titles[0].upper()].items_as_ordered_dict
        if self.brand == 'bma':
            for item in highlight_carousels[self.highlights_carousels_titles[0]].items:
                item.first_player_bet_button.click()
                break
        else:
            for item in highlight_carousels[self.highlights_carousels_titles[0].upper()].items:
                item.first_player_bet_button.click()
                break
        self.expected_betslip_counter_value += 1
        sleep(1)
        betslip_counter_value = self.site.header.bet_slip_counter.counter_value
        self.assertEqual(int(betslip_counter_value), self.expected_betslip_counter_value,
                         msg=f'Betslip counter value: "{betslip_counter_value}" is not the same as expected: '
                             f'"{self.expected_betslip_counter_value}"')
        hc_event_name, self.__class__.hc_event = list(highlight_carousel_cards.items())[0]
        event_id = self.hc_event.event_id
        self.hc_event.click()
        self.site.wait_content_state_changed()
        result = wait_for_result(lambda: event_id in self.device.get_current_url(),
                                 name=f'Waiting for "{self.destination_url}"',
                                 timeout=5)
        self.assertTrue(result,
                        msg=f'Event :"{event_id}" is not present in the URL :"{self.device.get_current_url()}"')
        self.site.back_button_click()
        self.site.wait_content_state_changed()
        result = wait_for_result(lambda: event_hub_url == self.device.get_current_url(),
                                 name=f'Waiting for "{self.destination_url}"',
                                 timeout=5)
        self.assertTrue(result, msg=f'User did not navigate back to Event hub:"{event_hub_url}"')

    def test_008_click_on_any_of_the_quick_links_available(self):
        """
        DESCRIPTION: Click on any of the Quick links available
        EXPECTED: user should land on the corresponding page. eg : A quick link for 'Today's Football' would navigate to the page where today's matches are listed under Football.
        """
        ql_date_from = get_date_time_as_string(date_time_obj=self.now, time_format=self.time_format, url_encode=False,
                                               hours=-5, days=-1)[:-3] + 'Z'
        quick_link_module_cms = None
        for module in self.sports_module_event_hub:
            if module['moduleType'] == 'QUICK_LINK':
                quick_link_module_cms = module
                break
        if quick_link_module_cms is None:
            self.cms_config.add_sport_module_to_event_hub(module_type='QUICK_LINK')
        else:
            quick_link_module_status = [module['disabled'] for module in self.sports_module_event_hub
                                        if module['moduleType'] == 'QUICK_LINK']
            if quick_link_module_status is True:
                self.cms_config.change_sport_module_state(sport_module=quick_link_module_cms)
        self.cms_config.create_quick_link(title=self.quick_link_name,
                                          sport_id=self.event_hub_index[0],
                                          destination=self.destination_url,
                                          page_type='eventhub',
                                          date_from=ql_date_from)
        quick_links = self.site.home.tab_content.quick_links.items_as_ordered_dict
        self.assertTrue(quick_links, msg='No "Quick Links" present')
        quick_links.get(self.quick_link_name).click()
        self.site.wait_content_state_changed()
        result = wait_for_result(lambda: self.destination_url == self.device.get_current_url(),
                                 name=f'Waiting for "{self.destination_url}"',
                                 timeout=25)
        navigated_url = self.device.get_current_url()
        self.assertTrue(result, msg=f'Expected Url after click:"{self.destination_url}" '
                                    f'not same as Actual Url:"{navigated_url}" ')
        self.site.back_button_click()

    def test_009_add_more_selections_to_the_bet_slip_from_different_components_on_the_event_hub_and_place_bet(self):
        """
        DESCRIPTION: Add more selections to the bet slip from different components on the event hub and place bet.
        EXPECTED: Selections get added to the bet slip and user is able to place bet.
        """
        self.site.open_betslip()
        singles_section_value = self.get_betslip_sections().Singles
        bet_info = self.place_and_validate_single_bet(number_of_stakes=len(singles_section_value), timeout=5)
        self.assertTrue(bet_info, msg='Bet placement unsuccessful')

    def test_010_load_cms_and_disabledelete_the_event_hub(self):
        """
        DESCRIPTION: Load CMS and disable/delete the event hub
        EXPECTED: All the components under the Event hub should be deleted and user should not see the Event hub menu item on Home page
        """
        # This step is already taken care by frameowrk teardown() method if we create any eventhub and its components
