import re
from datetime import datetime

import pytest

import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_012_UK_Tote.BaseUKTote import BaseUKTote


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod - we are NOT ALLOWED to Place a Tote bets on HL and PROD environments
# @pytest.mark.hl
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.uk_tote
@pytest.mark.open_bets
@pytest.mark.bet_placement
@pytest.mark.betslip
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.slow
@pytest.mark.timeout(700)
@pytest.mark.login
@vtest
class Test_C2321108_Verify_Quadpot_bet_is_displayed_on_Open_Bets_tab(BaseUKTote, BaseBetSlipTest):
    """
    TR_ID: C2321108
    VOL_ID: C12834344
    NAME: Verify Quadpot bet is displayed on Open Bets tab
    DESCRIPTION: This test case verifies the displayed contents of a Quadpot tote bet in the Settled Bets/Open Bets
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User has placed tote Quadpot Bet(s) on UK Tote events
    """
    keep_browser_open = True
    selection_outcomes = []
    selection_outcomes_uk_type_replaced = []
    selection_name = 'Quadpot Totepool'
    total_stake_label = 'TOTAL STAKE'
    expected_active_btn = 'POOLS'
    expected_market_name = 'Quadpot'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Select "Quadpot" sub-tab under "Tote" tab
        EXPECTED: "Quadpot" tab is selected
        EXPECTED: "Quadpot" racecard is opened
        EXPECTED: User is logged in
        """
        event = self.get_uk_tote_event(uk_tote_quadpot=True)
        self.__class__.eventID = event.event_id
        self.__class__.event_typename = event.event_typename.strip()
        self.__class__.uk_event_typename = event.uk_tote_typename
        self.__class__.bet_amount = event.min_total_stake
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        self.site.login()

        tab_opened = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(
            vec.racing.RACING_EDP_MARKET_TABS.totepool)
        self.assertTrue(tab_opened, msg=f'"{vec.uk_tote.TOTEPOOL}" tab is not opened')
        self.__class__.event_off_time = self.site.racing_event_details.tab_content.event_off_times_list.selected_item
        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        section_name, section = list(sections.items())[0]
        quadpot_opened = section.grouping_buttons.click_button(vec.uk_tote.UK_TOTE_TABS.quadpot)
        self.assertTrue(quadpot_opened, msg=f'"{vec.uk_tote.UK_TOTE_TABS.quadpot}" tab is not opened')
        self.__class__.pool = section.pool
        self.__class__.outcomes = list(self.pool.items_as_ordered_dict.items())
        self.assertTrue(self.outcomes, msg='No outcomes found')
        self.__class__.pool_legs = self.pool.grouping_buttons.items_as_ordered_dict
        self.assertTrue(self.pool_legs, f'Pool section: "{section_name}" not contains any leg')

    def test_001_select_at_least_one_selection_for_each_leg(self):
        """
        DESCRIPTION: Select at least one selection for each Leg
        EXPECTED: All selections are selected for each Leg
        EXPECTED: 'No. Lines' value is updated accordingly
        """
        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        section_name, self.__class__.section = list(sections.items())[0]

        for pool_leg_name, pool_leg in self.pool_legs.items():
            self.pool.grouping_buttons.click_button(button_name=pool_leg_name)
            outcomes = self.pool.items_as_ordered_dict
            self.assertTrue(outcomes, msg=f'No outcomes found for pool leg: "{pool_leg_name}"')
            outcome_name, outcome = list(outcomes.items())[0]
            outcome.select()
            self.assertTrue(self.section.bet_builder.summary.no_lines.value,
                            msg=f'"No. Lines" values is: "{self.section.bet_builder.summary.no_lines.value}"')
        self.__class__.bet_builder = self.section.bet_builder
        for pool_leg_name, pool_leg in self.pool_legs.items():
            pool_leg.scroll_to()
            self.assertTrue(pool_leg.is_filled(),
                            msg=f'Pool leg switch button: "{pool_leg_name}" not selected after adding selection')

    def test_002_enter_some_stake_amount_into_stake_per_line_input_field(self):
        """
        DESCRIPTION: Enter some stake amount into 'Stake per line' input field
        EXPECTED: '<currency symbol> <stake amount> TOTAL STAKE' button becomes clickable (enabled) on Tote Bet Builder
        EXPECTED: 'TOTAL STAKE' value is updated accordingly
        """
        self.bet_builder.summary.input.value = self.bet_amount
        self.assertTrue(self.bet_builder.summary.add_to_betslip_button.is_enabled(),
                        msg='"ADD TO SLIP" button is disabled')
        self.assertEqual(self.bet_builder.summary.add_to_betslip_button.label, self.total_stake_label)

    def test_003_add_to_slip_button(self):
        """
        DESCRIPTION: Tap "ADD TO SLIP" button
        EXPECTED: Tote Quadpot bets are added to betslip
        EXPECTED: Bet builder disappears
        """
        self.bet_builder.summary.add_to_betslip_button.click()
        self.assertFalse(self.section.bet_builder.is_displayed(expected_result=False),
                         msg='Bet builder not disappears')

    def test_004_open_betslip_and_verify_the_quadpot_tote_bet(self):
        """
        DESCRIPTION: Open betslip and verify the Quadpot tote bet
        EXPECTED: The bet section is collapsed by default
        EXPECTED: It is possible to expand the tote bet by clicking on the + button
        """
        self.site.open_betslip()
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section.items(), msg='*** No stakes found')

        stake_name, stake = list(singles_section.items())[0]
        self.assertTrue(stake.remove_button.is_displayed(), msg='Remove button was not found')
        self.__class__.stake = stake

    def test_005_verify_bet_details_for_quadpot_tote_bet(self):
        """
        DESCRIPTION: Verify bet details for Quadpot tote bet
        EXPECTED:  There are the following details on Quadpot tote bet:
        EXPECTED:  "Singles (1)" label in the section header
        EXPECTED:  "Quadpot Totepool"
        EXPECTED:  Number of lines
        EXPECTED:  Example:
        EXPECTED:    + Quadpot Totepool
        EXPECTED:    448 Lines
        """
        self.assertEqual(self.stake.outcome_name, self.selection_name,
                         msg=f'Actual outcome name "{self.stake.outcome_name}", expected "{self.selection_name}"')

        self.assertEqual(self.stake.market_name, vec.betslip.POT_BET_TITLE.format(number=1),
                         msg=f'Actual bet type "{self.stake.market_name}", '
                             f'expected "{vec.betslip.POT_BET_TITLE.format(number=1)}"')

    def test_006_verify_the_start_date_and_time_of_the_race(self):
        """
        DESCRIPTION: Verify the start date and time of the race
        EXPECTED: * Name of the each Leg is shown when the bet is expanded
        EXPECTED: * Name of selection for each Leg is shown when the bet is expanded
        EXPECTED:    Example:
        EXPECTED:        + Quadpot Totepool
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
        self.__class__.selection_outcomes = (list(selection_outcomes.keys()))

    def test_007_verify_stake_field(self):
        """
        DESCRIPTION: Verify "Stake" field
        EXPECTED: User is able to set the stake using the betslip keyboard (mobile)
        EXPECTED: "Total stake" value changes accordingly
        """
        self.enter_stake_amount(stake=(self.stake.name, self.stake))
        total_stake = self.get_betslip_content().total_stake
        self.__class__.expected_total_stake = '%.2f' % self.bet_amount
        self.assertEqual(total_stake, self.expected_total_stake,
                         msg=f'Actual total stake value "{total_stake}" '
                         f'is not equal expected "{self.expected_total_stake}"')
        self.assertEqual(self.stake.est_returns, 'N/A',
                         msg=f'Est returns is "{self.stake.est_returns}" not "N/A"')
        self.assertEqual(self.get_betslip_content().total_estimate_returns, 'N/A',
                         msg=f'Total Est. Returns is "{self.get_betslip_content().total_estimate_returns}" '
                         'not "N/A"')

        self.get_betslip_content().bet_now_button.click()
        self.check_bet_receipt_is_displayed()

        self.__class__.now_date = self.get_local_time_for_uk_tote(hours=1)

        receipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(receipt_sections, msg='No receipt sections found in BetReceipt')
        single_section = receipt_sections.get(vec.betslip.BETSLIP_SINGLES_NAME)
        self.assertTrue(single_section, msg=f'"{vec.betslip.BETSLIP_SINGLES_NAME}" section was not found')
        singles = single_section.items_as_ordered_dict
        self.assertTrue(singles, msg='No Single sections found')
        name = f'{vec.uk_tote.UQDP} {vec.uk_tote.TOTEPOOL.title()}'
        single = singles.get(name)
        self.assertTrue(single, msg=f'"{name}" not found in {list(singles.keys())}')
        self.__class__.outcome_bet_receipt_bet_id = single.bet_id

        self.site.bet_receipt.close_button.click()

    def test_008_navigate_to_open_bets_tab(self):
        """
        DESCRIPTION: Navigate to Open Bets tab
        """
        self.site.open_my_bets_open_bets()

    def test_009_tap_on_the_pools_sub_section(self):
        """
        DESCRIPTION: Tap on the Pools sub-section
        EXPECTED: All UK tote bets are displayed by default in List view
        EXPECTED: Quadpot tote bet information corresponds to placed bet:
        EXPECTED: * Selection Name(s) and places
        EXPECTED: * "Quadpot" text
        EXPECTED: * Race number (e.g. Race 3)
        EXPECTED: * Race Name (e.g 15:25 Wincanton (WI))
        EXPECTED: * Date of bet placement in a format MM/DD/YYYY (e.g. 10/19/2018)
        EXPECTED: * Bet Receipt id (e.g. P/0156602/0000117)
        EXPECTED: * Stake value (e.g. £2.00)
        EXPECTED: * Estimated returns value is N/A
        """
        self.site.open_bets.tab_content.grouping_buttons.click_button(vec.bet_history.POOLS_TAB_NAME)
        active_btn = self.site.open_bets.tab_content.grouping_buttons.current
        self.assertEqual(active_btn, self.expected_active_btn,
                         msg=f'"{self.expected_active_btn}" sorting type is not selected')
        sections = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='Can not find any section')

        # removing colons ":" 'Leg 1: 18:00' => 'Leg 1 18:00'
        # BMA-35778
        new_selection_outcomes = list(map(lambda x: re.sub(r"(\d)+(:) ", lambda str: str.group(1) + " ", x),
                                          self.selection_outcomes))

        # replacing to uk_event_type_name 'Fakenham' => 'Fakenham (FA)'
        self.__class__.updated_event_names = list(map(lambda str: str.replace(self.event_typename,
                                                                              self.uk_event_typename),
                                                      new_selection_outcomes))

        bet_name, self.__class__.tote_pool = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type='TOTEPOOL', event_names=self.updated_event_names, number_of_bets=1)

        bet_date = self.tote_pool.bet_receipt_info.date.text
        self.assertTrue(bet_date, msg='Bet date was not found')
        time_diff = self.now_date - datetime.strptime(bet_date, self.time_format_pattern)
        self.assertTrue(time_diff.seconds < 61,
                        msg=f'Date of bet placement does not correspond to placed bet. '
                            f'Difference between times is {time_diff.seconds} seconds, '
                        f'bet date is "{bet_date}" but current date is "{self.now_date}"')

        n_a_msg = 'N/A'
        self.assertEqual(self.tote_pool.est_returns.value, n_a_msg,
                         msg=f'Estimated returns: "{self.tote_pool.est_returns.value}" does not match with required: "{n_a_msg}"')

        self.assertEqual(self.tote_pool.stake.stake_value, '{0:.2f}'.format(self.bet_amount),
                         msg=f'Total Stake amount "{self.tote_pool.stake.value}" is not equal to expected '
                         f'"{self.total_stake}" for bet "{self.tote_pool.name}"')

        self.assertEqual(self.tote_pool.bet_receipt_info.bet_receipt.value, self.outcome_bet_receipt_bet_id,
                         msg=f'Open Bet section: "{self.tote_pool.name}" bet receipt ID '
                         f'"{self.outcome_bet_receipt_bet_id}" not found')
