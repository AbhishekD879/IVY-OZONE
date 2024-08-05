import voltron.environments.constants as vec
import time

import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_012_UK_Tote.BaseUKTote import BaseUKTote
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod - we are NOT ALLOWED to Place a Tote bets on HL and PROD environments
# @pytest.mark.hl
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.uk_tote
@pytest.mark.critical
@pytest.mark.desktop
@pytest.mark.races
@pytest.mark.login
@vtest
class Test_C2912270_Verify_UK_Tote_Place_Bet_Placement(BaseUKTote, BaseBetSlipTest):
    """
    TR_ID: C2912270
    NAME: Verify UK Tote Place Bet Placement
    DESCRIPTION: This test case verifies bet placement on Place UK tote
    PRECONDITIONS: * The User's account balance is sufficient to cover the bet stake
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * UK Tote feature is enabled in CMS
    PRECONDITIONS: * Place pool types are available for HR Event
    PRECONDITIONS: * User should have a Horse Racing event detail page open ("Tote" tab)
    PRECONDITIONS: * User should have a Place pool type open
    PRECONDITIONS: * To load Totepool ON/OFF CMS config use System-configuration (https://coral-cms- **endpoint** .symphony-solutions.eu)
    PRECONDITIONS: **endpoint** can be found using devlog
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Find HR event with available Place pool type
        DESCRIPTION: Navigate to the edp --> "TOTEPOOL" tab --> "PLACE" tab
        """
        event = self.get_uk_tote_event(uk_tote_place=True)
        self.__class__.eventID = event.event_id
        self.__class__.event_typename = event.event_typename.strip()
        self.__class__.bet_amount = '{0:.2f}'.format(event.min_total_stake)
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        self.site.login(async_close_dialogs=False)

        tab_content = self.site.racing_event_details.tab_content
        tab_opened = tab_content.event_markets_list.market_tabs_list.open_tab(
            vec.racing.RACING_EDP_MARKET_TABS.totepool)
        self.assertTrue(tab_opened, msg=f'"{vec.racing.RACING_EDP_MARKET_TABS.totepool}" tab is not opened')
        self.__class__.event_off_time = tab_content.event_off_times_list.selected_item
        sections = tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found')
        section_name, section = list(sections.items())[0]
        place_tab_opened = section.grouping_buttons.click_button(vec.uk_tote.UK_TOTE_TABS.place)
        self.assertTrue(place_tab_opened, msg=f'"{vec.uk_tote.UK_TOTE_TABS.place}" tab is not opened')

    def test_001_select_any_runners_press_place_button_and_tap_add_to_betslip_button_on_place_tote_bet_builder(self):
        """
        DESCRIPTION: Select any runners (press Place button) and tap "ADD TO BETSLIP" button on Place tote bet builder
        EXPECTED: * Tote Place bet is added to BetSlip
        EXPECTED: * Bet builder disappears
        EXPECTED: * Betslip is increased by 1 number indicator
        """
        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')

        section_name, section = list(sections.items())[0]
        outcomes = section.pool.items_as_ordered_dict
        self.assertTrue(all(outcomes), msg='No outcomes found')
        outcome_name, outcome = list(outcomes.items())[0]

        if outcome.runner_number:
            self.__class__.runner_info = '%s %s' % (outcome.runner_number, outcome_name)
        else:
            self.__class__.runner_info = '%s' % outcome_name
        cells = outcome.items
        self.assertTrue(cells, msg=f'No cells found for "{outcome_name}"')
        cell = cells[0]
        cell.click()
        self.assertTrue(cell.is_selected(timeout=2),
                        msg=f'Place cell is not selected for "{outcome_name}" runner')

        bet_builder = section.bet_builder
        self.assertTrue(bet_builder.is_displayed(timeout=3), msg='Bet builder is not shown')

        self.assertTrue(bet_builder.summary.add_to_betslip_button.is_enabled(timeout=3),
                        msg=f'"{vec.quickbet.BUTTONS.add_to_betslip}" button is not clickable')

        time.sleep(0.5)  # necessary spike in order to click "ADD TO BETSLIP" button

        bet_builder.summary.add_to_betslip_button.click()

        self.assertFalse(bet_builder.is_displayed(expected_result=False, timeout=3),
                         msg='Bet builder still shown on the screen')

        self.verify_betslip_counter_change(expected_value=1)

        self.site.open_betslip()
        self.__class__.singles_section = self.get_betslip_sections().Singles
        self.assertIn(f'{vec.uk_tote.PL} {vec.uk_tote.TOTEPOOL.title()}', self.singles_section, msg='Tote Place bet is not added to BetSlip')
        self.__class__.place_tote_stake = self.singles_section[f'{vec.uk_tote.PL} {vec.uk_tote.TOTEPOOL.title()}']

    def test_002_open_betslip_and_verify_the_place_tote_bet(self):
        """
        DESCRIPTION: Open BetSlip and verify the Place tote bet
        EXPECTED: * There is a "remove" button to remove the place tote bet from the betslip
        """
        self.assertTrue(self.place_tote_stake.has_event_name,
                        msg=f'"{self.place_tote_stake.name}" bet section is not expanded, event name is not shown')
        self.assertTrue(self.place_tote_stake.has_event_date,
                        msg=f'"{self.place_tote_stake.name}" bet section is not expanded, event date is not shown')

        self.assertTrue(self.place_tote_stake.remove_button.is_displayed(),
                        msg=f'"Remove" button is not available for "{self.place_tote_stake.name}" stake')

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
                         msg='Section title "%s" is not the same as expected "%s"' %
                             (self.singles_section.name, vec.betslip.BETSLIP_SINGLES_NAME))
        selections_count = self.get_betslip_content().selections_count

        self.assertEqual(
            selections_count,
            '1',
            msg='BetSlip counter in section name "%s" and counter "%s" doesn\'t match' %
                (selections_count, '1'))

        self.assertEqual(self.place_tote_stake.outcome_name, f'{vec.uk_tote.PL} {vec.uk_tote.TOTEPOOL.title()}',
                         msg='Actual outcome name "%s" is not the same as expected "%s"' %
                             (self.place_tote_stake.outcome_name, f'{vec.uk_tote.PL} {vec.uk_tote.TOTEPOOL.title()}'))

        self.assertEqual(self.place_tote_stake.market_name, vec.uk_tote.ONE_SELECTION_PLACE_BET,
                         msg='Actual bet type "%s" is not the same as expected "%s"' %
                             (self.place_tote_stake.market_name, vec.uk_tote.ONE_SELECTION_PLACE_BET))

        selection_outcomes = self.place_tote_stake.tote_outcomes.items_as_ordered_dict
        self.assertTrue(selection_outcomes, msg='No UK Tote selections found')
        self.assertEqual(list(selection_outcomes.keys())[0], self.runner_info,
                         msg='Selected runner "%s" is not the same as expected "%s"' %
                             (list(selection_outcomes.keys())[0], self.runner_info))

    def test_004_expand_the_bet_and_verify_the_start_date_and_time_of_the_race(self):
        """
        DESCRIPTION: Expand the bet and verify the start date and time of the race
        EXPECTED: * Time of the race is shown when the bet is expanded
        EXPECTED: * Format is the following:
        EXPECTED: HH:MM <event name>
        EXPECTED: <event start date>
        """
        expected_event_title = '%s %s' % (self.event_off_time, self.event_typename)
        self.assertEqual(self.place_tote_stake.event_name, expected_event_title,
                         msg='Actual event name "%s" is not the same as expected "%s"' %
                             (self.place_tote_stake.event_name, expected_event_title))
        self.assertEqual(self.place_tote_stake.event_date, 'Today',
                         msg='Actual event date: "%s" is not the same as expected: "Today"' %
                             self.place_tote_stake.event_date)

    def test_005_verify_stake_field(self):
        """
        DESCRIPTION: Verify "Stake" field
        EXPECTED: * User is able to set the stake using the BetSlip keyboard (mobile)
        EXPECTED: * User is able to modify stake
        EXPECTED: * "Total stake" value changes accordingly
        """
        self.enter_stake_amount(stake=(self.place_tote_stake.name, self.place_tote_stake))
        total_stake = self.get_betslip_content().total_stake
        self.assertEqual(total_stake, self.bet_amount,
                         msg='Actual total stake amount value "%s" is not the same as expected "%s"' %
                             (total_stake, self.bet_amount))

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
                         msg='Total Est. Returns: "%s" is not the same as expected: "N/A"' %
                             self.get_betslip_content().total_estimate_returns)

    def test_008_tap_the_remove_button(self):
        """
        DESCRIPTION: Tap the "remove" button
        EXPECTED: Bet is removed from the BetSlip
        """
        self.place_tote_stake.remove_button.click()
        if tests.settings.device_type == "mobile":
            result = self.site.has_betslip_opened(expected_result=False)
            self.assertFalse(result, msg='Betslip should not be displayed')
        else:
            result = wait_for_result(lambda: self.get_betslip_content().no_selections_title,
                                     name='Waiting for "No selections" message in Betslip',
                                     timeout=5)
            self.assertTrue(result, msg="'No selections' message is not shown")

    def test_009_place_bet_once_again(self):
        """
        DESCRIPTION: Place bet once again
        EXPECTED: * Place Tote bet is successfully placed
        EXPECTED: * Place Tote Bet receipt is shown
        """
        self.test_001_select_any_runners_press_place_button_and_tap_add_to_betslip_button_on_place_tote_bet_builder()
        self.test_005_verify_stake_field()
        self.get_betslip_content().bet_now_button.click()

        self.check_bet_receipt_is_displayed()
