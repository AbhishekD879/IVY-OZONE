from collections import OrderedDict
from datetime import datetime
import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_011_RACES_Specifics.Horse_Racing_Specifics.Horse_Racing_Event_Details_Page.Tote_Pool_tab.BaseInternationalTote import BaseInternationalTote
from voltron.utils.bpp_config import BPPConfig


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod  # cannot place bet on International Tote on production. Tested without placing bet
@pytest.mark.hl
@pytest.mark.critical
@pytest.mark.desktop
@pytest.mark.races
@pytest.mark.international_tote
@pytest.mark.tote
@pytest.mark.login
@pytest.mark.frequent_blocker
@vtest
class Test_C2912431_Verify_International_Tote_Place_Bet_Placement(BaseInternationalTote, BaseBetSlipTest):
    """
    TR_ID: C2912431
    NAME: Verify International Tote Place Bet Placement
    DESCRIPTION: This test case verifies bet placement on Place pool type on International tote
    DESCRIPTION: Please note that we are **NOT** **ALLOWED** to Place a Tote bets on HL and PROD environments!
    PRECONDITIONS: * The User's account balance is sufficient to cover the bet stake
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * International Tote feature is enabled in CMS
    PRECONDITIONS: * Place pool types are available for International  HR Event
    PRECONDITIONS: * User should have a Horse Racing event detail page open ("Tote" tab)
    PRECONDITIONS: * User should have a Place pool type open
    """
    keep_browser_open = True
    added_runners = OrderedDict()
    selection_name = f'{vec.tote.PL} {vec.tote.TOTEPOOL}'
    bpp_config = BPPConfig()
    exchange_rates = {}

    def test_000_preconditions(self):
        """
        DESCRIPTION: Find Racing event with International tote Win pool
        DESCRIPTION: Login
        """
        event = self.get_int_tote_event(int_tote_place=True)
        self._logger.info(f'*** Found event with parameters "{event}"')
        self.__class__.eventID = event.event_id
        self.__class__.event_typename = event.event_typename.strip()
        self.__class__.currency_code = event.currency_code
        self.site.login()

        self.__class__.bet_amount = f'{event.min_total_stake:.2f}'
        self.__class__.exchange_rates = self.bpp_config.get_currency_exchange_rates()
        self._logger.info(f'*** Exchange rates: "{self.exchange_rates}"')
        exchange_rate = self.exchange_rates[self.currency_code]
        self.__class__.expected_converted_total_stake_amount = f'{(float(self.bet_amount) / exchange_rate ) * 2:.2f}'

    def test_001_select_any_runners_press_place_button_and_tap_add_to_betslip_button_on_place_tote_bet_builder(self):
        """
        DESCRIPTION: Select any runners (press Place button) and tap "ADD TO BETSLIP" button on Place tote bet builder
        EXPECTED: * Tote Place bet is added to BetSlip
        EXPECTED: * Bet builder disappears
        EXPECTED: * Betslip is increased by 1 number indicator
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')

        tab_content = self.site.racing_event_details.tab_content
        tab_opened = tab_content.event_markets_list.market_tabs_list.open_tab(vec.racing.RACING_EDP_MARKET_TABS.totepool)
        self.assertTrue(tab_opened, msg=f'"{vec.racing.RACING_EDP_MARKET_TABS.totepool}" tab is not opened')
        self.__class__.event_off_time = tab_content.event_off_times_list.selected_item
        sections = tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        section_name, section = list(sections.items())[0]
        place_tab_opened = section.grouping_buttons.click_button(vec.tote.TOTE_TABS.place)
        self.assertTrue(place_tab_opened, msg=f'"{vec.tote.TOTE_TABS.place}" tab is not opened')

        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        section_name, section = list(sections.items())[0]
        outcomes = section.pool.items_as_ordered_dict
        self.assertTrue(all(outcomes), msg='No outcomes found')
        active_outcomes = [(outcome_name, outcome) for (outcome_name, outcome) in outcomes.items() if
                           outcome.is_enabled()]
        _temp = []
        for outcome_name, outcome in active_outcomes[:2]:
            cells = outcome.items
            self.assertTrue(cells, msg=f'No cells found for "{outcome_name}"')
            cell = cells[0]
            cell.click()
            self.assertTrue(cell.is_selected(timeout=2),
                            msg=f'Place cell is not selected for "{outcome_name}" runner')
            _temp.append((outcome_name, outcome.runner_number if outcome.runner_number else None))

        self.added_runners = OrderedDict(_temp)

        bet_builder = section.bet_builder
        self.assertTrue(bet_builder.is_displayed(timeout=3), msg='Bet builder is not shown')
        self.assertTrue(bet_builder.summary.add_to_betslip_button.is_enabled(timeout=3),
                        msg=f'"{vec.quickbet.BUTTONS.add_to_betslip}" button is not clickable')
        bet_builder.summary.add_to_betslip_button.click()
        self.__class__.expected_betslip_counter_value += 1
        self.assertFalse(bet_builder.is_displayed(expected_result=False, timeout=3),
                         msg='Bet builder still shown on the screen')

    def test_002_open_betslip_and_verify_the_place_tote_bet(self):
        """
        DESCRIPTION: Open BetSlip and verify the Place tote bet
        EXPECTED: * The bet section is collapsed by default
        EXPECTED: * It is possible to expand the tote bet by clicking on the **+** button
        EXPECTED: * There is a "remove" button to remove the place tote bet from the betslip
        """
        self.verify_betslip_counter_change(expected_value=self.expected_betslip_counter_value)

        self.site.open_betslip()
        self.__class__.singles_section = self.get_betslip_sections().Singles
        self.assertIn(self.selection_name, self.singles_section, msg='Tote Place bet is not added to BetSlip')

        self.__class__.place_tote_stake = self.singles_section[self.selection_name]
        section_name = self.place_tote_stake.name
        self.assertTrue(self.place_tote_stake.has_event_name,
                        msg=f'"{section_name}" bet section is not expanded, event name is not shown')
        self.assertTrue(self.place_tote_stake.has_event_date,
                        msg=f'"{section_name}" bet section is not expanded, event date is not shown')

        self.assertTrue(self.place_tote_stake.remove_button.is_displayed(),
                        msg=f'"Remove" button is not available for "{section_name}" stake')

    def test_003_verify_bet_details_for_place_tote_bet(self):
        """
        DESCRIPTION: Verify bet details for Place tote bet
        EXPECTED: There are the following details on place tote bet:
        EXPECTED: * "Singles (1)" label in the section header
        EXPECTED: * "Place Totepool"
        EXPECTED: * "Place" bet type name (eg. 1 Place Selection)
        EXPECTED: * All selections with correct order according to the selected runners
        """
        self.assertEqual(self.singles_section.name, vec.betslip.BETSLIP_SINGLES_NAME,
                         msg=f'Section title "{self.singles_section.name}" is not the same '
                             f'as expected "{vec.betslip.BETSLIP_SINGLES_NAME}"')
        selections_count = self.get_betslip_content().selections_count

        self.assertEqual(int(selections_count), self.expected_betslip_counter_value,
                         msg=f'Singles selection count "{int(selections_count)}" is not the same '
                             'as expected "{self.expected_betslip_counter_value)}"')

        self.assertEqual(self.place_tote_stake.outcome_name, self.selection_name,
                         msg=f'Actual outcome name "{self.place_tote_stake.outcome_name}" is not '
                             'the same as expected "{self.selection_name}"')

        self.assertEqual(self.place_tote_stake.market_name, vec.uk_tote.MULTIPLE_SELECTIONS_PLACE_BET.format(number=2),
                         msg=f'Actual bet type "{self.place_tote_stake.market_name}" is not the same'
                             f' as expected "{vec.uk_tote.MULTIPLE_SELECTIONS_PLACE_BET.format(number=2)}"')

        selection_outcomes = self.place_tote_stake.tote_outcomes.items_as_ordered_dict
        self.assertTrue(selection_outcomes, msg='No International Tote selections found')
        for selection_name, expected_selection_name in zip(selection_outcomes.keys(), self.added_runners.keys()):
            self.assertEqual(selection_name, expected_selection_name,
                             msg=f'Selected runner "{selection_name}" is not the same '
                                 f'as expected "{expected_selection_name}"')

    def test_004_expand_the_bet_and_verify_the_start_date_and_time_of_the_race(self):
        """
        DESCRIPTION: Expand the bet and verify the start date and time of the race
        EXPECTED: * Time of the race is shown when the bet is expanded
        EXPECTED: * Format is the following:
        EXPECTED: HH:MM <event name>
        EXPECTED: <event start date>
        """
        expected_event_title = f'{self.event_off_time} {self.event_typename}'
        self.assertIn(expected_event_title, self.place_tote_stake.event_name,
                      msg=f'Actual event name "{self.place_tote_stake.event_name}" is not'
                          f' the same as expected "{expected_event_title}"')
        self.assertTrue(any([self.place_tote_stake.event_date in ['Today', datetime.today().strftime('%A')]]),
                        msg=f'Actual event date: "{self.place_tote_stake.event_date}" is not the same '
                            f'as expected: "Today" or "{datetime.today().strftime("%A")}"')

    def test_005_verify_stake_field(self):
        """
        DESCRIPTION: Verify "Stake" field
        EXPECTED: * User is able to set the stake using the BetSlip keyboard (mobile)
        EXPECTED: * User is able to modify stake
        EXPECTED: * "Total stake" value changes accordingly
        """
        self.enter_stake_amount(stake=(self.place_tote_stake.name, self.place_tote_stake))
        total_stake = self.get_betslip_content().total_stake
        self.assertEqual(total_stake, self.expected_converted_total_stake_amount,
                         msg=f'Actual total stake amount value "{total_stake}" is not '
                             f'the same as expected "{self.expected_converted_total_stake_amount}"')

    def test_006_verify_estimated_returns(self):
        """
        DESCRIPTION: Verify "Estimated Returns"
        EXPECTED: Estimated Returns values are "N/A" for Tote bets
        """
        self.assertEqual(self.place_tote_stake.est_returns, 'N/A',
                         msg=f'Est. Returns value: "{self.place_tote_stake.est_returns}" '
                             f'is not the same as expected: "N/A"')

    def test_007_verify_total_stake_and_total_est_returns(self):
        """
        DESCRIPTION: Verify "Total Stake" and "Total Est. Returns"
        EXPECTED: * Total stake value corresponds to the actual total stake based on the stake value entered
        EXPECTED: * Total Est. Returns value is "N/A"
        """
        self.assertEqual(self.get_betslip_content().total_estimate_returns, 'N/A',
                         msg=f'Total Est. Returns: "{self.get_betslip_content().total_estimate_returns}"'
                             ' is not the same as expected: "N/A"')

    def test_008_tap_the_remove_button(self):
        """
        DESCRIPTION: Tap the "remove" button
        EXPECTED: Bet is removed from the BetSlip
        """
        self.place_tote_stake.remove_button.click()
        if self.device_type == "mobile":
            result = self.site.has_betslip_opened(expected_result=False)
            self.assertFalse(result, msg='Betslip should not be displayed')
        else:
            betslip = self.get_betslip_content()
            no_selections_title = betslip.no_selections_title
            self.assertTrue(no_selections_title, msg=f'"{vec.betslip.NO_SELECTIONS_TITLE}" title is not shown')
            self.assertEqual(no_selections_title, vec.betslip.NO_SELECTIONS_TITLE,
                             msg=f'Title "{no_selections_title}" is not as expected "{vec.betslip.NO_SELECTIONS_TITLE}"')

    def test_009_place_bet_once_again(self):
        """
        DESCRIPTION: Place bet once again
        EXPECTED: * Place Tote bet is successfully placed
        EXPECTED: * Place Tote Bet receipt is shown
        """
        self.test_001_select_any_runners_press_place_button_and_tap_add_to_betslip_button_on_place_tote_bet_builder()
        self.site.open_betslip()
        self.__class__.singles_section = self.get_betslip_sections().Singles
        self.assertIn(self.selection_name, self.singles_section, msg='Tote Place bet is not added to BetSlip')

        self.__class__.place_tote_stake = self.singles_section[self.selection_name]

        self.test_005_verify_stake_field()
        if tests.settings.backend_env != 'prod':
            # cannot place bet on International Tote on production
            self.get_betslip_content().bet_now_button.click()

            self.check_bet_receipt_is_displayed()
