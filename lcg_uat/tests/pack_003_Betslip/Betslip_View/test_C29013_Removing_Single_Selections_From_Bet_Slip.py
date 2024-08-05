import pytest
import tests
import voltron.environments.constants as vec
from crlat_ob_client.utils.date_time import get_date_time_as_string
from collections import OrderedDict
from random import choice
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.helpers import normalize_name
from voltron.utils.waiters import wait_for_result


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.smoke
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.betslip
@pytest.mark.critical
@pytest.mark.issue('https://jira.egalacoral.com/browse/BMA-55981')
@vtest
class Test_C29013_Removing_Single_Selections_From_Bet_Slip(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C29013
    NAME: Removing Single Selections From Bet Slip
    DESCRIPTION: This test case verifies removing of <Sport> selections from Bet Slip.
    PRECONDITIONS: 1.  User can be logged in or logged out
    PRECONDITIONS: 2.  A few single bets should be placed in the Bet Slip
    """
    keep_browser_open = True
    events = {}
    league1, league2 = None, None
    end_date = f'{get_date_time_as_string(days=0)}T22:00:00.000Z'

    def test_000_preconditions(self):
        """
        DESCRIPTION: TST2/STG2: Create football events, PROD: Find 2 active football events
        """
        if tests.settings.backend_env == 'prod':
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         number_of_events=2)
            live_events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                              in_play_event=True,
                                                              all_available_events=True)
            if len(live_events) < 2:
                raise SiteServeException(f'No enough live events found for category id "{self.ob_config.football_config.category_id}"')

            # event 1
            self.__class__.eventID = events[0]['event']['id']
            self.__class__.created_event_name = normalize_name(events[0]['event']['name'])
            market_name, outcomes = next(((market['market']['name'], market['market']['children'])
                                          for market in events[0]['event']['children']
                                          if 'Match Betting' == market['market']['templateMarketName'] and
                                          market['market'].get('children')), None)
            if outcomes is None:
                raise SiteServeException('There are no available outcomes')

            # outcomeMeaningMinorCode: A - away, H - home, D - draw
            self.__class__.team1_1 = next((outcome['outcome']['name'] for outcome in outcomes if
                                           outcome['outcome'].get('outcomeMeaningMinorCode') and
                                           outcome['outcome']['outcomeMeaningMinorCode'] == 'H'), None)
            if not self.team1_1:
                raise SiteServeException('No Home team found')

            draw_name_ = next((outcome['outcome']['name'] for outcome in outcomes if
                               outcome['outcome'].get('outcomeMeaningMinorCode') and
                               outcome['outcome']['outcomeMeaningMinorCode'] == 'D'), None)

            if not draw_name_:
                raise SiteServeException('No Draw outcome found')

            self.__class__.draw_name = draw_name_.upper() if self.brand == 'ladbrokes' else draw_name_

            self.__class__.selection_ids = OrderedDict([(outcome['outcome']['name'],
                                                         outcome['outcome']['id']) for outcome in outcomes])

            self.__class__.league1 = self.get_accordion_name_for_event_from_ss(event=events[0])

            self.events[self.eventID] = self.created_event_name
            self.__class__.expected_betslip_counter_value += 1

            # event 2
            self.__class__.eventID_2 = events[1]['event']['id']
            self.__class__.created_event_2_name = normalize_name(events[1]['event']['name'])
            self.events[self.eventID_2] = self.created_event_2_name
            self.__class__.league2 = self.get_accordion_name_for_event_from_ss(event=events[1])
            self.__class__.expected_betslip_counter_value += 1

            # live event 1
            live_event1 = choice(live_events)
            live_events.remove(live_event1)

            self.__class__.live_eventID = live_event1['event']['id']
            self.__class__.event_name = normalize_name(live_event1['event']['name'])
            self.__class__.league1_live = self.get_accordion_name_for_event_from_ss(event=live_event1, in_play_tab_slp=True)

            # live event 2
            live_event2 = choice(live_events)
            self.__class__.live_eventID_2 = live_event2['event']['id']
            self.__class__.event_name_2 = normalize_name(live_event2['event']['name'])
            self.__class__.league2_live = self.get_accordion_name_for_event_from_ss(event=live_event2, in_play_tab_slp=True)

        else:
            event_params = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.eventID = event_params.event_id
            self.events[self.eventID] = f'{event_params.team1} v {event_params.team2}'
            self.__class__.team1_1, self.__class__.selection_ids = event_params.team1, event_params.selection_ids
            self.__class__.eventID = event_params.event_id
            event_params2 = self.ob_config.add_autotest_premier_league_football_event()

            self.__class__.eventID_2 = event_params2.event_id
            self.events[self.eventID_2] = f'{event_params2.team1} v {event_params2.team2}'
            self.__class__.expected_betslip_counter_value += 2
            actual_value = len(self.events.items())
            self.assertTrue(actual_value == self.expected_betslip_counter_value,
                            msg=f'Actual number of created events "{actual_value}" '
                            f'is not the same as expected "{self.expected_betslip_counter_value}"')
            self.__class__.league1 = self.__class__.league2 = tests.settings.football_autotest_league

            event_params_live = self.ob_config.add_autotest_premier_league_football_event(is_live=True)
            self.__class__.live_eventID = event_params_live.event_id
            self.__class__.event_name = event_params_live.team1 + ' v ' + event_params_live.team2

            event_params_live_2 = self.ob_config.add_autotest_premier_league_football_event(is_live=True)
            self.__class__.live_eventID_2 = event_params_live_2.event_id
            self.__class__.event_name_2 = event_params_live_2.team1 + ' v ' + event_params_live_2.team2
            self.__class__.league1_live = self.__class__.league2_live = f'{tests.settings.football_autotest_competition} - {tests.settings.football_autotest_competition_league}'\
                if self.device_type == 'desktop'else tests.settings.football_autotest_competition_league
            market_name = normalize_name(
                self.ob_config.football_config.autotest_class.autotest_premier_league.market_name)
            self.__class__.draw_name = 'DRAW' if self.brand == 'ladbrokes' else 'Draw'

        self.__class__.expected_market_name = self.get_accordion_name_for_market_from_ss(ss_market_name=market_name)

    def test_001_tap_sport_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Sport> icon on the Sports Menu Ribbon
        EXPECTED: - <Sport> Landing Page is opened
        EXPECTED: - 'Today' tab is opened by default
        """
        self.site.open_sport(name='FOOTBALL')

    def test_002_make_a_few_single_selections_from_the_sport_landing_page(self):
        """
        DESCRIPTION: Make a few single selections from the <Sport> Landing Page
        """
        event = self.get_event_from_league(event_id=self.eventID,
                                           section_name=self.league1)
        output_prices = event.get_active_prices()
        self.assertTrue(output_prices,
                        msg=f'Could not find output prices for created event "{list(self.events.values())[0]}"')
        self.__class__.selection_name, selection_price = list(output_prices.items())[0]

        selection_price.click()
        if self.device_type == 'mobile':
            self.site.add_first_selection_from_quick_bet_to_betslip()
        self.assertTrue(selection_price.is_selected(timeout=2),
                        msg=f'Bet button "{self.selection_name}" is not active after selection')

        event2 = self.get_event_from_league(event_id=self.eventID_2,
                                            section_name=self.league2)
        output_prices2 = event2.get_active_prices()
        self.assertTrue(output_prices2,
                        msg=f'Could not find output prices for created event "{list(self.events.values())[1]}"')
        self.__class__.selection_name2, selection_price2 = list(output_prices2.items())[2]
        selection_price2.scroll_to()
        selection_price2.click()
        self.assertTrue(selection_price2.is_selected(timeout=2),
                        msg=f'Bet button {self.selection_name2} is not active after selection')

    def test_003_go_to_the_bet_slip_and_enter_stakes_for_added_selections(self):
        """
        DESCRIPTION: Go to the Bet Slip and enter Stakes for added selections
        EXPECTED: - Bet Slip page is opened.
        EXPECTED: - Selections are displayed in Bet Slip
        EXPECTED: - Stakes are entered
        """
        self.site.open_betslip()
        self.site.close_all_dialogs()
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section.items(), msg='*** No stakes found')

        self.__class__.stake = singles_section.get(self.selection_name)
        self.assertTrue(self.stake, msg=f'"{self.selection_name}" stake was not found')

        stake2 = singles_section.get(self.selection_name2)
        self.assertTrue(stake2, msg=f'"{self.selection_name2}" stake was not found')
        self.enter_stake_amount(stake=(self.stake.name, self.stake))
        self.enter_stake_amount(stake=(stake2.name, stake2))

    def test_004_remove_one_of_the_selections_via_x_button_within_selection_section(self):
        """
        DESCRIPTION: Remove one of the selections via 'x' button within selection section
        EXPECTED: 1.  Bet is removed from the Bet Slip
        EXPECTED: 2.  The counter in the 'Single' section header is decremented by 1
        EXPECTED: 3.  The betslip counter in the Global Header is decremented by 1
        EXPECTED: 4.  The 'Total Stake' field is decremented by stake defined in the bet removed
        EXPECTED: 5.  The 'Total Est. Returns' field is decremented by the estimated return in bet removed
        """
        selections_count = int(self.get_betslip_content().selections_count)
        total_stake = float(self.get_betslip_content().total_stake)
        est_returns = float(self.get_betslip_content().total_estimate_returns)
        stake_est_returns = float(self.stake.est_returns)
        self.stake.remove_button.click()
        singles_section = self.get_betslip_sections().Singles
        stakes = singles_section.keys()
        self.assertTrue(len(stakes) == 1, msg='Only one Stake should be present')
        selections_count_after_x = int(self.get_betslip_content().selections_count)
        total_stake_after_x = float(self.get_betslip_content().total_stake)
        est_returns_after_x = float(self.get_betslip_content().total_estimate_returns)
        calculated_expected_est_returns = float("{0:.2f}".format(est_returns - stake_est_returns))
        self.assertEqual((selections_count - 1), selections_count_after_x, msg=f'Expected counter {selections_count - 1},'
                         f' showed {selections_count_after_x}')
        total_stake_updated = total_stake - self.bet_amount
        self.assertEqual(total_stake_updated, total_stake_after_x, msg=f'Expected stake {total_stake_updated},'
                         f' showed {total_stake_after_x}')
        self.assertEqual(calculated_expected_est_returns, est_returns_after_x, msg=f'Expected stake {calculated_expected_est_returns},'
                         f' showed {est_returns_after_x}')

    def test_005_unselect_one_of_the_selections_from_the_event_page_go_to_the_betslip(self):
        """
        DESCRIPTION: Unselect one of the selections from the event page -> go to the Betslip
        EXPECTED: 1.  Bet is no more displayed on the Bet Slip
        EXPECTED: 2.  The counter in the Your Selections section header is decremented by 1
        EXPECTED: 3.  The betslip counter in the Global Header is decremented by 1
        EXPECTED: 4.  The 'Total Stake' field is decremented by stake defined in the bet removed
        EXPECTED: 5.  The 'Total Est. Returns' field is decremented by the estimated return in bet removed
        """
        self.site.close_betslip()

        event2 = self.get_event_from_league(event_id=self.eventID_2,
                                            section_name=self.league2)
        output_prices2 = event2.get_active_prices()
        self.assertTrue(output_prices2,
                        msg=f'Could not find output prices for created event "{list(self.events.values())[1]}"')
        output_prices2[self.selection_name2].click()
        self.assertFalse(output_prices2[self.selection_name2].is_selected(expected_result=False, timeout=2),
                         msg=f'Selection "{self.selection_name2}" is still highlighted after deselection')

        self.verify_betslip_counter_change(expected_value=0)

    def test_006_remove_all_selections_via_x_button_within_each_selection_section(self):
        """
        DESCRIPTION: Remove all selections via 'x' button within each selection section
        EXPECTED: 1.  All selections are removed from the Bet Slip
        EXPECTED: 2.  Betslip Overlay is closed (**for Mobile**)
        EXPECTED: 3.  The following message is displayed on the Betslip widget (**for Tablet and Mobile**): ***'You have no selections in the slip.'***
        """
        if self.device_type == 'mobile':
            self.assertFalse(self.site.has_betslip_opened(expected_result=False), msg='Betslip is not closed')
        else:
            betslip = self.get_betslip_content()
            no_selections_title = betslip.no_selections_title
            self.assertTrue(no_selections_title, msg=f'"{vec.betslip.NO_SELECTIONS_TITLE}" title is not shown')
            self.assertEqual(no_selections_title, vec.betslip.NO_SELECTIONS_TITLE,
                             msg=f'Title "{no_selections_title}" is not as expected "{vec.betslip.NO_SELECTIONS_TITLE}"')

    def test_007_add_only_one_bet_to_the_betslip(self):
        """
        DESCRIPTION: Add ONLY one bet to the betslip
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_ids[self.team1_1])

    def test_008_go_to_the_bet_slip_remove_selection_via_x_button(self):
        """
        DESCRIPTION: Go to the Bet Slip -> remove selection via  'x' button
        EXPECTED: 1.  All selections are removed from the Bet Slip
        EXPECTED: 2.  Betslip Overlay is closed (**for Mobile**)
        EXPECTED: 3.  The following message is displayed on the Betslip widget (**for Tablet and Mobile**): ***'You have no selections in the slip.'***
        """
        singles_section = self.get_betslip_sections().Singles
        stake = singles_section.get(self.selection_name)
        self.assertTrue(stake, msg=f'"{self.selection_name}" stake was not found')
        stake.remove_button.click()
        self.test_006_remove_all_selections_via_x_button_within_each_selection_section()

    def test_009_add_selection_to_the_bet_slip_from_the_event_details_page(self):
        """
        DESCRIPTION: Add selection to the Bet Slip from the event details page
        EXPECTED: Selection is added
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='football')
        bet_button = self.get_selection_bet_button(selection_name=self.draw_name, market_name=self.expected_market_name)
        bet_button.click()
        if self.device_type == 'mobile':
            self.site.add_first_selection_from_quick_bet_to_betslip(timeout=15)
            self.assertTrue(bet_button.is_selected(timeout=3), msg='Outcome button is not highlighted in green')
        self.__class__.expected_betslip_counter_value = 1

        self.verify_betslip_counter_change(expected_value=self.expected_betslip_counter_value)

    def test_010_repeat_steps_4_9(self):
        """
        DESCRIPTION: Repeat steps № 4 - 9
        """
        self.site.open_betslip()
        self.site.close_all_dialogs()
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section.items(), msg='*** No stakes found')
        stake = singles_section.get('Draw')
        self.assertTrue(stake, msg=f'Draw stake was not found')
        self.enter_stake_amount(stake=(stake.name, stake))
        stake.remove_button.click()
        self.test_006_remove_all_selections_via_x_button_within_each_selection_section()

    def test_011_navigate_to_in_play_page_add_any_3_selections_from_different_events(self):
        """
        DESCRIPTION: Navigate to In-Play page
        DESCRIPTION: Add several selections from different events
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name='football')
        self.site.football.tabs_menu.click_button(self.expected_sport_tabs.in_play)
        current_tab = self.site.football.tabs_menu.current
        self.assertEqual(current_tab, self.expected_sport_tabs.in_play,
                         msg=f'"{self.expected_sport_tabs.in_play}" tab is not selected after click, '
                         f'active tab is "{current_tab}"')

        event = self.get_event_from_league(event_id=self.live_eventID,
                                           section_name=self.league1_live)
        output_prices = event.get_active_prices()
        self.assertTrue(output_prices,
                        msg=f'Could not find output prices for created event "{self.event_name}"')

        self.__class__.selection_name, self.__class__.selection_price = choice(list(output_prices.items()))
        self.selection_price.scroll_to()
        self.device.driver.implicitly_wait(0.7)
        if tests.settings.backend_env == 'prod' and not self.selection_price.is_enabled():
            self.device.driver.implicitly_wait(0)
            self._logger.info(f'*** Selection "{self.selection_name}" is disabled, doing preconditions again')
            self.test_000_preconditions()
            event = self.get_event_from_league(event_id=self.live_eventID,
                                               section_name=self.league1_live,
                                               inplay_section=vec.inplay.LIVE_NOW_SWITCHER)
            output_prices = event.get_active_prices()
            self.assertTrue(output_prices,
                            msg=f'Could not find output prices for created event "{self.event_name}"')

            self.__class__.selection_name, self.__class__.selection_price = choice(list(output_prices.items()))
            self.selection_price.scroll_to()
            self.device.driver.implicitly_wait(0.7)

        self.selection_price.click()
        result = wait_for_result(
            lambda: self.selection_price.is_selected(timeout=2) is True,
            timeout=30,
            name='Selection is selected')
        self.assertTrue(result, msg=f'Bet button {self.selection_name} is not active after selection')
        if self.device_type == 'mobile':
            self.site.add_first_selection_from_quick_bet_to_betslip()

        event2 = self.get_event_from_league(event_id=self.live_eventID_2,
                                            section_name=self.league2_live)
        output_prices2 = event2.get_active_prices()
        self.assertTrue(output_prices2,
                        msg=f'Could not find output prices for created event "{self.event_name_2}"')
        self.__class__.selection_name2, self.__class__.selection_price2 = choice(list(output_prices2.items()))
        self.selection_price2.scroll_to()
        self.device.driver.implicitly_wait(0.7)
        self.selection_price2.click()
        result = wait_for_result(
            lambda: self.selection_price.is_selected(timeout=2) is True,
            timeout=30,
            name='Selection is selected')
        self.assertTrue(result, msg=f'Bet button {self.selection_name2} is not active after selection')

    def test_012_open_and_close_bet_slip(self):
        """
        DESCRIPTION: Open and close Bet Slip
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.site.open_betslip()
        self.site.close_all_dialogs(timeout=3)
        singles_section = self.get_betslip_sections().Singles
        singles_length = len(singles_section.items())
        self._logger.info('*** Singles section length %s' % singles_length)
        self.assertTrue(wait_for_result(lambda: singles_length == 2, timeout=10),
                        msg='There should be 2 singles stakes in betslip')

        self.site.close_betslip()
        if self.device_type == 'mobile':
            self.assertFalse(self.site.has_betslip_opened(expected_result=False, timeout=3),
                             msg='Betslip was not closed')

    def test_013_on_in_play_page_click_on_the_several_selections_again_to_remove_them_from_bet_slip(self):
        """
        DESCRIPTION: On In-Play page click on the same selections again to remove them from Bet Slip
        """
        event = self.get_event_from_league(event_id=self.live_eventID,
                                           section_name=self.league1_live)
        output_prices = event.get_active_prices()
        self.assertTrue(output_prices,
                        msg=f'Could not find output prices for created event "{self.event_name}"')
        selection_price = output_prices.get(self.selection_name)
        self.assertTrue(selection_price, msg=f'No active price found for selection "{self.selection_name}"')
        selection_price.click()
        self.assertFalse(selection_price.is_selected(expected_result=False, timeout=4),
                         msg=f'Bet button "{self.selection_name}" is active after unselection')

        event2 = self.get_event_from_league(event_id=self.live_eventID_2,
                                            section_name=self.league2_live)
        output_prices2 = event2.get_active_prices()
        self.assertTrue(output_prices2,
                        msg=f'Could not find output prices for created event "{self.event_name_2}"')
        selection_price2 = output_prices2.get(self.selection_name2)
        self.assertTrue(selection_price2, msg=f'No active price found for selection "{self.selection_name2}"')
        selection_price2.scroll_to()
        selection_price2.click()
        self.assertFalse(selection_price2.is_selected(expected_result=False, timeout=4),
                         msg=f'Bet button {self.selection_name2} is active after unselection')

    def test_014_open_bet_slip(self):
        """
        DESCRIPTION: Open Bet Slip
        EXPECTED: 1.  All selections are removed from the Bet Slip
        EXPECTED: 2.  The following message is displayed on the Betslip: ***'You have no selections in the slip.'***
        """
        self.site.open_betslip()
        betslip = self.get_betslip_content()
        no_selections_title = betslip.no_selections_title
        self.assertTrue(no_selections_title, msg=f'"{vec.betslip.NO_SELECTIONS_TITLE}" title is not shown')
        self.assertEqual(no_selections_title, vec.betslip.NO_SELECTIONS_TITLE,
                         msg=f'Title "{no_selections_title}" is not as expected "{vec.betslip.NO_SELECTIONS_TITLE}"')

        if self.device_type == 'mobile':
            no_selections_message = betslip.no_selections_message
            self.assertTrue(no_selections_message, msg=f'"{vec.betslip.NO_SELECTIONS_MSG}" message is not shown')
            self.assertEqual(no_selections_message, vec.betslip.NO_SELECTIONS_MSG,
                             msg=f'Message "{no_selections_message}" is not as expected "{vec.betslip.NO_SELECTIONS_MSG}"')
