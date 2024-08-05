import pytest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from crlat_siteserve_client.utils.date_time import get_date_time_as_string
from crlat_siteserve_client.utils.exceptions import SiteServeException
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_005_Build_Your_Bet.BaseBuildYourBetTest import BaseBanachTest
from voltron.pages.shared.components.base import ComponentBase
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.sports
@pytest.mark.Quick_Switcher
@pytest.mark.release_158_sprint
@vtest
class Test_C65950828_Quick_Switcher_end_to_end_Journey(BaseBetSlipTest, BaseBanachTest, ComponentBase):
    """
    TR_ID: C65950828
    NAME: Quick Switcher end-to-end Journey
    DESCRIPTION: Verify Quick Switcher end-to-end Journey
    PRECONDITIONS: * In CMS->System Config->Structure->EventQuickSwitcher->isQuickSwitchEnabled should be enabled
    PRECONDITIONS: * In front end events should be available for football
    """
    keep_browser_open = True
    end_time = f'{get_date_time_as_string(days=5)}T00:00:00.000Z'
    proxy = None

    def selections(self, start, selection):
        bet_buttons_list = self.site.home.bet_buttons
        self.assertTrue(bet_buttons_list, msg='No bet buttons on UI')
        for index in range(start, selection):
            selection_btn = bet_buttons_list[index]
            self.scroll_to_we(selection_btn)
            selection_btn.click()

    def bet_placement_and_verify_switcher(self, events):
        event = next((event for event in reversed(events)), None)
        bet_buttons = events[event].get_available_prices()
        bet_button_name = next(bet_button for bet_button in bet_buttons)
        bet_buttons[bet_button_name].click()
        if self.device_type != 'desktop':
            self.assertTrue(self.site.wait_for_quick_bet_panel(expected_result=True),
                            msg='Quick Bet is not present')
            # Get the Quick Bet panel's content
            quick_bet = self.site.quick_bet_panel.selection.content
            # Set the bet amount in the Quick Bet panel
            quick_bet.amount_form.input.value = self.bet_amount
            # Place the bet using the Quick Bet panel
            self.site.quick_bet_panel.place_bet.click()
            # Wait for the bet receipt to be displayed
            bet_receipt = self.site.quick_bet_panel.wait_for_bet_receipt_displayed()
            self.assertTrue(bet_receipt, msg='Bet Receipt is not displayed')
            # Close the Quick Bet panel
            self.site.quick_bet_panel.close()
            self.assertTrue(self.site.sport_event_details.change_match_section.is_displayed(),
                            msg='Meetings list is not shown')
        else:
            singles_section = self.get_betslip_sections().Singles
            stake_name, stake = list(singles_section.items())[0]
            self.enter_stake_amount(stake=(stake_name, stake), stake_bet_amounts={stake_name: 0.20})
            self.get_betslip_content().bet_now_button.click()
            self.check_bet_receipt_is_displayed()
            self.site.wait_content_state_changed()

    def get_events_names_for_tab(self, start_date, end_date):
        events_filter = self.ss_query_builder \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME, OPERATORS.GREATER_THAN_OR_EQUAL, start_date)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME, OPERATORS.LESS_THAN, end_date)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SUSPEND_AT_TIME, OPERATORS.GREATER_THAN_OR_EQUAL,
                                      self.start_date_minus))
        resp_events = self.ss_req.ss_event_for_type(type_id=self.type_id, query_builder=events_filter)
        events = []
        for event in resp_events:
            events.append(event['event']['name'].strip())
        return events

    def test_000_pre_conditions(self):
        """
        PRECONDITIONS: getting  events for today, tomorrow and future tab events and also validating cms
        config for change market
        """
        cms_config = self.cms_config.get_system_configuration_item('EventQuickSwitcher').get('isQuickSwitchEnabled')
        if not cms_config:
            if tests.settings.cms_env == 'prd0':
                raise CmsClientException('"EventQuickSwitcher" under it isQuickSwitchEnabled is not enable in CMS')
            else:
                self.cms_config.update_system_configuration_structure(config_item='EventQuickSwitcher',
                                                                  field_name="isQuickSwitchEnabled", field_value=True)
        events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                     in_play_event=True,
                                                     raise_exceptions=False)
        if not events:
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)

        self.__class__.event_id = events[0]['event']['id']
        self.__class__.type_id = events[0]['event']['typeId']
        # *************************today events ***************
        today_start_time = f'{get_date_time_as_string(days=0)}T00:00:00.000Z'
        today_end_time = f'{get_date_time_as_string(days=1)}T00:00:00.000Z'
        self.__class__.todays_events = self.get_events_names_for_tab(start_date=today_start_time,
                                                                     end_date=today_end_time)
        # *****************tomorrow_start_date*******************
        tomorrow_start_date = f'{get_date_time_as_string(days=1)}T00:00:00.000Z'
        tomorrow_end_time = f'{get_date_time_as_string(days=2)}T00:00:00.000Z'
        self.__class__.tomorrow_events = self.get_events_names_for_tab(start_date=tomorrow_start_date,
                                                                       end_date=tomorrow_end_time)

        # *****************future_start_date*******************
        future_start_date = f'{get_date_time_as_string(days=3)}T00:00:00.000Z'
        future_end_time = f'{get_date_time_as_string(days=50)}T00:00:00.000Z'
        self.__class__.future_events = self.get_events_names_for_tab(start_date=future_start_date,
                                                                     end_date=future_end_time)

    def test_001_launch_the_application_and_navigate_to_football(self):
        """
        DESCRIPTION: Launch the application and navigate to Football
        EXPECTED: * Football landing page is successfully loaded with respective data
        """
        self.site.login()
        self.site.wait_content_state('Homepage')
        if self.device_type == "mobile":
            self.selections(0, 1)
            self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet was not shown')
            self.assertTrue(self.site.quick_bet_panel.add_to_betslip_button.is_displayed(),
                            msg='"ADD TO BETSLIP" button is not displayed')
            self.site.quick_bet_panel.add_to_betslip_button.click()
            wait_for_haul(3)
            self.selections(5, 6)
            self.verify_betslip_counter_change(expected_value=2)
            self.assertTrue(self.site.wait_for_acca_notification_present(expected_result=True),
                            msg='Acca notification is not displayed')

    def test_002_click_on_any_event_from_the_matches_tab(self):
        """
        DESCRIPTION: Click on any event from the Matches tab
        EXPECTED: * User is navigated to the respective EDP page
        """
        self.navigate_to_edp(event_id=self.event_id)
        self.site.wait_content_state(state_name='EventDetails')

    def test_003_verify_the_change_match_option_on_the_top_bar(self, check_acca_bar=True):
        """
        DESCRIPTION: Verify the 'Change Match' option on the top bar
        EXPECTED: * User able to see 'Change Match' option followed by down arrow
        EXPECTED: Note: For Coral/LADS Desktop &amp; Coral Mobile: 'Change Match' is displayed on the top bar
        EXPECTED: For LADS Mobile: 'Change Match' is displayed under the top bar
        """
        self.assertTrue(self.site.sport_event_details.has_change_match_selector(expected_result=True),
                        msg=f'Change market drop down is not shown in football EDP')
        if check_acca_bar and self.device_type == "mobile":
            self.assertTrue(self.site.wait_for_acca_notification_present(expected_result=True),
                            msg='Acca notification is not displayed')
        self.site.sport_event_details.change_match_selector.click()
        self.assertTrue(self.site.sport_event_details.change_match_section.is_displayed(),
                        msg='Meetings list is not shown')
        if self.device_type == "mobile" and check_acca_bar:
            self.site.open_betslip()
            self.site.betslip.remove_all_button.click()
            dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_REMOVE_ALL)
            dialog.continue_button.click()
            self.assertTrue(self.site.sport_event_details.change_match_section.is_displayed(),
                            msg='Meetings list is not shown')

    def test_004_desktop_mouse_hover_on_change_match_option(self):
        """
        DESCRIPTION: Desktop: Mouse hover on 'Change Match' option
        EXPECTED: * 'Change Match' is displayed with underline
        """
        pass

    def test_005_click_on_change_match_option(self):
        """
        DESCRIPTION: Click on 'Change Match' option
        EXPECTED: * An overlay is coming into the picture with 'Matches' header + 'Close' button
        EXPECTED: * Under header, sub-tabs(Today,Tomorrow &amp; future) will be displayed
        EXPECTED: * By default user is navigated to the sub-tab which has events available.
        EXPECTED: Note:-
        EXPECTED: * If events are available in Today sub-tab then by default user is navigated to Today sub-tab
        EXPECTED: * If events are not available in Today sub-tab then by default user is navigated to Tomorrow sub-tab and 'Currently there are no events to show' message is displayed on Today sub tab
        EXPECTED: * If events are not available in Today,Tomorrow sub-tabs then by default user is navigated to Future sub-tab and 'Currently there are no events to show' message is displayed on Today,Tomorrow sub tabs
        """

        self.site.sport_event_details.change_match_section.has_grouping_buttons
        self.__class__.sub_tabs = self.site.sport_event_details.change_match_section.grouping_buttons.items_as_ordered_dict
        sub_tab_names = list(self.sub_tabs.keys())
        expected_tabs = [vec.sb.TABS_NAME_TODAY.upper(), vec.sb.TABS_NAME_TOMORROW.upper(),
                         vec.sb.TABS_NAME_FUTURE.upper()]
        self.assertListEqual(sub_tab_names, expected_tabs,
                             msg=f"events under todays tab '{sub_tab_names}' is not same as from ss call '{expected_tabs}'")
        selected_tab = self.site.sport_event_details.change_match_section.grouping_buttons.current
        # Check if matches are present in each tab
        today_has_matches = len(self.todays_events) > 0
        tomorrow_has_matches = len(self.tomorrow_events) > 0
        future_has_matches = len(self.future_events) > 0

        # Check if the selected tab matches the expected one based on the presence of matches
        if today_has_matches:
            expected_tab = vec.sb.TABS_NAME_TODAY
        elif tomorrow_has_matches:
            expected_tab = vec.sb.TABS_NAME_TOMORROW
        elif future_has_matches:
            expected_tab = vec.sb.TABS_NAME_FUTURE

        # Assert if the selected tab matches the expected one
        self.assertEqual(str(selected_tab).upper(), str(expected_tab).upper(),
                         msg=f"The selected tab is not as expected based on match presence.")

    def test_006_verify_the_today_sub_tab(self):
        """
        DESCRIPTION: Verify the 'Today' sub-tab
        EXPECTED: * If events are available then 'Today' sub-tab is loaded with respective data(Live events+Preplay events).
        EXPECTED: Else  'Currently there are no events to show' message is displayed on Today sub tab
        """
        today_tab = next(
            (tab for tab_name, tab in self.sub_tabs.items() if tab_name.upper() == vec.sb.TABS_NAME_TODAY.upper()),
            None)
        self.assertTrue(today_tab, msg='tomorrow tab is not available')
        today_tab.click()
        # **************validate today events ****************
        if len(self.todays_events) > 0:
            sections = \
                list(self.site.sport_event_details.change_match_section.accordions_list.items_as_ordered_dict.values())[
                    0]
            today_events = sections.items_as_ordered_dict
            self.assertListEqual(sorted(list(today_events.keys())), sorted(self.todays_events),
                                 msg=f"events under todays tab '{sorted(self.todays_events)}' is not same as from ss call \n"
                                     f"'{sorted(list(today_events.keys()))}'")
            self.bet_placement_and_verify_switcher(events=today_events)
        else:
            self.assertTrue(self.site.sport_event_details.change_match_section.has_no_events_label(),
                            msg=f"currently no events message is not displayed even there are no events ")
            # **************validate today events ****************
        tomorrow_tab = next(
            (tab for tab_name, tab in self.sub_tabs.items() if tab_name.upper() == vec.sb.TABS_NAME_TOMORROW.upper()),
            None)
        self.assertTrue(tomorrow_tab, msg='tomorrow tab is not available')
        tomorrow_tab.click()
        if len(self.tomorrow_events) > 0:
            sections = \
                list(self.site.sport_event_details.change_match_section.accordions_list.items_as_ordered_dict.values())[
                    0]
            tomorrow_events = sections.items_as_ordered_dict
            self.assertListEqual(sorted(list(tomorrow_events.keys())), sorted(self.tomorrow_events),
                                 msg=f"events under todays tab '{sorted(list(tomorrow_events.keys()))}' is not same as from ss call '{sorted(self.tomorrow_events)}'")
            self.bet_placement_and_verify_switcher(events=tomorrow_events)
        else:
            self.assertTrue(self.site.sport_event_details.change_match_section.has_no_events_label(),
                            msg=f"currently no events message is not displayed even there are no events ")
        #     ***************** validating future data ********************
        future_tab = next(
            (tab for tab_name, tab in self.sub_tabs.items() if tab_name.upper() == vec.sb.TABS_NAME_FUTURE.upper()),
            None)
        self.assertTrue(future_tab, msg='future tab is not available')
        future_tab.click()
        if len(self.future_events) > 0:
            sections = self.site.sport_event_details.change_match_section.accordions_list.items_as_ordered_dict
            future_events = {}
            for section_name, section in sections.items():
                future_event = section.items_as_ordered_dict
                self.assertTrue(future_event, msg=f'no events found under section %s' % section_name)
                future_events.update(future_event)
            self.assertListEqual(sorted(list(future_events.keys())), sorted(self.future_events),
                                 msg=f"events under todays tab '{sorted(list(future_events.keys()))}' is not same as from ss call '{sorted(self.future_events)}'")
            self.bet_placement_and_verify_switcher(events=future_events)
        else:
            self.assertTrue(self.site.sport_event_details.change_match_section.has_no_events_label(),
                            msg=f"currently no events message is not displayed even there are no events  ")

    def test_007_click_on_any_other_event_apart_from_the_event_which_is_currently_opened_in_the_background(self):
        """
        DESCRIPTION: Click on any other event apart from the event which is currently opened in the background
        EXPECTED: * User navigates to the respective event details page and also able to see 'Change Match' option
        """
        self.site.sport_event_details.change_match_section.has_grouping_buttons
        self.__class__.sub_tabs = self.site.sport_event_details.change_match_section.grouping_buttons.items_as_ordered_dict
        # Check if matches are present in each tab
        today_has_matches = len(self.todays_events) > 0
        tomorrow_has_matches = len(self.tomorrow_events) > 0
        future_has_matches = len(self.future_events) > 0

        # Check if the selected tab matches the expected one based on the presence of matches
        if today_has_matches:
            today_tab = next(
                (tab for tab_name, tab in self.sub_tabs.items() if tab_name.upper() == vec.sb.TABS_NAME_TODAY.upper()),
                None)
            self.assertTrue(today_tab, msg='tomorrow tab is not available')
            today_tab.click()
        elif tomorrow_has_matches:
            tomorrow_tab = next(
                (tab for tab_name, tab in self.sub_tabs.items() if
                 tab_name.upper() == vec.sb.TABS_NAME_TOMORROW.upper()),
                None)
            self.assertTrue(tomorrow_tab, msg='tomorrow tab is not available')
            tomorrow_tab.click()
        elif future_has_matches:
            future_tab = next(
                (tab for tab_name, tab in self.sub_tabs.items() if tab_name.upper() == vec.sb.TABS_NAME_FUTURE.upper()),
                None)
            self.assertTrue(future_tab, msg='future tab is not available')
            future_tab.click()
        else:
            raise SiteServeException(f"No events available for this type{self.type_id}")
        sections = \
            list(self.site.sport_event_details.change_match_section.accordions_list.items_as_ordered_dict.values())[
                0]
        events = sections.items_as_ordered_dict
        self.assertTrue(events, msg=f"no events are displayed under change option ")
        event_name, event = next(((event_name, event) for event_name, event in events.items()), None)
        event.click()
        self.site.wait_content_state(state_name='EventDetails')
        self.assertTrue(self.site.sport_event_details.has_change_match_selector(expected_result=True),
                        msg=f'Change market drop down is not shown in EDP {event_name}')

    def test_008_repeat_step_67_for_tomorrow_amp_future_sub_tabs(self):
        """
        DESCRIPTION: Repeat step-6,7 for Tomorrow &amp; Future sub-tabs
        EXPECTED: Note:-
        EXPECTED: In Future tab events are segregated by date in ascending order
        """
        # covered in above steps

    def test_009_click_on_change_match_option_again_and_scroll_the_page(self):
        """
        DESCRIPTION: Click on 'Change Match' option again and scroll the page
        EXPECTED: * User able to see an overlay until the last market on the EDP page for desktop
        """

    #     cant automate the step it's from UI
    def test_010_add_a_selection_to_the_betslip_and_place_bet(self):
        """
        DESCRIPTION: Add a selection to the betslip and place bet
        EXPECTED: * Overlay is still displayed in background
        EXPECTED: Desktop:-
        EXPECTED: * User able to add selection the beslip and also able to place bets
        EXPECTED: Mobile:-
        EXPECTED: * User able to add selection the quickbet and also able to place bet
        """

    #     covered in above steps

    def test_011_verify_whether_overlay_is_displaying_in_all_edp_markets(self):
        """
        DESCRIPTION: Verify whether overlay is displaying in all EDP markets
        EXPECTED: * Overlay will be displayed on the all the EDP markets
        """
        pass

    def test_012_close_the_overlay_by_clicking_on_change_match_button_and_navigate_to_build_your_bet_market_tab(self):
        """
        DESCRIPTION: Close the overlay by clicking on 'Change Match' button and Navigate to Build Your Bet market tab
        EXPECTED: * Overlay is closed
        EXPECTED: * User navigated to Build Your Bet market
        """
        eventID = self.get_ob_event_with_byb_market()
        self.navigate_to_edp(event_id=eventID)
        self.site.wait_content_state(state_name='EventDetails')
        self.assertTrue(
            self.site.sport_event_details.markets_tabs_list.open_tab(self.expected_market_tabs.build_your_bet),
            msg=f'"{self.expected_market_tabs.build_your_bet}" tab is not active')
        # Match betting selection
        match_betting = self.get_market(market_name=self.expected_market_sections.match_betting)
        self.assertTrue(match_betting, msg=f'"{self.expected_market_sections.match_betting}" market does not exist')
        match_betting_selection_name = match_betting.set_market_selection(selection_index=1)
        match_betting.set_market_selection(selection_index=1, time=True)
        self.assertTrue(match_betting_selection_name, msg='Match betting selection is not added to Dashboard')
        match_betting.add_to_betslip_button.click()
        self.assertTrue(self.site.sport_event_details.tab_content.has_dashboard_panel(),
                        msg=f"Dashboard panel is not shown even when the bet is added to betslip")
        self.site.sport_event_details.change_match_selector.click()
        self.assertTrue(self.site.sport_event_details.change_match_section.is_displayed(),
                        msg='Meetings list is not shown')

    def test_013_add_byb_selections_to_the_betslip_and_click_on_change_match_button(self):
        """
        DESCRIPTION: Add BYB selections to the betslip and click on 'Change Match' button
        EXPECTED: * BYB Selections are added to the betslip
        EXPECTED: * Overlay is displayed by hiding the BYB betslip
        """
        pass

    def test_014_close_the_overlay_by_clicking_on_close_button(self):
        """
        DESCRIPTION: Close the Overlay by clicking on 'close' button
        EXPECTED: * Change Match overlay is closed successfully
        EXPECTED: * BYB Betslip is coming into the picture with previously added selections
        """
        self.site.sport_event_details.change_match_selector.click()
        self.assertTrue(self.site.sport_event_details.tab_content.has_dashboard_panel(),
                        msg=f"Dashboard panel is not shown even when the bet is added to betslip")

    def test_015_verify_the_change_match_option_for_football___ampgt_specials_amp_outrights(self):
        """
        DESCRIPTION: Verify the 'Change Match' option for Football --&amp;gt; 'Specials' &amp; 'Outrights'
        EXPECTED: * 'Change Match' option is not displayed for 'Specials' &amp; 'Outrights'
        """
        self.navigate_to_page(name='sport/football')
        # navigating to football specials tab
        specials_tab_name = self.get_sport_tab_name(name=vec.sb.SPORT_TABS_INTERNAL_NAMES.specials,
                                                    category_id=self.ob_config.football_config.category_id)
        specials_tab = self.site.football.tabs_menu.click_button(specials_tab_name)
        current_tab_name = self.site.football.tabs_menu.current.upper()
        self.assertEqual(current_tab_name, specials_tab_name,
                         msg=f'{current_tab_name} is not expected as {specials_tab_name}')
        self.assertTrue(specials_tab, msg=f'"{specials_tab_name}" is not opened')
        # getting accordions in specials tab and checking whether each accordion is expanded and collapsed
        sections = self.site.contents.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg=f'no accordions are found')
        section_name, section = next(((section_name, section) for section_name, section in sections.items()), None)
        section.expand()
        self.assertTrue(section.is_expanded(timeout=10), msg=f'Section "{section_name}" is not expanded')
        events = section.items_as_ordered_dict
        self.assertTrue(events, msg=f'No events found in section "{section_name}"')
        event = list(events.values())[0]
        event.click()
        self.site.wait_content_state(state_name='EventDetails')
        self.assertFalse(self.site.sport_event_details.has_change_match_selector(expected_result=False),
                         msg=f'Change market drop down is shown in special EDP')
        self.site.back_button_click()
        outright_tab_name = self.get_sport_tab_name(name=vec.sb.SPORT_TABS_INTERNAL_NAMES.outrights,
                                                    category_id=self.ob_config.football_config.category_id,
                                                    raise_exceptions=False)
        outright_tab = self.site.football.tabs_menu.click_button(outright_tab_name)
        current_tab_name = self.site.football.tabs_menu.current.upper()
        self.assertEqual(current_tab_name, outright_tab_name,
                         msg=f'{current_tab_name} is not expected as {outright_tab_name}')
        self.assertTrue(outright_tab, msg=f'"{outright_tab_name}" is not opened')
        # getting accordions in out tab and checking whether each accordion is expanded and collapsed
        sections = self.site.contents.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg=f'no accordions are found')
        section_name, section = next(((section_name, section) for section_name, section in sections.items()), None)
        section.expand()
        self.assertTrue(section.is_expanded(timeout=10), msg=f'Section "{section_name}" is not expanded')
        events = section.items_as_ordered_dict
        self.assertTrue(events, msg=f'No events found in section "{section_name}"')
        event = list(events.values())[0]
        event.click()
        self.site.wait_content_state(state_name='EventDetails')
        self.assertFalse(self.site.sport_event_details.has_change_match_selector(expected_result=False),
                         msg=f'Change market drop down is shown in special EDP')

    def test_016_verify_the_change_match_option_for_other_sportseg_tennisbasketball_on_edp_page(self):
        """
        DESCRIPTION: Verify the 'Change Match' option for other sports(e.g., Tennis,Basketball) on EDP page
        EXPECTED: * 'Change Match' option is not displayed for other sports
        """
        event = self.get_active_events_for_category(category_id=self.ob_config.tennis_config.category_id)[0]
        event_id = event['event']['id']
        self.navigate_to_edp(event_id=event_id)
        self.site.wait_content_state(state_name='EventDetails')
        self.assertFalse(self.site.sport_event_details.has_change_match_selector(expected_result=False),
                         msg=f'Change market drop down is shown in tennis EDP')
        self.site.logout()
        self.test_002_click_on_any_event_from_the_matches_tab()
        self.test_003_verify_the_change_match_option_on_the_top_bar(check_acca_bar=False)
