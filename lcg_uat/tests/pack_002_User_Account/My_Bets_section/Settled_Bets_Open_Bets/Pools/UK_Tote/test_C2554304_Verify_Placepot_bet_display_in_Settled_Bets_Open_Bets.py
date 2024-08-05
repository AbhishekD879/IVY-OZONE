import re
from datetime import datetime

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
@pytest.mark.open_bets
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.bet_placement
@pytest.mark.betslip
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.login
@vtest
class Test_C2554304_Verify_Placepot_bet_is_displayed_on_Open_Bets_tab(BaseUKTote, BaseBetSlipTest):
    """
    TR_ID: C2554304
    NAME: Verify Placepot bet is displayed on Open Bets tab
    DESCRIPTION: This test case verifies the displayed contents of a Placepot tote bet in the Open Bets
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User has placed tote Placepot Bet(s) on UK Tote events
    """
    keep_browser_open = True
    selection_outcomes = []
    expected_active_btn = vec.bet_history.POOLS_TAB_NAME
    expected_market_name = 'Placepot'
    bet_history = vec.bet_history.SETTLED_BETS_TAB_NAME
    open_bets = vec.bet_history.OPEN_BETS_TAB_NAME

    def verify_placepot_tote_bet_information(self):
        """
        This method verifies whether Placepot tote bet information corresponds to placed bet:
        * Placepot title
        * Leg number with Time and Name of the meeting
        * Selection Name/s for each Leg
        * Date of bet placement in a format MM/DD/YYYY (e.g. 10/19/2018)
        * Bet Receipt id (e.g. P/0156602/0000117)
        * Stake value (e.g. £2.00)
        * Estimated returns value is N/A
        """
        bet_name, self.__class__.tote_pool = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type='TOTEPOOL', event_names=self.updated_event_names, number_of_bets=1)

        bet_date = self.tote_pool.bet_receipt_info.date.text
        self.assertTrue(bet_date, msg='Bet date was not found')
        time_diff = self.now_date - datetime.strptime(bet_date, self.time_format_pattern)
        self.assertTrue(time_diff.seconds < 61,
                        msg=f'Date of bet placement does not correspond to placed bet. '
                            f'Difference between times is {time_diff.seconds} seconds')

        self.assertEqual(self.tote_pool.bet_receipt_info.bet_receipt.value, self.outcome_bet_receipt_bet_id,
                         msg=f'Open Bet section: {self.tote_pool.name} '
                             f'bet receipt ID {self.outcome_bet_receipt_bet_id} not found')
        self.assertEqual(self.tote_pool.stake.stake_value, '{0:.2f}'.format(self.bet_amount),
                         msg=f'Total Stake amount: {self.tote_pool.stake.value} '
                             f'is not as expected: {self.total_stake} for bet {self.tote_pool.name}')
        self.assertEqual(self.tote_pool.est_returns.value, 'N/A',
                         msg=f'Estimated returns: {self.tote_pool.est_returns.value} '
                             f'is not as expected: "N/A"')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Run preconditions
        """
        event = self.get_uk_tote_event(uk_tote_placepot=True)
        self.__class__.eventID = event.event_id
        self.__class__.event_typename = event.event_typename.strip()
        self.__class__.uk_event_typename = event.uk_tote_typename
        self.__class__.bet_amount = event.min_total_stake

        self.site.login()
        placepot_bet_results = self.place_multiple_legs_bet(event_id=self.eventID,
                                                            tab_name=vec.uk_tote.UK_TOTE_TABS.placepot,
                                                            unit_stake=self.bet_amount)
        self.__class__.selected_outcomes = placepot_bet_results.get('selected_outcomes')
        self.__class__.races_titles = placepot_bet_results.get('races_titles')
        self.site.open_betslip()
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section.items(), msg='*** No stakes found')
        stake_name, stake = list(singles_section.items())[0]
        self.__class__.stake = stake
        selection_outcomes = self.stake.multiple_tote_outcomes.items_as_ordered_dict
        self.assertTrue(selection_outcomes, msg='No UK Tote selections found')
        self.__class__.selection_outcomes = (list(selection_outcomes.keys()))
        self.enter_stake_amount(stake=(self.stake.name, self.stake))
        self.get_betslip_content().bet_now_button.click()
        self.check_bet_receipt_is_displayed()

        self.__class__.now_date = self.get_local_time_for_uk_tote(hours=1)

        receipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(receipt_sections, msg='No receipt sections found in BetReceipt')
        single_section = receipt_sections.get(vec.betslip.BETSLIP_SINGLES_NAME)

        self.assertTrue(single_section, msg=f'"{vec.betslip.BETSLIP_SINGLES_NAME}" section was not found')
        singles = single_section.items_as_ordered_dict
        self.assertTrue(singles, msg='No Single sections found')
        name = f'{vec.uk_tote.UPLP} {vec.uk_tote.TOTEPOOL.title()}'
        single = singles.get(name)
        self.assertTrue(single, msg=f'"{name}" not found in {list(singles.keys())}')

        self.__class__.outcome_bet_receipt_bet_id = single.bet_id
        self.site.bet_receipt.close_button.click()

    def test_001_navigate_to_open_bets_tab(self):
        """
        DESCRIPTION: Navigate to Open Bets tab
        """
        self.site.open_my_bets_open_bets()

    def test_002_tap_on_the_pools_sub_section(self):
        """
        DESCRIPTION: Tap on the Pools sub-section
        EXPECTED: All UK tote bets are displayed by default in List view
        EXPECTED: Placepot tote bet information corresponds to placed bet:
        EXPECTED: * Placepot title
        EXPECTED: * Leg number with Time and Name of the meeting
        EXPECTED: * Selection Name/s for each Leg
        EXPECTED: * Date of bet placement in a format MM/DD/YYYY (e.g. 10/19/2018)
        EXPECTED: * Bet Receipt id (e.g. P/0156602/0000117)
        EXPECTED: * Stake value (e.g. £2.00)
        EXPECTED: * Estimated returns value is N/A
        """
        self.site.open_bets.tab_content.grouping_buttons.click_button(vec.bet_history.POOLS_TAB_NAME)
        active_button = self.site.open_bets.tab_content.grouping_buttons.current
        self.assertEqual(active_button, self.expected_active_btn,
                         msg=f'{active_button} section is selected instead of {self.expected_active_btn}')
        sections = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='Can not find any section')
        # Removing colons -  ":" 'Leg 1: 18:00' => 'Leg 1 18:00'
        # TODO https://jira.egalacoral.com/browse/BMA-35778
        new_selection_outcomes = list(map(lambda x: re.sub(r"(\d)+(:) ", lambda str: str.group(1) + " ", x),
                                          self.selection_outcomes))
        # replacing to uk_event_type_name 'Fakenham' => 'Fakenham (FA)'
        self.__class__.updated_event_names = list(
            map(lambda str: str.replace(self.event_typename, self.uk_event_typename), new_selection_outcomes))
        self.verify_placepot_tote_bet_information()
