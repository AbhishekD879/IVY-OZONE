import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common
from datetime import timedelta
from datetime import date


@pytest.mark.medium
@pytest.mark.user_account
@pytest.mark.desktop
@pytest.mark.uat
@pytest.mark.prod
@pytest.mark.stg2
@pytest.mark.tst2
@vtest
class Test_C44870365_Verfy_Settled_Bets_Tab_and_its_contents(Common):
    """
    TR_ID: C44870365
    NAME: Verify Settled Bets Tab and its contents.
    DESCRIPTION: This TC is to verify Settled Tab and its contents.
    PRECONDITIONS: Used should be logged in
    PRECONDITIONS: User must have some single, double, each way and accumulator bets placed.
    PRECONDITIONS: User should have some settled bets.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Used should be logged in
        PRECONDITIONS: User must have some single, double, each way and accumulator bets placed.
        PRECONDITIONS: User should have some settled bets.
        """
        self.site.login()
        self.site.wait_content_state('Homepage')
        self.site.open_my_bets_settled_bets()
        self.site.close_all_dialogs(timeout=5)

    def test_001__verfiy_settled_bets_tab_header_for_following_bet_type_for_each_bet_single__double__acca(self):
        """
        DESCRIPTION: Verfiy Settled Bets Tab Header for following
        DESCRIPTION: * Bet type for each bet (Single / Double / ACCA etc )
        DESCRIPTION: * Result label for the overall bet (Lost/ Won/ Cashed out, Void) ( Left/Right Layout)
        EXPECTED: User is able to see
        EXPECTED: * Bet type for each bet (Single / Double / ACCA etc ) (Left side of bet header)
        EXPECTED: * Result label for the overall bet (Lost/ Won/ Cashed out, Void) (Right side of the bet header)
        """
        bets = self.site.bet_history.tab_content.accordions_list.items_as_ordered_dict
        current_tab_name = self.site.bet_history.tab_content.grouping_buttons.current
        if(len(bets)) == 0:
            self._logger.info(f'There are no bets displayed on "{current_tab_name}" of "{vec.bet_history.SETTLED_BETS_TAB_NAME}"')
        else:
            bet_headers = self.site.bet_history.bet_types
            count = 0
            for bet_type in bet_headers:
                if any(subheader in bet_type for subheader in vec.betslip.BETSLIP_BETTYPES):
                    _, bet = self.site.bet_history.tab_content.accordions_list.get_bet(bet_type=bet_type)
                    count += 1
                self.assertEqual(bet.bet_type, bet_type,
                                 msg=f'Bet type: "{bet.bet_type}" '
                                     f'is not as expected: "{bet_type}"')
                self.assertTrue(bet.date, msg=f'Bet date is not shown for bet type "{bet_type}"')
                odds_sign = bet.odds_sign.strip('"')
                bet_odds = f'{odds_sign}{bet.odds_value}'
                self.assertTrue(bet_odds, msg=f'odds are not present for bet type "{bet_type}" ')
                self.assertTrue(bet.stake.value, msg=f'stake is not present for bet type "{bet_type}"')
                self.assertTrue(bet.bet_receipt_info.bet_id, msg=f'bet id is not present for bet type "{bet_type}"')
                status = bet.bet_status
                self.assertTrue(status in vec.betslip.BETSLIP_BETSTATUS, msg=f'bets not available for bet type "{bet_type}"')
                if count >= 3:
                    break

    def test_002_verify_user_can_see__profit__loss_information_with_down_arrow(self):
        """
        DESCRIPTION: Verify user can see  Profit / Loss information with down arrow.
        EXPECTED: User is able to see Profit/Loss section just above the bets with down arrow on it.
        """
        self.__class__.profit_loss = self.site.bet_history.tab_content.accordions_list.settled_bets
        self.assertTrue(self.profit_loss, msg='Profit / Loss information not shown')

    def test_003_verify_user_can_see_profit_loss_information_by_clicking_on_it(self):
        """
        DESCRIPTION: Verify user can see Profit/Loss information by clicking on it.
        EXPECTED: Uses is able Profit/Loss information by clicking on it (This will show information based on dates set in the calendar)
        """
        self.profit_loss.click()
        self._logger.info(f'No transactions listed with message- {self.site.transaction_history.transaction_message}') \
            if self.site.transaction_history.transaction_message else \
            self.assertTrue(self.site.transaction_history.transaction_data, msg='No transactions history found')
        if self.device_type == 'mobile':
            self.site.transaction_history.back_button.click()
        else:
            self.navigate_to_page(name='Home')
            self.site.wait_content_state('HomePage')
            self.site.open_my_bets_settled_bets()

    def test_004_verify_information_which_appears_on_screen_is_based_on_dates_choosen(self):
        """
        DESCRIPTION: Verify information which appears on screen is based on dates chosen
        DESCRIPTION: Verify Sports, Lotto and Pools tab in 'Settled Bets'
        DESCRIPTION: Verify Settled Bets Tab and the footer lists Contains
        DESCRIPTION: -The stake
        DESCRIPTION: -Potential return
        DESCRIPTION: -Receipt ID
        DESCRIPTION: -Time and date stamp
        EXPECTED: User is able to see information based on dates set in the calendar for following tabs Sports, Lotto and Pools.
        EXPECTED: User is able to see following details.
        EXPECTED: -The stake
        EXPECTED: -Potential return
        EXPECTED: -Receipt ID
        EXPECTED: -Time and date stamp
        """
        new_date = date.today() - timedelta(days=5)
        past_date = new_date.__format__('%d/%m/%Y')
        self.site.bet_history.tab_content.accordions_list.date_picker.date_from.date_picker_value = past_date
        self.assertEqual(self.site.bet_history.tab_content.accordions_list.date_picker.date_from.text, past_date,
                         msg='Date range is not selected')
        settled_bet_tabs = self.site.bet_history.tab_content.grouping_buttons.items_as_ordered_dict
        self.assertTrue(settled_bet_tabs, msg='Settled Bet tabs are not displayed')
        for tab_name, tab in settled_bet_tabs.items():
            tab.click()
            self.site.wait_content_state_changed()
            expected_tab_name = self.site.bet_history.tab_content.grouping_buttons.current
            self.assertEqual(tab_name, expected_tab_name, msg=f'Actual "{tab_name}" is not matched with the expected "{expected_tab_name}"')
            self.test_001__verfiy_settled_bets_tab_header_for_following_bet_type_for_each_bet_single__double__acca()
