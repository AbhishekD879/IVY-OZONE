from datetime import datetime

import voltron.environments.constants as vec
import pytest
import re
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_012_UK_Tote.BaseUKTote import BaseUKTote


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod - we are NOT ALLOWED to Place a Tote bets on HL and PROD environments
# @pytest.mark.hl
@pytest.mark.uk_tote
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.high
@pytest.mark.bet_placement
@pytest.mark.bet_receipt
@pytest.mark.open_bets
@pytest.mark.desktop
@pytest.mark.login
@vtest
class Test_C2554306_Verify_Exacta_bet_is_displayed_on_Open_Bets_tab(BaseUKTote, BaseBetSlipTest):
    """
    TR_ID: C2554306
    NAME: Verify Exacta bet is displayed on Open Bets tab
    DESCRIPTION: This test case verifies the displayed contents of a Exacta tote bet in the Settled Bets/Open Bets
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User has placed tote Exacta Bet(s) on UK Tote events
    """
    keep_browser_open = True
    selection_outcomes = []
    expected_active_btn = vec.bet_history.POOLS_TAB_NAME
    expected_market_name = 'Tote Exacta Pool'

    def verify_exacta_bet_details(self, bet_name):
        """
        This method verifies exacta bet details
        :param bet_name: example "1. Dr Julius No**, 2. Newberry"
        """
        betlegs = self.tote_pool.items_as_ordered_dict
        self.assertTrue(betlegs, msg='No betlegs found for "%s"' % bet_name)

        betleg_name, betleg = list(betlegs.items())[0]
        outcome_names = [name.replace('.', '') for name in betleg.outcome_names]
        self.assertEqual(outcome_names, self.selection_outcomes,
                         msg=f'Outcome names "{outcome_names}" is not equal to expected "{self.selection_outcomes}')

        self.assertEqual(betleg.market_name, self.expected_market_name,
                         msg=f'Market name "{betleg.market_name}" is not equal '
                             f'to expected "{self.expected_market_name}"')

        bet_date = self.tote_pool.bet_receipt_info.date.text
        self.assertTrue(bet_date, msg='Bet date was not found')
        time_diff = self.now_date - datetime.strptime(bet_date, self.time_format_pattern)
        self.assertTrue(time_diff.seconds < 61,
                        msg=f'Date of bet placement does not correspond to placed bet. '
                            f'Difference between times is {time_diff.seconds} seconds, '
                            f'bet date is "{bet_date}" but current date is "{self.now_date}"')

        race_number = betleg.race_number
        self.assertTrue(re.match(r'Race.\d', race_number), 'Race expression is not correct')

        self.assertEqual(self.tote_pool.est_returns.value, 'N/A',
                         msg=f'Estimated returns: "{self.tote_pool.est_returns.value}" '
                             f'does not match with required: "N/A"')

        self.assertEqual(self.tote_pool.stake.stake_value, '{0:.2f}'.format(self.bet_amount),
                         msg=f'Total Stake amount "{self.tote_pool.stake.stake_value}" is not equal to '
                             f'expected: "{self.bet_amount}" for bet "{self.tote_pool.name}"')

        self.assertEqual(self.tote_pool.bet_receipt_info.bet_receipt.value, self.outcome_bet_receipt_bet_id,
                         msg=f'Bet receipt id: "{self.tote_pool.bet_receipt_info.bet_receipt.value}" is not equal to '
                             f'expected: "{self.outcome_bet_receipt_bet_id}"')

    def test_001_select_exacta_sub_tab_under_tote_tab(self):
        """
        DESCRIPTION: Select "Exacta" sub-tab under "Tote" tab
        EXPECTED: Exacta tab is selected
        EXPECTED: Exacta racecard is opened
        """
        event = self.get_uk_tote_event(uk_tote_exacta=True)
        self.__class__.eventID = event.event_id
        self.__class__.event_typename = event.event_typename.strip()
        self.__class__.uk_event_typename = event.uk_tote_typename
        self.__class__.bet_amount = event.min_total_stake
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        self.site.login()

        tab_opened = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(
            vec.racing.RACING_EDP_MARKET_TABS.totepool)
        self.assertTrue(tab_opened, msg='UK Tote tab is not opened')
        self.__class__.event_off_time = self.site.racing_event_details.tab_content.event_off_times_list.selected_item
        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        section_name, section = list(sections.items())[0]
        exacta_opened = section.grouping_buttons.click_button(vec.uk_tote.UK_TOTE_TABS.exacta)
        self.assertTrue(exacta_opened, msg='Exacta tab is not opened')
        self.__class__.outcomes = list(section.pool.items_as_ordered_dict.items())
        self.assertTrue(self.outcomes, msg='No outcomes found')

    def test_002_select_1st_and_2nd_check_boxes_for_any_runners(self):
        """
        DESCRIPTION: Select "1st" and "2nd" check boxes for any runners
        EXPECTED: Selections are added to the Exacta tote bet builder
        EXPECTED: "ADD TO BETSLIP" button becomes enabled in the bet builder
        EXPECTED: Corresponding bet type name is shown in the bet builder
        """
        for index, (outcome_name, outcome) in enumerate(self.outcomes[:2]):
            self.__class__.selection_outcomes.append(f'{index + 1} {outcome_name}')
            checkboxes = outcome.items_as_ordered_dict
            self.assertTrue(checkboxes, msg=f'No checkboxes found for "{outcome_name}"')
            checkbox_name, checkbox = list(checkboxes.items())[index]
            checkbox.click()
            self.assertTrue(checkbox.is_selected(),
                            msg=f'Checkbox "{checkbox_name}" is not selected for "{outcome_name}" after click')

        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        section_name, section = list(sections.items())[0]
        self.__class__.bet_builder = section.bet_builder
        self.assertTrue(self.bet_builder.summary.add_to_betslip_button.is_enabled(),
                        msg='ADD TO BETSLIP button is not enabled')

    def test_003_tap_add_to_betslip_button(self):
        """
        DESCRIPTION: Tap "ADD TO BETSLIP" button
        EXPECTED: Tote exacta bets are added to betslip
        EXPECTED: Bet builder disappears
        """
        self.bet_builder.summary.add_to_betslip_button.click()

    def test_004_open_betslip_and_verify_the_exacta_tote_bet(self):
        """
        DESCRIPTION: Open betslip and verify the exacta tote bet
        EXPECTED: The bet section is collapsed by default
        EXPECTED: It is possible to expand the tote bet by clicking on the **+** button
        EXPECTED: There is a "remove" button to remove the exacta tote bet from the betslip
        """
        self.site.open_betslip()
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section.items(), msg='*** No stakes found')

        stake_name, stake = list(singles_section.items())[0]
        self.assertTrue(stake.remove_button.is_displayed(), msg='Remove button was not found')

        self.__class__.stake = stake

    def test_005_verify_bet_details_for_exacta_tote_bet(self):
        """
        DESCRIPTION: Verify bet details for exacta tote bet
        EXPECTED: There are the following details on exacta tote bet:
        EXPECTED: "Singles (1)" label in the section header
        EXPECTED: "Exacta Totepool"
        EXPECTED: "Exacta" bet type name
        EXPECTED: Both selections with correct order according to the selected check boxes
        EXPECTED: Example:
        EXPECTED: + **Exacta Totepool**
        EXPECTED: Exacta
        EXPECTED: **1. Dr Julius No**
        EXPECTED: **2. Newberry New**
        """
        self.assertEqual(self.stake.market_name, vec.uk_tote.STRAIGHT_EXACTA_BET,
                         msg=f'Actual bet type "{self.stake.market_name}", expected "{vec.uk_tote.STRAIGHT_EXACTA_BET}"')
        selection_outcomes = self.stake.tote_outcomes.items_as_ordered_dict
        self.assertTrue(selection_outcomes, msg='No UK Tote selections found')
        self.assertEqual(list(selection_outcomes.keys()), self.selection_outcomes)

    def test_006_expand_the_bet_and_verify_the_start_date_and_time_of_the_race(self):
        """
        DESCRIPTION: Expand the bet and verify the start date and time of the race
        EXPECTED: * Time of the race is shown when the bet is expanded
        EXPECTED: * Format is the following:
        EXPECTED: HH:MM <event name>
        EXPECTED: <event start date>
        EXPECTED: Example:
        EXPECTED: 14:20 Lingfield
        EXPECTED: Today
        """
        expected_event_title = f'{self.event_off_time} {self.event_typename}'
        self.assertEqual(self.stake.event_name, expected_event_title,
                         msg=f'Actual event title "{self.stake.event_name}", expected "{expected_event_title}"')
        self.assertEqual(self.stake.event_date, 'Today',
                         msg=f'Actual event date "{self.stake.event_date}", expected "Today"')

        self.enter_stake_amount(stake=(self.stake.name, self.stake))
        self.assertEqual(self.get_betslip_content().total_estimate_returns, 'N/A',
                         msg=f'Total Est. Returns is "{self.get_betslip_content().total_estimate_returns}" not "N/A"')
        self.get_betslip_content().bet_now_button.click()
        self.check_bet_receipt_is_displayed()

        self.__class__.now_date = self.get_local_time_for_uk_tote(hours=1)

        receipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(receipt_sections, msg='No receipt sections found in BetReceipt')
        single_section = receipt_sections.get(vec.betslip.BETSLIP_SINGLES_NAME)

        self.assertTrue(single_section, msg=f'"{vec.betslip.BETSLIP_SINGLES_NAME}" section was not found')
        singles = single_section.items_as_ordered_dict
        self.assertTrue(singles, msg='No Single sections found')
        name = f'{vec.uk_tote.UEXA} {vec.uk_tote.TOTEPOOL.title()}'
        single = singles.get(name)
        self.assertTrue(single, msg=f'"{name}" not found in {list(singles.keys())}')

        self.__class__.outcome_bet_receipt_bet_id = single.bet_id
        self.site.bet_receipt.close_button.click()

    def test_007_navigate_to_open_bets_tab(self):
        """
        DESCRIPTION: Navigate to Open Bets tab
        """
        self.site.open_my_bets_open_bets()

    def test_008_tap_on_the_pools_sub_section(self):
        """
        DESCRIPTION: Tap on the Pools sub-section
        EXPECTED: All UK tote bets are displayed by default in List view
        EXPECTED: Exacta tote bet information corresponds to placed bet:
        EXPECTED: *  Selection Name(s) and places
        EXPECTED: *  "Tote Exacta Pool" text
        EXPECTED: *  Race number (e.g. Race 3)
        EXPECTED: *  Race Name (e.g 15:25 Wincanton (WI))
        EXPECTED: *  Date of bet placement in a format MM/DD/YYYY (e.g. 10/19/2018)
        EXPECTED: *  Bet Receipt id (e.g. P/0156602/0000117)
        EXPECTED: *  Stake value (e.g. £2.00)
        EXPECTED: *  Estimated returns value is N/A (exact value in case bet is settled as Won)
        """
        self.site.open_bets.tab_content.grouping_buttons.click_button(vec.bet_history.POOLS_TAB_NAME)
        active_btn = self.site.open_bets.tab_content.grouping_buttons.current
        self.assertEqual(active_btn, self.expected_active_btn,
                         msg=f'"{self.expected_active_btn}" sorting type is not selected')
        sections = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='Can not find any section')

        expected_event = f'{self.event_off_time} {self.uk_event_typename}'
        bet_name, self.__class__.tote_pool = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type='SINGLE', event_names=expected_event, number_of_bets=1)

        self.verify_exacta_bet_details(bet_name)
