import pytest
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_012_UK_Tote.BaseUKTote import BaseUKTote
import voltron.environments.constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod - we are NOT ALLOWED to Place a Tote bets on HL and PROD environments
# @pytest.mark.hl
@pytest.mark.uk_tote
@pytest.mark.horseracing
@pytest.mark.critical
@pytest.mark.desktop
@pytest.mark.races
@pytest.mark.login
@vtest
class Test_C1743725_Verify_UK_Tote_Placepot_Bet_Placement(BaseUKTote, BaseBetSlipTest):
    """
    TR_ID: C1743725
    NAME: Verify UK Tote Placepot Bet Placement
    """
    keep_browser_open = True
    pool_type = vec.betslip.POT_BET_TITLE.format(number=1)
    selection_outcomes = []
    currency = '£'
    total_stake_label = 'TOTAL STAKE'

    def test_001_select_placepot_sub_tab_under_tote_tab(self):
        """
        DESCRIPTION: Select "Placepot" sub-tab under "Tote" tab
        EXPECTED: "Placepot" tab is selected
        EXPECTED: "Placepot" racecard is opened
        """
        event = self.get_uk_tote_event(uk_tote_placepot=True)
        self.__class__.eventID = event.event_id
        self.__class__.event_typename = event.event_typename.strip()
        self.__class__.bet_amount = '{0:.2f}'.format(event.min_total_stake)
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        self.site.login(async_close_dialogs=False)

        tab_opened = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(
            vec.racing.RACING_EDP_MARKET_TABS.totepool)
        self.assertTrue(tab_opened, msg='"%s" tab is not opened' % vec.racing.RACING_EDP_MARKET_TABS.totepool)
        self.__class__.event_off_time = self.site.racing_event_details.tab_content.event_off_times_list.selected_item
        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        section_name, section = list(sections.items())[0]
        placepot_opened = section.grouping_buttons.click_button(vec.uk_tote.UK_TOTE_TABS.placepot)
        self.assertTrue(placepot_opened, msg='"%s" tab is not opened' % vec.uk_tote.UK_TOTE_TABS.placepot)

    def test_002_select_at_least_one_selection_for_each_leg(self):
        """
        DESCRIPTION: Select at least one selection for each Leg
        EXPECTED: All selections are selected for each Leg
        EXPECTED: 'No. Lines' value is updated accordingly
        """
        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')

        section_name, self.__class__.section = list(sections.items())[0]
        self.__class__.pool = self.section.pool
        self.__class__.outcomes = list(self.pool.items_as_ordered_dict.items())
        self.assertTrue(self.outcomes, msg='No outcomes found')
        self.__class__.pool_legs = self.pool.grouping_buttons.items_as_ordered_dict
        self.assertTrue(self.__class__.pool_legs, 'Pool section: "%s" not contains any leg' % section_name)

        for pool_leg_name, pool_leg in self.pool_legs.items():
            self.pool.grouping_buttons.click_button(button_name=pool_leg_name)
            outcomes = self.pool.items_as_ordered_dict
            self.assertTrue(outcomes, msg='No outcomes found for pool leg: "%s"' % pool_leg_name)
            outcome_name, outcome = list(outcomes.items())[0]
            if outcome.runner_number:
                selection_name = '%s: %s - %s. %s' % (pool_leg_name.title(), self.pool.race_title,
                                                      outcome.runner_number, outcome_name)
            else:
                # there is no runner number for 'Unnamed Favourite'
                selection_name = '%s: %s - %s' % (pool_leg_name.title(), self.pool.race_title, outcome_name)
            self.__class__.selection_outcomes.append(selection_name)
            outcome.select()
            self.assertTrue(self.section.bet_builder.summary.no_lines.value,
                            msg='"No. Lines" values is: "%s"' % self.section.bet_builder.summary.no_lines.value)
        self.__class__.bet_builder = self.section.bet_builder
        for pool_leg_name, pool_leg in self.pool_legs.items():
            pool_leg.scroll_to()
            self.assertTrue(pool_leg.is_filled(),
                            msg='Pool leg switch button: "%s" not selected after adding selection' % pool_leg_name)

    def test_003_enter_some_stake_amount_into_stake_per_line_input_field(self):
        """
        DESCRIPTION: Enter some stake amount into 'Stake per line' input field
        EXPECTED: Stake amount is shown in the 'Stake per line' input field
        EXPECTED: Stake amount is shown in format <currency symbol> <stake amount value>
        EXPECTED: '<currency symbol> <stake amount> TOTAL STAKE' button becomes clickable (enabled) on Tote Bet Builder
        EXPECTED: 'TOTAL STAKE' value is updated accordingly
        """
        self.bet_builder.summary.input.value = self.bet_amount
        actual_amount = self.bet_builder.summary.input.value
        self.assertEqual(actual_amount, self.bet_amount,
                         msg='Actual input field value: "%s", expected: "%s"'
                             % (actual_amount, self.bet_amount))
        self.assertTrue(self.bet_builder.summary.add_to_betslip_button.is_enabled(),
                        msg='"ADD TO SLIP" button is disabled')
        self.assertEqual(self.bet_builder.summary.add_to_betslip_button.label, self.total_stake_label)
        expected_value = '{0}{1}'.format(self.currency, self.bet_amount)
        self.assertEqual(self.bet_builder.summary.add_to_betslip_button.value, expected_value,
                         msg='Actual total stake value: "%s", expected: "%s"'
                             % (self.bet_builder.summary.add_to_betslip_button.value, expected_value))

    def test_004_add_to_slip_button(self):
        """
        DESCRIPTION: Tap "ADD TO SLIP" button
        EXPECTED: Tote Placepot bets are added to betslip
        EXPECTED: Bet builder disappears
        """
        self.bet_builder.summary.add_to_betslip_button.click()
        self.__class__.betslip_counter = self.site.header.bet_slip_counter.counter_value
        self.assertFalse(self.section.bet_builder.is_displayed(expected_result=False),
                         msg='Bet builder not disappears')

    def test_005_open_betslip_and_verify_the_placepot_tote_bet(self):
        """
        DESCRIPTION: Open betslip and verify the Placepot tote bet
        EXPECTED: The bet section is collapsed by default
        EXPECTED: It is possible to expand the tote bet by clicking on the + button
        EXPECTED: There is a "remove" button to remove the Placepot tote bet from the betslip
        """
        self.site.open_betslip()
        singles_section = self.get_betslip_sections().Singles

        selections_count = self.get_betslip_content().selections_count

        self.assertEqual(
            selections_count,
            self.betslip_counter,
            msg='BetSlip counter in section name "%s" and counter "%s" doesn\'t match' %
                (selections_count, self.betslip_counter))
        stake_name, stake = list(singles_section.items())[0]
        self.assertTrue(stake.remove_button.is_displayed(), msg='Remove button was not found')
        self.__class__.stake = stake

    def test_006_verify_bet_details_for_placepot_tote_bet(self):
        """
        DESCRIPTION: Verify bet details for Placepot tote bet
        EXPECTED:  There are the following details on Placepot tote bet:
        EXPECTED:  "Singles (1)" label in the section header
        EXPECTED:  "Placepot Totepool"
        EXPECTED:  Number of lines
        EXPECTED:  Example:
        EXPECTED:    + Placepot Totepool
        EXPECTED:    448 Lines
        """
        self.assertEqual(self.stake.outcome_name, f'{vec.uk_tote.UPLP} {vec.uk_tote.TOTEPOOL.title()}',
                         msg='Actual outcome name "%s", expected "%s"' %
                             (self.stake.outcome_name, f'{vec.uk_tote.UPLP} {vec.uk_tote.TOTEPOOL.title()}'))
        self.assertEqual(self.stake.market_name, self.pool_type,
                         msg='Actual bet type "%s", expected "%s"' %
                             (self.stake.market_name, self.pool_type))

    def test_007_verify_the_start_date_and_time_of_the_race(self):
        """
        DESCRIPTION: Verify the start date and time of the race
        EXPECTED: * Name of the each Leg is shown when the bet is expanded
        EXPECTED: * Name of selection for each Leg is shown when the bet is expanded
        EXPECTED:    Example:
        EXPECTED:        + Placepot Totepool
        EXPECTED:        448 Lines
        EXPECTED:         Leg1: 1mHCap
        EXPECTED:            1. Dr Julius No
        EXPECTED:         Leg2: 6f HCap
        EXPECTED:            1. Rivas Rob Roy
        EXPECTED:            2. Queen of Kalahari
        EXPECTED:     etc.
        """
        selection_outcomes = self.stake.multiple_tote_outcomes.items_as_ordered_dict
        self.assertTrue(selection_outcomes, msg='No UK Tote selections found')
        self.assertEqual(list(selection_outcomes.keys()), self.selection_outcomes)

    def test_008_verify_stake_field(self):
        """
        DESCRIPTION: Verify "Stake" field
        EXPECTED: User is able to set the stake using the betslip keyboard (mobile)
        EXPECTED: User is able to modify stake
        EXPECTED: "Total stake" value changes accordingly
        """
        self.enter_stake_amount(stake=(self.stake.name, self.stake))
        total_stake = self.get_betslip_content().total_stake
        expected_total_stake = self.bet_amount
        self.assertEqual(total_stake, expected_total_stake,
                         msg='Actual total stake value "%s" is not equal expected "%s"'
                             % (total_stake, expected_total_stake))

    def test_009_verify_odds_and_estimated_returns(self):
        """
        DESCRIPTION: Verify "Odds" and "Estimated Returns"
        EXPECTED: Odds and Estimated Returns values are "N/A" for Tote bets
        """
        est_returns = self.stake.est_returns
        self.assertEqual(est_returns, 'N/A',
                         msg=f'Est returns is "{est_returns}" not "N/A"')

    def test_010_verify_total_est_returns(self):
        """
        DESCRIPTION: Verify "Total Est. Returns"
        EXPECTED: Total Est. Returns value is "N/A"
        """
        total_estimate_returns = self.get_betslip_content().total_estimate_returns
        self.assertEqual(total_estimate_returns, 'N/A',
                         msg=f'Total Est returns is "{total_estimate_returns}" not "N/A"')

    def test_011_tap_the_bet_now_button(self):
        """
        DESCRIPTION: Tap the "Bet Now" button
        EXPECTED: Trifecta Tote bet is successfully placed
        EXPECTED: Trifecta Tote Bet receipt is shown
        """
        self.get_betslip_content().bet_now_button.click()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.click_done()

    def test_012_repeat_step_2_5_tap_on_remove_button(self):
        """
        DESCRIPTION: Repeat Step 2-5, tap on remove button
        EXPECTED: Betslip is cleared
        """
        self.test_002_select_at_least_one_selection_for_each_leg()
        self.test_003_enter_some_stake_amount_into_stake_per_line_input_field()
        self.test_004_add_to_slip_button()
        self.test_005_open_betslip_and_verify_the_placepot_tote_bet()
        self.stake.remove_button.click()

        self.verify_betslip_counter_change(expected_value=0)
