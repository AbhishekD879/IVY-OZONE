import pytest
import voltron.environments.constants as vec
from tests.pack_012_UK_Tote.BaseUKTote import BaseUKTote
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.mobile_only
@vtest
class Test_C16852870_Verify_Quick_Deposit_for_UK_Tote_bets(BaseUKTote, BaseBetSlipTest):
    """
    TR_ID: C16852870
    NAME: Verify Quick Deposit for UK Tote bets
    DESCRIPTION: Verify that the user is redirected on Deposit page after clicking the "Deposit" button on the header in the betslip
    PRECONDITIONS: User is logged in
    """
    keep_browser_open = True
    addition = 5.00

    def test_001_go_to_the_horse_racing_page(self):
        """
        DESCRIPTION: Go to the Horse racing page
        EXPECTED: Horse racing page is opened
        """
        event = self.get_uk_tote_event(uk_tote_exacta=True)
        self.__class__.selection_ids = event.selection_ids[:2]
        self.__class__.eventID = event.event_id
        self.site.login()
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('Horseracing')

    def test_002_click_on_the_event_with_the_tote_available(self):
        """
        DESCRIPTION: Click on the event with the Tote available
        EXPECTED: The event is loaded
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        tab_opened = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(
            vec.racing.RACING_EDP_MARKET_TABS.totepool)
        self.assertTrue(tab_opened, msg='UK Tote tab is not opened')

    def test_003_click_on_the_add_to_betslip_button_ex_add_2_selections_for_exacta_tote_pool(self):
        """
        DESCRIPTION: Click on the "Add to Betslip" button (ex add 2 selections for Exacta Tote Pool)
        EXPECTED: The selections are added to Betslip
        """
        self.__class__.user_balance = self.site.header.user_balance
        self.open_betslip_with_selections(selection_ids=self.selection_ids)

    def test_004_go_to_the_betslip(self):
        """
        DESCRIPTION: Go to the Betslip
        EXPECTED: Betslip is opened and the added Tote bet is displayed
        """
        # covered in step 3

    def test_005_enter_the_stake_that_is_bigger_than_the_user_balance_tap_place_bet_button(self):
        """
        DESCRIPTION: Enter the stake that is bigger than the user balance, tap 'Place Bet' button
        EXPECTED: The "insufficient funds in your account to place bet" message is displayed
        """
        self.assertTrue(self.get_betslip_content(),
                        msg='Betslip widget was not opened')
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section, msg='No one added selection found on Betslip')
        selection_name = list(singles_section.ordered_collection.keys())[0]
        self.__class__.stake = singles_section.get(selection_name)
        self.assertTrue(self.stake, msg=f'"{selection_name}" stake was not found on the Betslip')
        self.__class__.bet_amount = self.user_balance + self.addition
        self.enter_stake_amount(stake=(self.stake.name, self.stake))
        actual_stake_amount = self.stake.amount_form.input.value
        actual_message = self.get_betslip_content().bet_amount_warning_message
        expected_message = vec.quickbet.QUICKBET_DEPOSIT_NOTIFICATION.format(self.addition)
        self.assertEqual(actual_message, expected_message,
                         msg=f'Actual message "{actual_message}" is not the same as expected "{expected_message}"')
        expected_stake_amount = '{0:.2f}'.format(self.bet_amount)
        self.assertEqual(actual_stake_amount, expected_stake_amount,
                         msg=f'Actual stake input amount: "{actual_stake_amount}", expected: "{expected_stake_amount}"')
        self.assertEqual(self.get_betslip_content().make_quick_deposit_button.name,
                         vec.Quickdeposit.MAKE_DEPOSIT_BUTTON_CAPTION,
                         msg=f'"{self.get_betslip_content().make_quick_deposit_button.name}" is no the same as '
                             f'expected "{vec.Quickdeposit.MAKE_DEPOSIT_BUTTON_CAPTION}"')

    def test_006_click_on_the_user_balance_on_the_header_in_the_betslip(self):
        """
        DESCRIPTION: Click on the user balance on the header in the betslip
        EXPECTED: Two sections are opened:
        EXPECTED: - Hide Balance
        EXPECTED: - Deposit
        """
        self.assertTrue(self.get_betslip_content().quick_deposit_link.is_displayed(),
                        msg='"Deposit" option is not availale in balance dropdown')
        self.get_betslip_content().balance_button.click()
        self.assertTrue(self.get_betslip_content().hide_balance_option.is_displayed(),
                        msg='"Hide Balance" option is not availale in balance dropdown')

    def test_007_click_on_the_deposit_button(self):
        """
        DESCRIPTION: Click on the "Deposit" button
        EXPECTED: Betslip is closed and the user is redirected to the main Deposit Page
        """
        self.get_betslip_content().balance_button.click()
        self.get_betslip_content().quick_deposit_link.click()
        wait_for_result(lambda: self.site.deposit.is_displayed(),
                        name=f'main Deposit Page to be displayed',
                        timeout=15)
        self.assertTrue(self.site.deposit.is_displayed(), msg='"Deposit" menu is not displayed')
