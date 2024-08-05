from collections import OrderedDict

import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # cannot suspend selection
# @pytest.mark.hl    # cannot suspend selection
@pytest.mark.sports
@pytest.mark.football
@pytest.mark.in_play
@pytest.mark.liveserv_updates
@pytest.mark.desktop
@pytest.mark.slow
@pytest.mark.medium
@pytest.mark.safari
@vtest
class Test_C141197_Verify_displaying_of_suspended_selection_on_Sport_In_Play_page_widget_when_it_is_added_to_the_betslip(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C141197
    NAME: Verify displaying of suspended selection on <Sport> In-Play page/widget when it is added to the betslip
    DESCRIPTION: This test case verifies displaying of suspended selection on <Sport> In-Play page/widget when it is added to the betslip
    PRECONDITIONS: - LiveServer is available only for In-Play <Sport> events with the following attributes:
    PRECONDITIONS: drilldownTagNames="EVFLAG_BL"
    PRECONDITIONS: isMarketBetInRun = "true"
    PRECONDITIONS: - To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: - To verify suspension check new received value in "status" attribute using Dev Tools-> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: EVENT/EVMKT/SELCN depend on level of triggering suspension event/market/selection
    PRECONDITIONS: *NOTE:* *pushes with LiveServe updates also are received if selection is added to the betslip*
    """
    keep_browser_open = True
    output_price = None
    initial_output_prices = None
    expected_betslip_counter_value = 1
    sport_name = vec.sb.FOOTBALL
    initial_prices = {'odds_home': '1/12', 'odds_draw': '1/13', 'odds_away': '1/14'}

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add 'Football' live event
        """
        start_time = self.get_date_time_formatted_string(seconds=10)
        event_params = self.ob_config.add_autotest_premier_league_football_event(is_live=True, start_time=start_time,
                                                                                 lp=self.initial_prices)

        self.__class__.event_name = event_params.team1 + ' v ' + event_params.team2
        self.__class__.eventID, self.__class__.team1, self.__class__.selection_ids = \
            event_params.event_id, event_params.team1, event_params.selection_ids

        self.__class__.league = f'{tests.settings.football_autotest_competition} - ' \
                                f'{tests.settings.football_autotest_competition_league}' \
            if self.device_type == 'desktop' else tests.settings.football_autotest_competition_league

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is loaded
        """
        self.site.wait_content_state(state_name='Home')

    def test_002_navigate_to_sports_landing_page_from_sports_ribbon_left_navigation_menu(self):
        """
        DESCRIPTION: Navigate to Sports Landing page from Sports Ribbon/Left Navigation menu
        EXPECTED: <Sport> Landing page is opened
        """
        self.site.open_sport(name=self.sport_name)
        active_tab = self.site.football.tabs_menu.current
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                    self.ob_config.football_config.category_id)
        self.assertEqual(active_tab, expected_tab_name,
                         msg=f'Actual tab name: "{active_tab}" is not as expected: "{expected_tab_name}"')

    def test_003_open_in_play_page_for_particular_sport(self):
        """
        DESCRIPTION: Open 'In-Play' page for particular Sport
        EXPECTED: 'In-Play' page is opened
        """
        in_play_tab = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.in_play,
                                              self.ob_config.basketball_config.category_id)
        tab_opened = self.site.football.tabs_menu.click_button(in_play_tab)
        self.assertTrue(tab_opened, msg=f'"{in_play_tab}" tab was not opened')

    def test_004_verify_the_price_odds_buttons_view_of_the_events_displayed(self):
        """
        DESCRIPTION: Verify the 'Price/Odds' buttons view of the events displayed
        EXPECTED: 'Price/Odds' buttons display price received from backend on light grey background
        """
        self.site.wait_content_state_changed(timeout=20)
        if self.device_type == 'mobile':
            selector = self.site.inplay.tab_content.dropdown_market_selector
            selector.items_as_ordered_dict['Match Result'].click()
        if not self.device_type == 'mobile':
            self.device.refresh_page()
            self.device.refresh_page()
        self.site.wait_content_state_changed(timeout=20)
        event = self.get_event_from_league(event_id=self.eventID,
                                           section_name=self.league)
        self.__class__.initial_output_prices = event.get_active_prices()
        self.__class__.expected_prices = OrderedDict()
        for sel_name, sel in self.initial_output_prices.items():
            self.expected_prices[sel_name] = sel.outcome_price_text
        self.verify_prices_not_suspended(initial_output_prices=self.initial_output_prices)

    def test_005_click_tap_on_price_odds_button_and_check_its_displaying(self):
        """
        DESCRIPTION: Click/Tap on Price/Odds button and check it's displaying
        EXPECTED: Selected Price/Odds button is marked as added to Betslip (becomes green)
        """
        event = self.get_event_from_league(event_id=self.eventID,
                                           section_name=self.league)
        actual_prices = event.get_active_prices()
        self.__class__.output_price = list(actual_prices.values())[0]
        self.__class__.output_price.click()

        if self.device_type in ['mobile', 'tablet']:
            self.site.add_first_selection_from_quick_bet_to_betslip()

    def test_006_verify_that_selection_is_added_to_bet_slip(self):
        """
        DESCRIPTION: Verify that selection is added to Bet Slip
        EXPECTED: Selection is present in Bet Slip and counter is increased on header
        """
        self.site.open_betslip()
        singles_section = self.get_betslip_sections().Singles
        stake = singles_section.get(self.team1)
        self.assertTrue(stake, msg=f'Stake: "{self.team1}" not found in the Bet Slip')

        selections_count = self.get_betslip_content().selections_count
        self.assertEqual(int(selections_count), self.expected_betslip_counter_value,
                         msg=f'Actual Bet Slip counter value: "{int(selections_count)}" '
                             f'is not as expected: "{self.expected_betslip_counter_value}"')
        self.site.close_betslip()

    def test_007_suspend_the_outcome_and_at_the_same_time_have_sport_in_play_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Trigger the following situation for this outcome:
        DESCRIPTION: outcomeStatusCode = 'S'
        DESCRIPTION: and at the same time have <Sport> In-Play page opened to watch for updates
        """
        self.ob_config.change_selection_state(selection_id=self.selection_ids[self.team1], displayed=True, active=False)

    def test_008_verify_outcome_for_the_event(self):
        """
        DESCRIPTION: Verify outcome for the event
        EXPECTED: * Price/Odds button for selected outcome is displayed immediately as greyed out and become disabled on <Sport> In-Play page
        EXPECTED: * Price is still displaying on the Price/Odds button
        EXPECTED: * Price/Odds button is not marked as added to Betslip (is not green anymore)
        """
        event = self.site.contents.tab_content.accordions_list.get_event_from_league_by_event_id(
            league=self.league, event_id=self.eventID)
        self.assertTrue(event, msg=f'Event with name "{self.event_name}" not found')
        price_buttons = list(event.get_all_prices().items())
        self.assertTrue(price_buttons, msg='Price buttons are not displayed')
        actual_prices = OrderedDict()
        for selection_name, outputprice in price_buttons:
            actual_prices[selection_name] = outputprice.outcome_price_text
        self.verify_prices(actual_prices=actual_prices, expected_prices=self.expected_prices)
        self.assertFalse(self.output_price.is_enabled(timeout=20, expected_result=False),
                         msg=f'Price is not suspended for:"{self.team1}"')

    def test_009_activate_the_outcome_and_at_the_same_time_have_sport_in_play_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Change attribute for this outcome:
        DESCRIPTION: outcomeStatusCode = 'A'
        DESCRIPTION: and at the same time have <Sport> In-Play page opened to watch for updates
        """
        self.ob_config.change_selection_state(selection_id=self.selection_ids[self.team1], displayed=True, active=True)

    def test_010_verify_outcome_for_the_event(self):
        """
        DESCRIPTION: Verify outcome for the event
        EXPECTED: * Price/Odds button for selected outcome is no more disabled, it becomes active immediately
        EXPECTED: * Price/Odds button is marked as added to Betslip (Becomes green)
        """
        event = self.site.contents.tab_content.accordions_list.get_event_from_league_by_event_id(
            league=self.league, event_id=self.eventID)
        self.assertTrue(event, msg=f'Event with name"{self.event_name}"not found')
        price_buttons = list(event.get_all_prices().items())
        self.assertTrue(price_buttons, msg='Price buttons are not displayed')
        actual_prices = OrderedDict()
        for selection_name, outputprice in price_buttons:
            actual_prices[selection_name] = outputprice.outcome_price_text
        self.verify_prices(actual_prices=actual_prices, expected_prices=self.expected_prices)
        self.assertTrue(self.output_price.is_enabled(timeout=2), msg=f'Price is suspended for:"{self.team1}"')

    def test_011_for_desktop_navigate_to_sports_landing_page_from_sports_ribbon_left_navigation_menu(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Navigate to Sports Landing page (make sure that Sport has available live events) from Sports Ribbon/Left Navigation menu
        EXPECTED: * Sports Landing page is opened
        EXPECTED: * 'Matches' tab is selected by default
        EXPECTED: * In-Play widget with available live events for particular Sport is displayed in 3-rd Service column
        """
        # Verified for desktop in previous steps
        pass

    def test_012_for_desktop_repeat_steps_4_10(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Repeat steps 4-10
        """
        # Verified for desktop in previous steps
        pass

    def test_013_for_desktop_navigate_to_event_details_page_of_live_event(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Navigate to Event Details page of Live event
        EXPECTED: * Event Details page is opened
        EXPECTED: * In-Play widget with available live events for particular Sport is displayed in 3-rd Service column
        """
        # TODO https://jira.egalacoral.com/browse/VOL-1970
        pass

    def test_014_for_desktop_repeat_steps_4_10(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Repeat steps 4-10
        """
        # TODO https://jira.egalacoral.com/browse/VOL-1970
        pass
