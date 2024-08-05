import pytest

import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # cannot test LiveServ updates on HL/PROD
# @pytest.mark.hl
@pytest.mark.prod_incident
@pytest.mark.desktop
@pytest.mark.liveserv_updates
@pytest.mark.betslip
@pytest.mark.medium
@pytest.mark.login
@vtest
class Test_C9243966_Verify_adding_new_selection_to_the_BetSlip_which_contains_undisplayed_selection(BaseBetSlipTest):
    """
    TR_ID: C9243966
    NAME: Verify adding new selection to the BetSlip which contains undisplayed selection
    DESCRIPTION: This test case verifies adding new selection to the BetSlip which contains undisplayed selection.
    PRECONDITIONS: * User is Logged in
    PRECONDITIONS: * User has positive balance to place a bet
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add events and login
        """
        event = self.ob_config.add_autotest_premier_league_football_event()
        event_2 = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.selection, self.__class__.selection_ids = event.team1, event.selection_ids
        self.__class__.selection_2, self.__class__.selection_ids_2 = event_2.team1, event_2.selection_ids
        self.site.login(username=tests.settings.betplacement_user)

    def test_001_add_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add selection to the BetSlip
        EXPECTED: Selection is added
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids[self.selection])

    def test_002_undisplay_current_selection(self):
        """
        DESCRIPTION: Undisplay current selection
        EXPECTED: Current selection still remain in the BetSlip
        """
        self.ob_config.change_selection_state(selection_id=self.selection_ids[self.selection],
                                              displayed=False, active=True)
        singles_section = self.get_betslip_sections().Singles
        stake_name, _ = list(singles_section.items())[0]
        self.assertEqual(stake_name, self.selection, msg=f'Selection {self.selection} should be present in betslip')

    def test_003_add_new_selection_to_the_betslip_and_open_it(self):
        """
        DESCRIPTION: Add new selection to the BetSlip and open it
        EXPECTED: * New selection is added to the BetSlip
        EXPECTED: * Old (undisplayed) selection remains shown in the BetSlip
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids_2[self.selection_2])
        singles_section = self.get_betslip_sections().Singles
        stake_name, _ = list(singles_section.items())[0]
        self.assertEqual(stake_name, self.selection, msg=f'Selection {self.selection} is not present in betslip')
        stake_name2, _ = list(singles_section.items())[1]
        self.assertEqual(stake_name2, self.selection_2, msg=f'Selection {self.selection_2} is not present in betslip')
        self.assertEqual(len(singles_section.items()), self.expected_betslip_counter_value,
                         msg='Newly added selection and old (undisplayed) selection are not present in betslip')

    def test_004_place_bet(self):
        """
        DESCRIPTION: Place bet
        EXPECTED: Bet is placed for both selection
        """
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        betreceipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(betreceipt_sections, msg='No BetReceipt sections found')
        for section_name, section in betreceipt_sections.items():
            receipts = section.items_as_ordered_dict
            self.assertTrue(receipts, msg='No Bet receipt sections found')
            self.assertTrue(len(receipts) == self.expected_betslip_counter_value, msg='Bet was not placed on all selections')
            self.assertTrue(receipts.get(self.selection), msg=f'Selection {self.selection} is not present in receipt')
            self.assertTrue(receipts.get(self.selection_2), msg=f'Selection {self.selection_2} is not present in receipt')
