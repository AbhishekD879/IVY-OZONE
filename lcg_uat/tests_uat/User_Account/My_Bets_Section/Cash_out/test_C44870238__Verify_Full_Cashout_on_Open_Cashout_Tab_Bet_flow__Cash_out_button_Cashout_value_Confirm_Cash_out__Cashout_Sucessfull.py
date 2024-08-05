import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from crlat_siteserve_client.siteserve_client import simple_filter
from crlat_siteserve_client.constants import ATTRIBUTES, LEVELS, OPERATORS


@pytest.mark.stg2
@pytest.mark.tst2
@pytest.mark.p2
@pytest.mark.uat
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.cash_out
@vtest
class Test_C44870238__Verify_Full_Cashout_on_Open_Cashout_Tab_Bet_flow__Cash_out_button_Cashout_value_Confirm_Cash_out__Cashout_Sucessfull(BaseBetSlipTest):
    """
    TR_ID: C44870238
    NAME: -Verify Full Cashout on Open/Cashout Tab Bet flow --> Cash-out button (Cashout value)-->Confirm Cash-out -->Cashout Sucessfull
    """
    keep_browser_open = True

    def test_001_make_a_bet_from_a_cash_out_market(self):
        """
        DESCRIPTION: Make a bet from a cash out market
        EXPECTED: You should have made a bet from a cash out market.
        """
        self.site.login()
        cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y'), \
            simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y')
        event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                    all_available_events=True,
                                                    additional_filters=cashout_filter,
                                                    in_play_event=False)[0]
        self.__class__.event_name = event['event']['name']
        market = next((market for market in event['event']['children']), None)
        outcomes_resp = market['market']['children']
        all_selection_ids = {i['outcome']['name']: i['outcome']['id']
                             for i in outcomes_resp if 'Unnamed' not in i['outcome']['name']}
        self.open_betslip_with_selections(selection_ids=list(all_selection_ids.values())[0])
        self.place_and_validate_single_bet()
        self.check_bet_receipt_is_displayed()
        self.site.close_betreceipt()

    def test_002_go_to_my_bets_open_bets_and_check_that_you_see_the_cash_out_button_for_this_bet(self):
        """
        DESCRIPTION: Go to My Bets->Open Bets and check that you see the Cash Out button for this bet.
        EXPECTED: The bet should show a Cash Out button.
        """
        self.site.open_my_bets_open_bets()
        bet_name, self.__class__.bet = self.site.open_bets.tab_content.accordions_list. \
            get_bet(bet_type='SINGLE', event_names=self.event_name)
        self.assertTrue(self.bet.buttons_panel.has_full_cashout_button, msg='"FULL CASHOUT" button is not present')

    def test_003_click_on_the_cash_out_button_and_check_that_you_see_a_flashing_confirm_cash_out_button(self):
        """
        DESCRIPTION: Click on the Cash Out button and check that you see a flashing Confirm Cash Out button
        EXPECTED: You should see the flashing Confirm Cash Out Button
        """
        self.bet.buttons_panel.full_cashout_button.click()
        self.assertTrue(self.bet.buttons_panel.has_confirm_cashout_button(), msg='Confirm cash out button is not displayed')

    def test_004_click_on_the_confirm_cash_out_button(self):
        """
        DESCRIPTION: Click on the Confirm Cash Out button
        EXPECTED: You should have clicked on the Confirm Cash Out button and your bet should have been cashed out
        """
        self.bet.buttons_panel.cashout_button.click()
        self.assertTrue(self.bet.has_cashed_out_mark(timeout=20), msg='Cash Out is not successful')

    def test_005_verify_that_you_see_a_cash_out_successful_message(self):
        """
        DESCRIPTION: Verify that you see a Cash Out Successful message
        EXPECTED: You should see a Cash Out Successful message
        """
        self.assertTrue(self.bet.wait_for_message(message=vec.bet_history.FULL_CASH_OUT_SUCCESS),
                        msg=f'Message "{vec.bet_history.FULL_CASH_OUT_SUCCESS}" is not Displayed')

    def test_006_go_to_my_bets_settled_bets_and_verify_that_you_see_the_cashed_out_bet_there(self):
        """
        DESCRIPTION: Go to My Bets->Settled Bets and verify that you see the Cashed Out bet there.
        EXPECTED: Your Cashed Out bet should now be in My Bets->Settled Bets
        """
        self.site.open_my_bets_settled_bets()
        _, bet = self.site.bet_history.tab_content.accordions_list. \
            get_bet(bet_type='SINGLE', event_names=self.event_name, raise_exception=False)
        self.assertTrue(bet.event_name == self.event_name, msg=f'Cannot find event {self.event_name} in Settled Bets tab')

    def test_007_go_to_my_bets_open_bets_and_verify_that_the_cashed_out_bet_is_no_longer_there(self):
        """
        DESCRIPTION: Go to My Bets->Open Bets and verify that the Cashed Out bet is no longer there.
        EXPECTED: The Cashed Out bet should not be in My Bets->Open Bets.
        """
        self.navigate_to_page(name='/')
        self.site.wait_content_state(state_name='Homepage')
        self.site.open_my_bets_open_bets()
        sections = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        if len(sections) == 0:
            self._logger.info('*** Currently have no open bets')
        else:
            for section in sections.keys():
                if vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE in section:
                    self.assertFalse(self.event_name in section, msg=f'Cashed out event "{self.event_name}" found in '
                                                                     f'Open Bets tab')
