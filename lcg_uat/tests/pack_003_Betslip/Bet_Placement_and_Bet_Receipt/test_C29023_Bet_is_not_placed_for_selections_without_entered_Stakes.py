import voltron.environments.constants as vec
import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.desktop
@pytest.mark.betslip
@pytest.mark.bet_placement
@pytest.mark.medium
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C29023_Bet_is_not_placed_for_selections_without_entered_Stakes(BaseBetSlipTest):
    """
    TR_ID: C29023
    NAME: Bet is not placed for selections without entered Stakes
    DESCRIPTION: This test case verifies Handling when Stake fields for some of several selections are empty
    PRECONDITIONS: 1.  User is logged in
    PRECONDITIONS: 2.  User has sufficient funds for placing a bet
    """
    keep_browser_open = True
    stakes_to_bet = 2
    singles_name = vec.betslip.BETSLIP_SINGLES_NAME.title()

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test events and log in
        """
        if tests.settings.backend_env != 'prod':
            event_params = self.ob_config.add_UK_greyhound_racing_event(number_of_runners=3)
            self.__class__.selection_ids = event_params.selection_ids
        else:
            self.__class__.selection_ids = \
                self.get_active_event_selections_for_category(category_id=self.ob_config.backend.ti.horse_racing.category_id)
        self.site.login(username=tests.settings.betplacement_user)

    def test_001_add_few_selections_to_the_betslip(self):
        """
        DESCRIPTION: Add a few selections to the Betslip
        EXPECTED: Betslip is opened, selections are displayed on the Betslip
        """
        self.open_betslip_with_selections(selection_ids=list(self.selection_ids.values()))

    def test_002_enter_valid_stake_for_some_of_added_selections_the_other_selections_leave_without_stakes(self):
        """
        DESCRIPTION: Enter valid 'Stake' for some of added selections, the other selections leave without Stakes
        """
        singles_section = self.get_betslip_sections().Singles
        self.__class__.stake_name1, _ = list(singles_section.items())[0]
        self.__class__.stake_name2, _ = list(singles_section.items())[1]
        for stake in self.zip_available_stakes(section=singles_section, number_of_stakes=self.stakes_to_bet).items():
            self.enter_stake_amount(stake=stake)

    def test_003_tap_bet_now_button(self):
        """
        DESCRIPTION: Tap 'Bet Now' button
        EXPECTED: - 'Bet Now' button is enabled and it is possible to start bet placement process as soon as stake is entered at least for one selection
        EXPECTED: - Bet is successfully placed for the selections with entered Stake, other selections are ignored and cleared from the Betslip
        EXPECTED: - Bet Receipt is shown and contains information about placed bets (only selections with entered Stakes, selections without Stakes are not displayed on Bet Receipt)
        """
        self.assertTrue(self.get_betslip_content().bet_now_button.is_enabled(), msg='"Bet Now" button is not enabled')
        self.get_betslip_content().bet_now_button.click()
        self.check_bet_receipt_is_displayed()
        betreceipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(betreceipt_sections, msg='No Bet Receipt sections found')
        singles = betreceipt_sections.get(self.singles_name, None)
        receipts = singles.items_as_ordered_dict
        self.assertEqual(len(receipts), self.stakes_to_bet,
                         msg=f'{self.stakes_to_bet} found in Bet Receipt instead of {len(receipts)}')

        receipt_names = [list(receipts.keys())[0], list(receipts.keys())[1]]
        stake_names = [self.stake_name1, self.stake_name2]
        self.assertListEqual(sorted(receipt_names), sorted(stake_names),
                             msg=f'Stake names {sorted(stake_names)} '
                                 f'are not the same as on receipt {sorted(receipt_names)}')
