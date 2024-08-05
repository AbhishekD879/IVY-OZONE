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
@pytest.mark.uk_tote
@pytest.mark.high
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.desktop
@pytest.mark.bet_placement
@pytest.mark.bet_receipt
@pytest.mark.open_bets
@pytest.mark.login
@vtest
class Test_C2554308_Verify_Trifecta_Bet_is_Displayed_On_Open_Bets_tab(BaseUKTote, BaseBetSlipTest):
    """
    TR_ID: C2554308
    NAME: Verify Trifecta bet is displayed on Open Bets tab
    DESCRIPTION: This test case verifies the displayed contents of a Trifecta tote bet in the Settled Bets/Open Bets
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User has placed tote Trifecta Bet(s) on UK Tote events
    """
    keep_browser_open = True
    selection_outcomes = []

    def verify_trifecta_tote_bet_information(self, obj):
        pools_opened = obj.tab_content.grouping_buttons.click_button(vec.bet_history.POOLS_TAB_NAME)
        self.assertTrue(pools_opened, msg='Pools tab is not opened')

        bet_name, self.__class__.single_bet = obj.tab_content.accordions_list.get_bet(
            bet_type='SINGLE', event_names=self.uk_event_typename, number_of_bets=1)

        bet_legs = self.single_bet.items_as_ordered_dict
        self.assertTrue(bet_legs, msg=f'No one bet leg was found for bet: "{bet_name}"')

        betleg_name, betleg = list(bet_legs.items())[0]
        selection_names = [item.replace('.', '') for item in betleg.outcome_names]
        self.assertTrue(len(selection_names) != 0, msg='Selection Names are not present')

        self.assertEqual(self.selection_outcomes, selection_names,
                         msg=f'Selection Name(s) and places do not correspond to placed bet. '
                             f'Expected: "{self.selection_outcomes}". Actual: {selection_names}')

        market_name = betleg.market_name
        actual_split = market_name.split(' ')
        for trifecta_word in actual_split:
            self.assertTrue(re.search(trifecta_word, self.selection_name, re.IGNORECASE),
                            msg=f"Names are not equal {self.selection_name} : {market_name}")

        race_number = betleg.race_number
        self.assertTrue(re.match(r'Race.\d', race_number), 'Race expression is not correct')

        bet_date = self.single_bet.bet_receipt_info.date.text
        self.assertTrue(bet_date, msg='Bet date was not found')
        time_diff = self.now_date - datetime.strptime(bet_date, self.time_format_pattern)
        self.assertTrue(time_diff.seconds < 61,
                        msg=f'Date of bet placement does not correspond to placed bet. '
                            f'Difference between times is {time_diff.seconds} seconds, '
                            f'bet date is "{bet_date}" but current date is "{self.now_date}"')

        actual_bet_id = self.single_bet.bet_receipt_info.bet_receipt.value
        self.assertEqual(self.bet_id, actual_bet_id,
                         msg=f'Bet Receipt id does not correspond to placed bet. '
                             f'Expected: "{self.bet_id}". Actual: {actual_bet_id}')
        stake_value = self.single_bet.stake.stake_value
        self.assertEqual('{0:.2f}'.format(self.bet_amount), stake_value,
                         msg=f'Stake value does not correspond to placed bet. '
                             f'Expected: "{self.bet_amount}". Actual: {stake_value}')
        est_value = self.single_bet.est_returns.stake_value
        self.assertEqual(self.event_NA, est_value,
                         msg=f'Est returns is "{est_value}" not "N/A"')

    def test_001_select_trifecta_sub_tab_under_tote_tab(self):
        """
        DESCRIPTION: Select "Trifecta" sub-tab under "Tote" tab
        EXPECTED: "Trifecta" tab is selected
        EXPECTED: "Trifecta" racecard is opened
        """
        event = self.get_uk_tote_event(uk_tote_trifecta=True)
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
        self._logger.info(f'*** Event off time {self.event_off_time}')
        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        section_name, self.__class__.section = list(sections.items())[0]
        trifecta_opened = self.section.grouping_buttons.click_button(vec.uk_tote.UK_TOTE_TABS.trifecta)
        self.assertTrue(trifecta_opened, msg=f'"{vec.uk_tote.UK_TOTE_TABS.trifecta}" tab is not opened')
        self.__class__.outcomes = list(self.section.pool.items_as_ordered_dict.items())
        self.assertTrue(self.outcomes, msg='No outcomes found')

    def test_002_select_1st_and_2nd_and_3rd_check_boxes_for_any_runners(self):
        """
        DESCRIPTION: Select "1st", "2nd" and "3rd" check boxes for any runners
        EXPECTED: Selections are added to the Trifecta tote bet builder
        EXPECTED: "ADD TO BETSLIP" button becomes enabled in the bet builder
        EXPECTED: Corresponding bet type name is shown in the bet builder
        """
        for index, (outcome_name, outcome) in enumerate(self.outcomes[:3]):
            self.__class__.selection_outcomes.append(f'{index + 1} {outcome_name}')
            checkboxes = outcome.items_as_ordered_dict
            self.assertTrue(checkboxes, msg=f'No checkboxes found for "{outcome_name}"')
            checkbox_name, checkbox = list(checkboxes.items())[index]
            checkbox.click()
            self.assertTrue(checkbox.is_selected(),
                            msg=f'Checkbox "{checkbox_name}" is not selected for "{outcome_name}" after click')
        self.__class__.bet_builder = self.section.bet_builder
        self.assertTrue(self.bet_builder.summary.add_to_betslip_button.is_enabled(),
                        msg='ADD TO BETSLIP button is not enabled')

    def test_003_tap_add_to_betslip_button(self):
        """
        DESCRIPTION: Tap "ADD TO BETSLIP" button
        EXPECTED: Tote Trifecta bets are added to betslip
        EXPECTED: Bet builder disappears
        """
        self.bet_builder.summary.add_to_betslip_button.click()
        self.assertFalse(self.section.bet_builder.is_displayed(expected_result=False),
                         msg='Bet builder not disappears')

    def test_004_open_betslip_and_verify_the_trifecta_tote_bet(self):
        """
        DESCRIPTION: Open betslip and verify the Trifecta tote bet
        EXPECTED: The bet section is collapsed by default
        EXPECTED: It is possible to expand the tote bet by clicking on the **+** button
        EXPECTED: There is a "remove" button to remove the trifecta tote bet from the betslip
        """
        self.site.open_betslip()
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section.items(), msg='*** No stakes found')
        self.__class__.selection_name = singles_section.keys()[0]

        stake_name, stake = list(singles_section.items())[0]
        self.__class__.event_NA = stake.est_returns
        self.assertTrue(stake.remove_button.is_displayed(),
                        msg=f'Remove button was not found for stake: "{stake_name}"')
        self.__class__.stake = stake

    def test_005_verify_stake_field(self):
        """
        DESCRIPTION: Verify "Stake" field
        EXPECTED: User is able to set the stake using the betslip keyboard (mobile)
        EXPECTED: User is able to modify stake
        EXPECTED: "Total stake" value changes accordingly
        """
        self.enter_stake_amount(stake=(self.stake.name, self.stake))
        self.__class__.total_stake = self.get_betslip_content().total_stake
        expected_total_stake = '%.2f' % self.bet_amount
        self.assertEqual(self.total_stake, expected_total_stake,
                         msg=f'Actual total stake value "{self.total_stake}" is not equal '
                         f'expected "{expected_total_stake}"')

    def test_006_tap_the_bet_now_button(self):
        """
        DESCRIPTION: Tap the "Bet Now" button
        EXPECTED: Trifecta Tote bet is successfully placed
        EXPECTED: Trifecta Tote Bet receipt is shown
        """
        self.get_betslip_content().bet_now_button.click()
        self.check_bet_receipt_is_displayed()

        self.__class__.now_date = self.get_local_time_for_uk_tote(hours=1)

        receipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(receipt_sections, msg='No receipt sections found in BetReceipt')
        single_section = receipt_sections.get(vec.betslip.BETSLIP_SINGLES_NAME)

        self.assertTrue(single_section, msg=f'"{vec.betslip.BETSLIP_SINGLES_NAME}" section was not found')
        singles = single_section.items_as_ordered_dict
        self.assertTrue(singles, msg='No Single sections found')
        name = f'{vec.uk_tote.UTRI} {vec.uk_tote.TOTEPOOL.title()}'
        single = singles.get(name)
        self.assertTrue(single, msg=f'"{name}" not found in {list(singles.keys())}')

        self.__class__.bet_id = single.bet_id
        self.assertTrue(self.bet_id, msg='Bet id is not found on Bet Receipt')
        self.site.bet_receipt.footer.click_done()

    def test_007_navigate_to_open_bets_tab(self):
        """
        DESCRIPTION: Navigate to Open Bets tab
        EXPECTED: 'Open Bets' tab is opened
        """
        self.site.open_my_bets_open_bets()

    def test_008_tap_on_the_pools_sub_section(self):
        """
        DESCRIPTION: Tap on the Pools sub-section
        EXPECTED: All UK tote bets are displayed by default in List view
        EXPECTED: Trifecta tote bet information corresponds to placed bet:
        EXPECTED: *  Selection Name(s) and places
        EXPECTED: *  "Tote Trifecta Pool" text
        EXPECTED: *  Race number (e.g. Race 3)
        EXPECTED: *  Race Name (e.g 15:25 Wincanton (WI))
        EXPECTED: *  Date of bet placement in a format MM/DD/YYYY (e.g. 10/19/2018)
        EXPECTED: *  Bet Receipt id (e.g. P/0156602/0000117)
        EXPECTED: *  Stake value (e.g. £2.00)
        EXPECTED: *  Estimated returns value is N/A (exact value in case bet is settled as Won)
        """
        self.verify_trifecta_tote_bet_information(self.site.open_bets)
